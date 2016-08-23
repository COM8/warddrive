
import gpsd
from time import sleep
import RPi.GPIO as GPIO
from os import system
import iwlist
def stop():
	import pprint
	pp=pprint()
	pp.pprint(loggedData)
	"""file = open("logFile.log", "a")
	for item in loggedData:
		file.writelines(["%s\n" % str(element) for element in item])"""
	exit(0)

if __name__ == "__main__":
	loggedData = list()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4,GPIO.IN) 
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
			system("clear")
			if GPIO.input(4)==GPIO.LOW:
				try:
					packet = gpsd.get_current()
					position = packet.position()
					percision = packet.position_precision()
					content = iwlist.scan(interface='wlan1')
					cells = iwlist.parse(content)
					for element in cells:
						element["positon"] = position
						element["percision"] = percision
						del element["cellnumber"]
						print(element)
						print("_____________________________________________________________")
					loggedData.append(cells)
					sleep(0.2)

				except gpsd.NoFixError:
					print("no fix")
				except IndexError:
					pass
				except KeyboardInterrupt:
					stop()
				except :
					pass
			else:
				print("no Fix")
		except KeyboardInterrupt:
			stop()