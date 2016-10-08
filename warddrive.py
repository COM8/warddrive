#!/usr/bin/python3.4

import gpsd
import RPi.GPIO as GPIO
import iwlist
import pickle
import RPi.GPIO as GPIO
from os import chdir
from time import sleep

def stop(channel):
    save()
    GPIO.cleanup()
    # exit(0)
    while GPIO.input == 0:
        sleep(0.5)
    while GPIO.input == 1:
        sleep(0.5)
    exit(0)
    main()

def save():
    with open("logFile" + '.pkl', 'wb') as f:
        pickle.dump(loggedData, f, pickle.HIGHEST_PROTOCOL)
		
def setupGPIO():
	GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(19, 1)
    #GPIO.add_event_detect(23, GPIO.FALLING, callback=stop, bouncetime=200)

def main():
    global loggedData
    i = 0
    state = 0
    loggedData = None
	
	chdir("/home/pi/GPS/")
    try:
        with open("logFile" + '.pkl', 'rb') as f:
            loggedData = pickle.load(f)
    except FileNotFoundError:
        loggedData = dict()
    
	setupGPIO()
	
    try:
        gpsd.connect()
    except ConnectionRefusedError:
        from time import sleep
        from os import system
        print("Service not running... starting it")
        system("sudo killall gpsd")
        system("sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock")
        sleep(10)
        gpsd.connect()
		
    while True:
        try:
            if GPIO.input(23) == 0:
                stop(channel=None)
            if GPIO.input(4) == GPIO.LOW:
                GPIO.output(13, 1)
                try:
                    packet = gpsd.get_current()
                    position = packet.position()
                    percision = packet.position_precision()
                    for interface in range(1, 2):
                        content = iwlist.scan(
                            interface='wlan' + str(interface))
                        if len(content) > 0:
                            for element in iwlist.parse(content):
                                element["position"] = position
                                element["percision"] = percision
                                del element["cellnumber"]
                                try:
                                    dif1 = (percision[0] + percision[1])
                                    dif2 = loggedData[element["mac"]]["percision"][
                                        0] + loggedData[element["mac"]]["percision"][1]
                                    if dif1 < dif2:
                                        if dif1 + 10 <= dif2:
                                            loggedData[element["mac"]][
                                                "position"] = position
                                            loggedData[element["mac"]][
                                                "percision"] = percision
                                        else:
                                            loggedData[element["mac"]]["position"] = (((loggedData[element["mac"]]["position"][
                                                                                      0]) + element["position"][0]) / 2, ((loggedData[element["mac"]]["position"][1]) + element["position"][1]) / 2)
                                            loggedData[element["mac"]]["percision"] = ((percision[0] + loggedData[element["mac"]][
                                                                                       "percision"][0]) / 2, (percision[1] + loggedData[element["mac"]]["percision"][1]) / 2)
                                    elif dif1 >= dif2:
                                        if dif1 <= (dif2 + 10):
                                            loggedData[element["mac"]]["position"] = (((loggedData[element["mac"]]["position"][
                                                                                      0]) + element["position"][0]) / 2, ((loggedData[element["mac"]]["position"][1]) + element["position"][1]) / 2)
                                            loggedData[element["mac"]]["percision"] = ((percision[0] + loggedData[element["mac"]][
                                                                                       "percision"][0]) / 2, (percision[1] + loggedData[element["mac"]]["percision"][1]) / 2)
                                except KeyError:
                                    print(element)
                                    loggedData[element["mac"]] = element
                        else:
                            break
                except gpsd.NoFixError:
                    pass
                except IndexError:
                    pass
                except KeyboardInterrupt:
                    stop(23)
                except KeyError:
                    pass
                else:
                    if i >= 5:
                        save()
                        i = 0
                    else:
                        i += 1
                    if state == 0:
                        GPIO.output(6, 1)
                        state = 1
                    else:
                        GPIO.output(6, 0)
                        state = 0
            else:
                GPIO.output(13, 0)
        except KeyboardInterrupt:
            print(loggedData)
            stop(23)

if __name__ == "__main__":
    main()
