#!/usr/bin/python
import time
import threading
import struct
import webbrowser
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

#---setup flags, variables and data structures
NetworkInfo = {}
DeviceList = list()
rx_data=""
execFlag = 0
nodecount = 0
DEBUG = 0
accesslock = threading.Lock()
ser=Serial(PORT,BAUD)

def msg_pack(data):
	if "parameter" in data.keys():
		if data['parameter']['source_addr_long'] not in DeviceList:
			accesslock.acquire()
			DeviceList.append(data['parameter']['source_addr_long'])
			accesslock.release()
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

def plotwaypoints():
	writehtml = open('plot_waypoints_gmaps.html','w')
	message = """
<!DOCTYPE html>
	<html> 
	<head> 
		<meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
  		<title>Google Maps Multiple Markers</title> 
  		<script src="http://maps.google.com/maps/api/js?sensor=false" 
        		type="text/javascript"></script>
	</head> 
	<body>
  		<div id="map" style="width: 1300px; height: 700px;"></div>

  		<script type="text/javascript">
    				var locations = [
      				['RSU0', 35.308380,-80.742462, 1],
      				['RSU2', 35.308739,-80.742218, 2],
				['RSU3', 35.308605,-80.742233, 3],
				['RSU4', 35.308846,-80.742310, 4],	  
    				];

    				var map = new google.maps.Map(document.getElementById('map'), {
      					zoom: 15,
      					center: new google.maps.LatLng(35.308792, -80.741898),
      					mapTypeId: google.maps.MapTypeId.ROADMAP
    				});

    				var infowindow = new google.maps.InfoWindow();

    				var marker, i;

    				for (i = 0; i < locations.length; i++) {  
      					marker = new google.maps.Marker({
        					position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        					map: map
      					});

      					google.maps.event.addListener(marker, 'click', (function(marker, i) {
        					return function() {
          					infowindow.setContent(locations[i][0]);
          					infowindow.open(map, marker);
        					}
      					})(marker, i));
    				}
  		</script>
	</body>
	</html> """
	writehtml.write(message)
	writehtml.close()
	filename = 'plot_waypoints_gmaps.html'
	webbrowser.open(filename,new=0)
	return 0


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
				time.sleep(1)
		time.sleep(1)
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
		if uinput=='plot':
			plotwaypoints()
	if execFlag:
		thread1.join()
	ser.close()
	print "goodbye... shutting down masternode.."




