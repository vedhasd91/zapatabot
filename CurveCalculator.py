#!/usr/bin/python
    
import math
diameterOfEarthMeters = 6371.0 * 2 * 1000


def degreeToRadian (degree):
    return (degree * (math.pi) / 180)
    
def radianToDegree (radian) :
    return (radian * 180 / (math.pi))


def CoordinatesToAngle (latitude1, longitude1, latitude2, longitude2):
	longitudeDifferenceRadians = degreeToRadian(longitude2 - longitude1)
	latitude1Radian = degreeToRadian(latitude1)
	latitude2Radian = degreeToRadian(latitude2)
	

	a = math.cos(latitude1Radian)
	b = math.sin(latitude2Radian)
	c = math.sin(latitude1Radian)
	d = math.cos(latitude2Radian)
	e = math.cos(longitudeDifferenceRadians)
	f = math.sin(longitudeDifferenceRadians) 
	
	finx = (a * b) - c * d * e
	
	finy = f * d
	#print finy
	#print finx
	
	finz = radianToDegree(math.atan2 (finy,finx))
	#print finz
	if finz<0:
		finz = 180-abs(finz)
		return finz
	else:
		return finz
	
	
	
	
	
	
def CoordinatesToMeters (latitude1, longitude1, latitude2, longitude2):
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

	
#angle = CoordinatesToAngle (35.308586, -80.742317, 35.308792, -80.741898)

#if (angle < 0):
#    angle = 180 - abs(angle)
#    print "curve angle is:", angle
   
#else:
#    print "curve angle is:", angle

def CurveCat(angle):
	if (38.0000000000 <= angle <= 62.0000000000):
    		print "curve is of degree 6"
		return 6

	elif (62.0000000000 < angle <= 85.0000000000):
    		print "curve is of degree 5"
		return 5

	elif (85.0000000000 < angle <= 109.0000000000):
    		print "curve is of degree 4"
		return 4

	elif (109.0000000000 < angle <= 133.0000000000):
    		print "curve is of degree 3"
		return 3
	
	elif (133.0000000000 < angle <= 157.0000000000):
    		print "curve is of degree 2"
		return 2

	elif (157.0000000000 < angle <= 180.0000000000):
    		print "curve is of degree 1"
		return 1
	else:
		return 0
   
   
#distance_mtr= CoordinatesToMeters(35.308586, -80.742317, 35.308792, -80.741898)
#print "distance in meters between two nodes is:", distance_mtr



