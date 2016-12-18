from geopy.geocoders import ArcGIS
from geopy.location import Location
from geopy.distance import (vincenty, EARTH_RADIUS, Distance)

import math
import types
import time

import unittest

class ArcGISTestCases(unittest.TestCase):

	def setUp(self):
		self.address = "Sunnersta" #static address to be found

		self.userlocation = (59.8585107,17.6368508)

		self.addrNone = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba" #non-existing address
		self.scheme = "https"
		self.plainscheme = "http"
		self.geolocators = []
		
		#set up for ArcGIS
		self.geolocator2auth = ArcGIS("asailona", "uppsala00", "asailona.maps.arcgis.com")
		self.geolocator2 = ArcGIS()
		self.arcgisurl = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find"
		self.arcgisurlmulti = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
		self.arcgisgenerate = "https://www.arcgis.com/sharing/generateToken?username=asailona&password=uppsala00&expiration=3600&f=json&referer=asailona.maps.arcgis.com"
		self.geolocators.append(self.geolocator2auth)
		self.geolocators.append(self.geolocator2)

	def testArcGIS(self):
		#assert if the object's structure is the same as class ArcGIS
		self.assertIsInstance(self.geolocator2, ArcGIS, "The object is not an instance of class ArcGIS")

		#assert the url built
		self.assertEqual(self.geolocator2.scheme, self.scheme)
		self.assertEqual(self.geolocator2.api, self.arcgisurl)
		self.assertEqual(self.geolocator2.api_multi, self.arcgisurlmulti)

		#assert if the authenticated mode is used
		var = self.geolocator2auth._refresh_authentication_token()
		var2 = self.geolocator2auth._base_call_geocoder(self.arcgisgenerate)
		self.geolocator2auth.token = var2['token']
		self.assertIsNotNone(self.geolocator2auth.token, "The token is None")
		
	def testDataTypeNone(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.addrNone)
			self.assertIsNone(location, "location found! " + web_serv + " " + str(self.geolocators[gl]))
			
	def testDataTypeSingle(self):		
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address)
			self.assertIsNotNone(location, "location not found! " + web_serv)
			self.assertIsInstance(location, Location, "location is not an instance of class Location! " + web_serv)
			self.assertIsNot(type(location), list, "location is multiple! " + web_serv)
			self.assertIs(type(location), Location, "location is not of type Location! " + web_serv)
			self.assertIs(type(location.address), unicode, "address is not of type unicode! " + web_serv + " " + str(self.geolocators[gl]))
			self.assertIs(type(location.latitude), float, "latitude is not of type float! " + web_serv)
			self.assertIs(type(location.longitude), float, "longitude is not of type float! " + web_serv)
			self.assertIs(type(location.altitude), float, "altitude is not of type float! " + web_serv)
			self.assertIs(type(location.raw), dict, "raw is not of type dict! " + web_serv)
			
	def testDataTypeMultiple(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address, False)
				
			self.assertIsNotNone(location, "location not found! " + web_serv)
			self.assertIs(type(location), list, "location is single! " + web_serv)
			for l in range(len(location)):
				self.assertIsInstance(location[l], Location, "location is not an instance of class Location! " + web_serv)
				self.assertIs(type(location[l]), Location, "location is not of type Location! " + web_serv)
				self.assertIs(type(location[l].address), unicode, "address is not of type unicode! " + web_serv + " " + str(self.geolocators[gl]))
				self.assertIs(type(location[l].latitude), float, "latitude is not of type float! " + web_serv)
				self.assertIs(type(location[l].longitude), float, "longitude is not of type float! " + web_serv)
				self.assertIs(type(location[l].altitude), float, "altitude is not of type float! " + web_serv)
				self.assertIs(type(location[l].raw), dict, "raw is not of type dict! " + web_serv)
			
	def testAddressSingle(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)
			
			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'
			
			location = self.geolocators[gl].geocode(self.address)			
			self.assertIn(self.address,location.raw['name'], "address is not the same for " + web_serv + "," + self.address + " != " + location.raw['name'])
			
	def testAddressMultiple(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address,exactly_one=False)	
			for gl1 in range(len(location)):
				self.assertIn(self.address,location[gl1].raw['name'], "address not found " + web_serv)
			
	def testAddressSingleChanges(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=True)			
			self.assertIn(self.address,location.raw['name'], "address not found " + web_serv)
			
	def testAddressMultipleChanges(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=False)	
			for gl1 in range(len(location)):
				self.assertIn(self.address,location[gl1].raw['address'], "address not found " + web_serv)
						
	def testOrderedData(self):
		for gl in range(len(self.geolocators)):
			time.sleep(2)

			#flag for differentiate between authenticated and unauthenticated request
			web_serv = 'not_auth'
			if gl == 0:
				web_serv = 'auth'

			location = self.geolocators[gl].geocode(self.address,self.userlocation,exactly_one=False)	

			#put all distance in array
			distance = []
			for l in range(len(location)):
				distance.append(vincenty(self.userlocation,(location[l].latitude,location[l].longitude)))
			
			#compare all distance with the first distance, the first one should be the smallest
			min_distance = distance[0]
			for l in range(len(distance)):
				self.assertLessEqual(min_distance, distance[l], "The order of data is wrong " + web_serv)

if __name__ == '__main__':
	unittest.main()