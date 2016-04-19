#!/usr/bin/python
import math

diameterOfEarthMeters = 6371.0*2*1000

def degreeToRadian(degree):
    return (degree * math.pi / 180)
    
def radianToDegree(radian):
    return (radian * 180 / (math.pi))
	
def CoordinatesToMeters(latitude1, longitude1, latitude2, longitude2):
	latitude1Radian = degreeToRadian(latitude1)
	longitude1Radian = degreeToRadian(longitude1)
	latitude2Radian = degreeToRadian(latitude2)
	longitude2Radian = degreeToRadian(longitude2)
	
	x = math.sin((latitude2Radian - latitude1Radian) / 2)

	y = math.sin((longitude2Radian - longitude1Radian) / 2)
	
#	a = math.asin(math.sqrt((x * x)
	b = math.cos(latitude1Radian)
	c = math.cos(latitude2Radian)
	d = math.asin(math.sqrt((x * x) + b * c * y * y))
	
	
	dist = diameterOfEarthMeters * d
	#print dist
	return dist


	
def SlopeCalculator (altitude1, altitude2, distance):
	rise = abs(altitude2 - altitude1)
	a = distance * distance
	b = rise * rise
	diff = abs(a - b);
	run = math.sqrt(diff)
	if run !=0:
		slope = (rise/run) * 100
		if altitude2>altitude1:
			return (slope,'u')
		else:
			return (slope,'d')
	
	
	
#distance_mtr = CoordinatesToMeters(35.308586, -80.742317, 35.308792, -80.741898)
#print "distance between two nodes is:", distance_mtr

#slope_val = SlopeCalculator(215.10, 210.40, distance_mtr)
#print "slope is:",slope_val

def SlopeCategory(slope_val):
	if(0.0000000000 <= slope_val <= 20.0000000000):
		#print "slope is of type 1"
		return 1

	if(20.0000000000 < slope_val <= 40.0000000000):
		#print "slope is of type 2"
		return 2

	if(40.0000000000 < slope_val <= 60.0000000000):
		#print "slope type is 3"
		return 3

	if(60.0000000000 < slope_val <= 80.0000000000):
		#print "slope is of type 4"
		return 4

	if(80.0000000000 < slope_val <= 10.0000000000):
		#print "slope is of type 5"
		return 5
	
	return 0

