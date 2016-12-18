from geopy.geocoders import DataBC
from geopy.location import Location
from geopy.distance import (vincenty, EARTH_RADIUS, Distance)

import math
import types
import time

import unittest

class GeopyTestCases(unittest.TestCase):

	def setUp(self):
		self.address2 = "Mackenzie" #static address for DataBC only
		
		self.userlocation = (59.8585107,17.6368508)

		self.addrNone = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba" #non-existing address
		self.scheme = "https"
		self.plainscheme = "http"
		self.geolocators = []
		
		#set up for Data BC
		self.geolocator4 = DataBC()
		self.databcurlapi = "https://apps.gov.bc.ca/pub/geocoder/addresses.geojson"
		self.geolocators.append(self.geolocator4)

	def testDataBC(self):
		#assert if the object's structure is the same as class Data BC
		self.assertIsInstance(self.geolocator4, DataBC, "The object is not an instance of class Data BC")

		#assert the url built
		self.assertEqual(self.geolocator4.scheme, self.scheme)
		self.assertEqual(self.geolocator4.api, self.databcurlapi)

	def testDataTypeNone(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.addrNone)
			self.assertIsNone(location, "location found! " + str(gl) + " " + str(self.geolocators[gl]))
			
	def testDataTypeSingle(self):		
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address2)
			
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
			location = self.geolocators[gl].geocode(self.address2, location_descriptor="any", exactly_one=False)
				
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
			location = self.geolocators[gl].geocode(self.address2)	
			self.assertIn(self.address2,location.raw['fullAddress'])
			
	def testAddressMultiple(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address2,exactly_one=False)	
			for gl1 in range(len(location)):
				if self.address2 in location[gl1].raw['fullAddress']:
					self.assertIn(self.address2,location[gl1].raw['fullAddress'])
			
	def testAddressSingleChanges(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address2,self.userlocation,exactly_one=True)	
			self.assertIn(self.address2,location.raw['fullAddress'])
			
	def testAddressMultipleChanges(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address2,self.userlocation,exactly_one=False)	
			for gl1 in range(len(location)):
				if self.address2 in location[gl1].raw['fullAddress']:
					self.assertIn(self.address2,location[gl1].raw['fullAddress'])
	
	def testOrderedData(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address2,self.userlocation,exactly_one=False)	
			
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