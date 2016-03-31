#!/usr/bin/python
import time
import threading
from xbee import ZigBee
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

NetworkInfo = {}
accessList = threading.Lock()
DeviceList = list()

ser=Serial(PORT,BAUD)

def msg_pack(data):
	if "parameter" in data.keys():
        	DeviceList.append(data['parameter']['source_addr_long'])
		print "device added to list...."
		print DeviceList
	elif data['id']=="rx":
		rx_data = data['rf_data']
		print rx_data
	return 0

zb = ZigBee(ser,callback=msg_pack)

#---Zigbee Node ping----------
print "Performing network reset...Wait for 10 secs"
zb.at(command="NR",parameter="1")
time.sleep(10)
print "Acquiring Node addresses... wait for number of nodes to show up"
zb.at(command="ND")

#---ZigBee Target Thread Function---
def networkhandler(name, delay, counter):
	while counter:
		#print "%s %s "%(name, time.ctime(time.time()))
		for device in DeviceList:
			zb.tx(dest_addr_long=device,dest_addr='\xFF\xFE',data="LOC")
			time.sleep(1)
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
	thread1 = threading.Thread(target=networkhandler,args=("ZigBee Thread",3,3))
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
	#pingthread.join()
	#thread2.join()
	#zb.at(command="NR",parameter="1")
	#print "Shutting down..resetting network"
	#time.sleep(10)
	#zb.at(command="FR")
	#print "Performing software reset of co-ordinator"
	#time.sleep(5)
	ser.close()
	print "goodbye... shutting down masternode.."
