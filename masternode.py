#! /usr/bin/python
import time
import threading
from xbee import XBee
from serial import Serial

#MasterNode python script: Includes modules, networkhandler, gps handler, class handler, optimal algorithm
#Authors: MasterNode/Network Handler: Vedhas Deshpande
#GPS handler: Pallavi Avle
#Classhandler: Chinmay Admane
#Optimal Algorithm: Ben Rhoades
#Git Repo: https://github.com/vedhasd91/zapatabot.git

#--setup xbee and serial objects
PORT='/dev/ttyUSB0'
BAUD=9600

ser=Serial(PORT,BAUD)
xb = XBee(ser)


#---ZigBee Target Thread Function---
def networkhandler(name, delay, counter):
	while counter:
		#To-DO ZigBee stuff
		time.sleep(delay)
		#print "%s %s "%(name, time.ctime(time.time()))
		xb.tx(dest_addr='\x00\x01',data=name)
		counter-=1
	return 0

def gpshandler(name, delay, counter):
	while counter:
		#To-Do GPS stuff
		time.sleep(delay)
		print "%s %s "%(name, time.ctime(time.time()))
		counter-=1
	return 0

def classhandler():
	#To Do classification stuff here
	return 0

if __name__ == "__main__":
	print ">>>>>>>>>>MASTER NODE<<<<<<<<<<"
	thread1 = threading.Thread(target=networkhandler,args=("ZigBee Thread",1,10))
	#thread1.start()
	thread2 = threading.Thread(target=gpshandler,args=("GPS Thread",2,10))
	#thread2.start()
	while 1:
		#Infrastructure Software control prompt
		uinput=raw_input(">>")
		if uinput=='exit':
			break
		if uinput=='zigbee':
			thread1.start()
	thread1.join()
	#thread2.join()
	print "goodbye... shutting down masternode.."
