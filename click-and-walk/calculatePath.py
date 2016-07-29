#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import urllib2
import json
import time

cur = [-81.2879310,43.0167200]

def calculatePath(cur,des,speed,f):
	print('calculating path:',cur,des,speed,f)
	distance = calculateDistance(cur,des)
	unitVec = [(des[0]-cur[0])/distance, (des[1] - cur[1])/distance]
	nextPoint = cur
	path = []
	x = speed/f * unitVec[0]
	y = speed/f * unitVec[1]
	while calculateDistance(nextPoint,des) > speed/f:
		nextPoint = [nextPoint[0] + x, nextPoint[1] + y]
		path.append(nextPoint)
	path.append(des)
	return path


def calculateDistance(cur,des):
	distance = ((des[0] - cur[0])**2 + (des[1] - cur[1])**2)**0.5
	return distance

import xml.etree.cElementTree as ET
import urllib2
import json

lastLat = ""
lastLng = ""

def getTargetLocation():
	response = urllib2.urlopen("https://london-pokemap.herokuapp.com/clicked_location", timeout = 5)
	r = json.load(response)
	#print('GET: new location',r)
	return r

def generateXML(geo):
	gpx = ET.Element("gpx", version="1.1", creator="Xcode")
	wpt = ET.SubElement(gpx, "wpt", lat=geo[1], lon=geo[0])
	ET.SubElement(wpt, "name").text = "PokemonLocation"
	ET.ElementTree(gpx).write("pokemonLocation.gpx")
	print("Location Updated!", "latitude:", geo[1], "longitude:" ,geo[0])


def main():
	global cur
	while True:
		des = getTargetLocation()
		kmH = 600
		realSpeed = kmH/3.6      #m/s 	 #9km/h
		speed = 0.0020/250*realSpeed		#0.0020/250*2.5
		f = 10
		path = calculatePath(cur,des,speed,f)
		stepLeft = len(path)
		for i in path:
			#print('des:',des)
			#print('cur',cur)
			newDes = getTargetLocation()
			if newDes != des:
				break


			cur = list(i) 	#set current to current point in the path
			#print(i)
			print('step left:', stepLeft)
			i[0] = str(i[0])
			i[1] = str(i[1])
			generateXML(i)
			sleepPeriod = float(float(1)/float(f))
			print('sleeping ' + str(sleepPeriod) + ' seconds')
			time.sleep(sleepPeriod)
			stepLeft = stepLeft - 1 
		des = [float(des[0]),float(des[1])]
		#cur = list(des)
		#print(cur,des)
		while (abs(cur[0]-des[0]) < 0.000008 and abs(cur[1]-des[1]) < 0.000008):
			des = getTargetLocation()
			des = [float(des[0]),float(des[1])]
			print('waiting for new location')
	


if __name__ == '__main__':
	main()

