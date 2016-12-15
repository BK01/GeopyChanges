from geopy.geocoders import GoogleV3
from geopy.geocoders import ArcGIS
from geopy.geocoders import Bing
from geopy.geocoders import DataBC
from geopy.geocoders import GeocodeFarm
from geopy.geocoders import GeoNames
from geopy.geocoders import Mapzen
from geopy.geocoders import OpenCage
from geopy.geocoders import OpenMapQuest
from geopy.geocoders import Nominatim
from geopy.geocoders import Photon
from geopy.location import Location
import unittest
import types
import time

class TestWebServices(unittest.TestCase):

	def setUp(self):
		self.address = "Sunnersta"
		self.addrNone = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba"
		self.scheme = "https"
		self.plainscheme = "http"
		self.geolocators = []

		#set up for Google
		self.geolocator1 = GoogleV3()
		self.googleurl = "https://maps.googleapis.com/maps/api/geocode/json"
		self.googledomain = "maps.googleapis.com"
		self.geolocators.append(self.geolocator1)
		
		#set up for ArcGIS
		self.geolocator2auth = ArcGIS("asailona", "uppsala00", "asailona.maps.arcgis.com")
		self.geolocator2 = ArcGIS()
		self.arcgisurl = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find"
		self.arcgisgenerate = "https://www.arcgis.com/sharing/generateToken?username=asailona&password=uppsala00&expiration=3600&f=json&referer=asailona.maps.arcgis.com"
		self.geolocators.append(self.geolocator2auth)
		self.geolocators.append(self.geolocator2)

		#set up for Bing
		self.geolocator3auth = Bing("AjIo4Ums4724tF5U5V7t91SHwwvjm8GP8wf0b3HZmVJWVQLlGJtSwv04IlwJ6971")
		self.bingapikey = "AjIo4Ums4724tF5U5V7t91SHwwvjm8GP8wf0b3HZmVJWVQLlGJtSwv04IlwJ6971"
		self.bingurlapi = "https://dev.virtualearth.net/REST/v1/Locations"
		self.geolocators.append(self.geolocator3auth)
		
		#set up for Data BC
		self.geolocator4 = DataBC()
		self.databcurlapi = "https://apps.gov.bc.ca/pub/geocoder/addresses.geojson"
		self.geolocators.append(self.geolocator4)
		
		#set up for geocodeFarm
		self.geolocator5 = GeocodeFarm()
		self.geourlapi = "https://www.geocode.farm/v3/json/forward/"
		self.geolocators.append(self.geolocator5)
		
		#set up for GeoNames
		self.geolocator6 = GeoNames(None, "asailona")
		self.gnameapi = "http://api.geonames.org/searchJSON"
		self.geolocators.append(self.geolocator6)
		
		#set up for MapZen
		self.geolocator7 = Mapzen("mapzen-yJXCFyc")
		self.mapzenapikey = "mapzen-yJXCFyc"
		self.mapzenapi = "https://search.mapzen.com/v1/search"
		self.geolocators.append(self.geolocator7)
		
		#set up for OpenCage
		self.geolocator8 = OpenCage("1aea82c9f55149dc1acc6ae04be7747c")
		self.openapikey = "1aea82c9f55149dc1acc6ae04be7747c"
		self.opendomain = "api.opencagedata.com"
		self.openapi = "https://api.opencagedata.com/geocode/v1/json"
		self.geolocators.append(self.geolocator8)
		
		#set up for Open Street Map
		self.geolocator9 = Nominatim()
		self.osmdomain = "nominatim.openstreetmap.org"
		self.osmapi = "https://nominatim.openstreetmap.org/search"
		self.geolocators.append(self.geolocator9)

		#set up for Photon
		self.geolocator10 = Photon()
		self.photondomain = "photon.komoot.de"
		self.photonapi = "https://photon.komoot.de/api"
		self.geolocators.append(self.geolocator10)

	def testGoogle(self):
		#assert if the object's structure is the same as class GoogleV3
		self.assertIsInstance(self.geolocator1, GoogleV3, "The object is not an instance of class GoogleV3")
		
		#assert the url built
		self.assertEqual(self.geolocator1.scheme, self.scheme)
		self.assertEqual(self.geolocator1.domain, self.googledomain)
		self.assertEqual(self.geolocator1.api, self.googleurl)

	def testArcGIS(self):
		#assert if the object's structure is the same as class ArcGIS
		self.assertIsInstance(self.geolocator2, ArcGIS, "The object is not an instance of class ArcGIS")

		#assert the url built
		self.assertEqual(self.geolocator2.scheme, self.scheme)
		self.assertEqual(self.geolocator2.api, self.arcgisurl)

		#assert if the authenticated mode is used
		var = self.geolocator2auth._refresh_authentication_token()
		var2 = self.geolocator2auth._base_call_geocoder(self.arcgisgenerate)
		self.geolocator2auth.token = var2['token']
		self.assertIsNotNone(self.geolocator2auth.token, "The token is None")

	def testBing(self):
		#assert if the object's structure is the same as class Bing
		self.assertIsInstance(self.geolocator3auth, Bing, "The object is not an instance of class Bing")

		#assert the url built
		self.assertEqual(self.geolocator3auth.scheme, self.scheme)
		self.assertEqual(self.geolocator3auth.api, self.bingurlapi)
		self.assertEqual(self.geolocator3auth.api_key, self.bingapikey)

	def testDataBC(self):
		#assert if the object's structure is the same as class Data BC
		self.assertIsInstance(self.geolocator4, DataBC, "The object is not an instance of class Data BC")

		#assert the url built
		self.assertEqual(self.geolocator4.scheme, self.scheme)
		self.assertEqual(self.geolocator4.api, self.databcurlapi)

	def testGeocodeFarm(self):
		#assert if the object's structure is the same as class Geocode Farm
		self.assertIsInstance(self.geolocator5, GeocodeFarm, "The object is not an instance of class Geocode Farm")

		#assert the url built
		self.assertEqual(self.geolocator5.scheme, self.scheme)
		self.assertEqual(self.geolocator5.api, self.geourlapi)

	def testGeoNames(self):
		#assert if the object's structure is the same as class GeoNames
		self.assertIsInstance(self.geolocator6, GeoNames, "The object is not an instance of class GeoNames")

		#assert the url built
		self.assertEqual(self.geolocator6.scheme, self.plainscheme)
		self.assertEqual(self.geolocator6.api, self.gnameapi)

	def testMapzen(self):
		#assert if the object's structure is the same as class Mapzen
		self.assertIsInstance(self.geolocator7, Mapzen, "The object is not an instance of class Mapzen")

		#assert the url built
		self.assertEqual(self.geolocator7.geocode_api, self.mapzenapi)
		self.assertEqual(self.geolocator7.api_key, self.mapzenapikey)

	def testOpenCage(self):
		#assert if the object's structure is the same as class OpenCage
		self.assertIsInstance(self.geolocator8, OpenCage, "The object is not an instance of class OpenCage")

		#assert the url built
		self.assertEqual(self.geolocator8.scheme, self.scheme)
		self.assertEqual(self.geolocator8.api, self.openapi)		
		self.assertEqual(self.geolocator8.api_key, self.openapikey)
		self.assertEqual(self.geolocator8.domain, self.opendomain)

	def testNominatim(self):
		#assert if the object's structure is the same as class Open Street Map
		self.assertIsInstance(self.geolocator9, Nominatim, "The object is not an instance of class Open Street Map")

		#assert the url built
		self.assertEqual(self.geolocator9.scheme, self.scheme)
		self.assertEqual(self.geolocator9.api, self.osmapi)		
		self.assertEqual(self.geolocator9.domain, self.osmdomain)

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
	    	if (type(self.geolocators[gl]) == DataBC):
	    		location = self.geolocators[gl].geocode(self.address, 25, 0, "any", False, None)
	    	elif (type(self.geolocators[gl]) == OpenCage):
	    		location = self.geolocators[gl].geocode(self.address, None, None, None, False)
	    	else:
	        	location = self.geolocators[gl].geocode(self.address, False)
	        	
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
			if gl in (0,5):
				self.assertIn(self.address,location.raw['formatted_address'])
			elif gl == 3:
				self.assertIn(self.address,location.raw['address']['formattedAddress'])
			elif gl == 6:
				self.assertIn(self.address,location.raw['name'])
			elif gl == 7:
				self.assertIn(self.address,location.raw['properties']['label'])
			elif gl == 8:
				self.assertIn(self.address,location.raw['formatted'])
			elif gl == 9:
				self.assertIn(self.address,location.raw['display_name'])
			elif gl == 10:
				self.assertIn(self.address,location.raw['properties']['name'])

	def testAddressMultiple(self):
		for gl in range(len(self.geolocators)):
			#print self.geolocators[gl]
			time.sleep(2)
			location = self.geolocators[gl].geocode(self.address,exactly_one=False)	
			if gl in (0,5):
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['formatted_address'])
			elif gl == 3:
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['address']['formattedAddress'])
			elif gl == 6:
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['name'])
			elif gl == 7:
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['properties']['label'])
			elif gl == 8:
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['formatted'])
			elif gl == 9:
				for gl1 in range(len(location)):
					self.assertIn(self.address,location[gl1].raw['display_name'])
			elif gl == 10:
				for gl1 in range(len(location)):
					if self.address in location[gl1].raw['properties']['name']:
						self.assertIn(self.address,location[gl1].raw['properties']['name'])

if __name__ == '__main__':
	unittest.main()