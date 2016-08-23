
import gpsd
from time import sleep
import RPi.GPIO as GPIO
from os import system
import iwlist
import pickle
from os import chdir
def save():
	with open("logFile" + '.pkl', 'wb') as f:
		pickle.dump(loggedData, f, pickle.HIGHEST_PROTOCOL)
if __name__ == "__main__":
	chdir("/home/pi/GPS/")
	loggedData =None
	try:
		with open("logFile" + '.pkl', 'rb') as f:
			loggedData = pickle.load(f)
	except FileNotFoundError:
		loggedData=dict()
	print(loggedData)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4,GPIO.IN) 
	GPIO.setup(19,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.output(19,1)
	try:
		gpsd.connect()
	except ConnectionRefusedError:
		print("Service not running... starting it")		
		system("sudo killall gpsd")
		system("sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock")
		sleep(10)
		gpsd.connect()
	while True:
		i=0
		try:
			#system("clear")
			if GPIO.input(4)==GPIO.LOW:
				GPIO.output(13,1)
				try:
					packet = gpsd.get_current()
					position = packet.position()
					percision = packet.position_precision()
					content = iwlist.scan(interface='wlan1')
					cells = iwlist.parse(content)
					for element in cells:
						element["position"] = position
						element["percision"] = percision
						del element["cellnumber"]
						print("_____________________________________________________________")
						try:
							x=((loggedData[element["mac"]]["position"][0])+element["position"][0])/2
							y=((loggedData[element["mac"]]["position"][1])+element["position"][1])/2
							loggedData[element["mac"]]["position"][0]=x
							loggedData[element["mac"]]["position"][1]=y
							print("no new Wifi")
						except KeyError:
							loggedData[element["mac"]]=element
							print(element)
					if i<=15:
						save()
					else:
						i+=1

				except gpsd.NoFixError:
					print("no fix")
				except IndexError:
					pass
				except KeyboardInterrupt:
					print(loggedData)
					save()

					exit(0)
				except :
					pass
			else:
				GPIO.output(13,0)
				print("no Fix")
		except KeyboardInterrupt:
			print(loggedData)
			save()
			exit(0)