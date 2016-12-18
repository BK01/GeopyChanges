from geopy.geocoders import Photon
from geopy.location import Location
from geopy.distance import (vincenty, EARTH_RADIUS, Distance)

import math
import types
import time

import unittest

class PhotonTestCases(unittest.TestCase):

	def setUp(self):
		self.address = "Sunnersta" #static address to be found

		self.userlocation = (59.8585107,17.6368508)

		self.addrNone = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba" #non-existing address
		self.scheme = "https"
		self.plainscheme = "http"
		self.geolocators = []

		#set up for Photon
		self.geolocator10 = Photon()
		self.photondomain = "photon.komoot.de"
		self.photonapi = "https://photon.komoot.de/api"
		self.geolocators.append(self.geolocator10)

	def testPhoton(self):
		#assert if the object's structure is the same as class Photon
		self.assertIsInstance(self.geolocator10, Photon, "The object is not an instance of class Photon")

		#assert the url built
		self.assertEqual(self.geolocator10.scheme, self.scheme)
		self.assertEqual(self.geolocator10.api, self.photonapi)		
		self.assertEqual(self.geolocator10.domain, self.photondomain)
		
	def testDataTypeNone(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.addrNone)
			self.assertIsNone(location, "location found! " + str(gl) + " " + str(self.geolocators[gl]))
			
	def testDataTypeSingle(self):		
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address)
			
			self.assertIsNotNone(location, "location not found! " + str(gl))
			self.assertIsInstance(location, Location, "location is not an instance of class Location! " + str(gl))
			self.assertIsNot(type(location), list, "location is multiple! " + str(gl))
			self.assertIs(type(location), Location, "location is not of type Location! " + str(gl))
			self.assertIs(type(location.address), unicode, "address is not of type unicode! " + str(gl) + " " + str(self.geolocators[gl]))
			self.assertIs(type(location.latitude), float, "latitude is not of type float! " + str(gl))
			self.assertIs(type(location.longitude), float, "longitude is not of type float! " + str(gl))
			self.assertIs(type(location.altitude), float, "altitude is not of type float! " + str(gl))
			self.assertIs(type(location.raw), dict, "raw is not of type dict! " + str(gl))
			#print(location)
	
	def testDataTypeMultiple(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address, exactly_one=False)
				
			self.assertIsNotNone(location, "location not found! " + str(gl))
			self.assertIs(type(location), list, "location is single! " + str(gl))
			for l in range(len(location)):
				self.assertIsInstance(location[l], Location, "location is not an instance of class Location! " + str(gl))
				self.assertIs(type(location[l]), Location, "location is not of type Location! " + str(gl))
				self.assertIs(type(location[l].address), unicode, "address is not of type unicode! " + str(gl) + " " + str(self.geolocators[gl]))
				self.assertIs(type(location[l].latitude), float, "latitude is not of type float! " + str(gl))
				self.assertIs(type(location[l].longitude), float, "longitude is not of type float! " + str(gl))
				self.assertIs(type(location[l].altitude), float, "altitude is not of type float! " + str(gl))
				self.assertIs(type(location[l].raw), dict, "raw is not of type dict! " + str(gl))
				#print(location[l])
			
	def testAddressSingle(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address)			
			self.assertIn(self.address,location.raw['properties']['name'])

	def testAddressMultiple(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address,exactly_one=False)	
			for gl1 in range(len(location)):
				if self.address in location[gl1].raw['properties']['name']:
					self.assertIn(self.address,location[gl1].raw['properties']['name'])	
			
	def testAddressSingleChanges(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=True)			
			self.assertIn(self.address,location.raw['properties']['name'])

	def testAddressMultipleChanges(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=False)	
			for gl1 in range(len(location)):
				if self.address in location[gl1].raw['properties']['name']:
					self.assertIn(self.address,location[gl1].raw['properties']['name'])		
						
	def testOrderedData(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=False)	

			#put all distance in array
			distance = []
			for l in range(len(location)):
				distance.append(vincenty(self.userlocation,(location[l].latitude,location[l].longitude)))
			
			#compare all distance with the first distance, the first one should be the smallest
			min_distance = distance[0]
			for l in range(len(distance)):
				self.assertLessEqual(min_distance, distance[l], "The order of data is wrong")

if __name__ == '__main__':
	unittest.main()