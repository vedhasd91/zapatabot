#!/usr/bin/python
import time
import threading
import struct
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
DeviceList = list()
rx_data=""
execFlag = 0
nodecount = 0
DEBUG = 0

ser=Serial(PORT,BAUD)

def msg_pack(data):
	if "parameter" in data.keys():
		if data['parameter']['source_addr_long'] not in DeviceList:
			DeviceList.append(data['parameter']['source_addr_long'])
			print "device added to list...."
			print DeviceList
	elif data['id']=="rx":
		rx_data = data['rf_data']
		NetworkInfo[data['source_addr_long']].insert(2,rx_data)
		print NetworkInfo[data['source_addr_long']][0] + " sent to co-ordinator: " + NetworkInfo[data['source_addr_long']][2]
	elif DEBUG:
		print data
	return 0

zb = ZigBee(ser,callback=msg_pack)

#---Zigbee Node ping----------
print "Acquiring Node addresses..."
zb.at(command="ND")

#---ZigBee Target Thread Function---
def networkhandler(name, delay, cmd, nodecount):
	while not execFlag:
		#print "%s %s "%(name, time.ctime(time.time()))
		for device in DeviceList:
			if str(device) not in NetworkInfo.keys():
				NetworkInfo[str(device)] = ['RSU'+str(nodecount),device]
				nodecount+=1
				print NetworkInfo[device][0] + " is " + str([device])
			else:	
				zb.tx(dest_addr_long=NetworkInfo[device][1],dest_addr='\xFF\xFE',data=cmd)
				time.sleep(3)
	return 0

if __name__ == "__main__":
	print ">>>>>>>>>>MASTER NODE<<<<<<<<<<"
	thread1 = threading.Thread(target=networkhandler,args=("ZTh",3,"LOC",nodecount))
	while 1:
		#Infrastructure Software control prompt
		uinput=raw_input(">>")
		if uinput=='exit':
			execFlag = 1
			break
		if uinput=='zigbee init':
			thread1.start()
		if uinput=='ls':
			print NetworkInfo
	if execFlag:
		thread1.join()
	ser.close()
	print "goodbye... shutting down masternode.."




