
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
	i=0
	state=0
	chdir("/home/pi/GPS/")
	loggedData =None
	try:
		with open("logFile" + '.pkl', 'rb') as f:
			loggedData = pickle.load(f)
	except FileNotFoundError:
		loggedData=dict()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4,GPIO.IN) 
	GPIO.setup(19,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(6,GPIO.OUT)
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
		try:
			if GPIO.input(4)==GPIO.LOW:
				GPIO.output(13,1)
				try:
					packet = gpsd.get_current()
					position = packet.position()
					percision = packet.position_precision()
					for interface in range(0,2):
						content = iwlist.scan(interface='wlan'+str(interface))
						if len(content)>0:
							for element in iwlist.parse(content):
								element["position"] = position
								element["percision"] = percision
								del element["cellnumber"]
								try:
									x=((loggedData[element["mac"]]["position"][0])+element["position"][0])/2
									y=((loggedData[element["mac"]]["position"][1])+element["position"][1])/2
									loggedData[element["mac"]]["position"]=(x,y)
								except KeyError:
									loggedData[element["mac"]]=element
						else:
							break
				except gpsd.NoFixError:
					pass
				except FileNotFoundError:
					pass
				except KeyboardInterrupt:
					save()
					GPIO.cleanup()
					exit(0)
				except KeyError:
					pass
				else:
					if i>=15:
						save()
						if state==0:
							GPIO.output(6,1)
							state=1
						else:
							GPIO.output(6,0)
							state=0
						i=0

					else:
						i+=1
			else:
				GPIO.output(13,0)
		except KeyboardInterrupt:
			print(loggedData)
			save()
			GPIO.cleanup()
			exit(0)
			