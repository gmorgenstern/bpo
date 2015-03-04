# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import RPi.GPIO as GPIO
import bluetooth._bluetooth as bluez
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
dev_id = 0
UUID = "e2c56db5dffb48d2b060d0f5a71096e0"
GPIOStatus=False 
GPIO.output(3,False)

try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	print "----------"
        time.sleep(1)
        counter=0
        acc=0
	for beacon in returnedList:
                if len(beacon) < 6:
                   continue 
	 	tokenbeacon = beacon.split(",")
                acc = acc + int(tokenbeacon[5])
                counter = counter + 1  
                print beacon
        power = acc/counter 
        print power        
	if power < -72: 
               if GPIOStatus == False:
                    GPIO.output(3,True)
                    GPIOStatus = True
        else: 
               if GPIOStatus == True:   
                    GPIO.output(3,False)
                    GPIOStatus = False
 
	

