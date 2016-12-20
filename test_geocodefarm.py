from geopy.geocoders import GeocodeFarm
from geopy.location import Location
from geopy.distance import (vincenty, Distance)

import unittest

import time

class GeocodeFarmTestCases(unittest.TestCase):

    def setUp(self):
        self.address = "Sunnersta" #static address to be found

        self.address2 = "Mackenzie" #static address for DataBC only
        
        self.userlocation = (59.8585107,17.6368508)

        self.addrNone = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba" #non-existing address
        self.scheme = "https"
        self.plainscheme = "http"

        #set up for geocodeFarm
        self.geolocator5 = GeocodeFarm()
        self.geourlapi = "https://www.geocode.farm/v3/json/forward/"

    def testGeocodeFarm(self):
        #assert if the object's structure is the same as class Geocode Farm
        self.assertIsInstance(self.geolocator5, GeocodeFarm, "The object is not an instance of class Geocode Farm")

        #assert the url built
        self.assertEqual(self.geolocator5.scheme, self.scheme)
        self.assertEqual(self.geolocator5.api, self.geourlapi)
        
    def testDataTypeNone(self):
        #time.sleep(2)
        #without userlocation
        location = self.geolocator5.geocode(self.addrNone)
        self.assertIsNone(location, "location found! " + str(self.geolocator5))

        #with userlocation
        location = self.geolocator5.geocode(self.addrNone, self.userlocation)
        #print(location)
        #print(location.latitude)
        self.assertIsNone(location, "location found! " + str(self.geolocator5))

    def testDataTypeSingle(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address)
        
        self.assertIsNotNone(location, "location not found! ")
        self.assertIsInstance(location, Location, "location is not an instance of class Location! ")
        self.assertIsNot(type(location), list, "location is multiple! ")
        self.assertIs(type(location), Location, "location is not of type Location! ")
        self.assertIs(type(location.address), unicode, "address is not of type unicode! ")
        self.assertIs(type(location.latitude), float, "latitude is not of type float! ")
        self.assertIs(type(location.longitude), float, "longitude is not of type float! ")
        self.assertIs(type(location.altitude), float, "altitude is not of type float! ")
        self.assertIs(type(location.raw), dict, "raw is not of type dict! ")
        #print(location)
    
    def testDataTypeMultiple(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address, False)
            
        self.assertIsNotNone(location, "location not found! ")
        self.assertIs(type(location), list, "location is single! ")
        for l in range(len(location)):
            self.assertIsInstance(location[l], Location, "location is not an instance of class Location! ")
            self.assertIs(type(location[l]), Location, "location is not of type Location! ")
            self.assertIs(type(location[l].address), unicode, "address is not of type unicode! ")
            self.assertIs(type(location[l].latitude), float, "latitude is not of type float! ")
            self.assertIs(type(location[l].longitude), float, "longitude is not of type float! ")
            self.assertIs(type(location[l].altitude), float, "altitude is not of type float! ")
            self.assertIs(type(location[l].raw), dict, "raw is not of type dict! ")
            #print(location[l])
            
    def testAddressSingle(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address)
        self.assertIn(self.address,location.raw['formatted_address'])

    def testAddressMultiple(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address,exactly_one=False)
        for gl1 in range(len(location)):
            self.assertIn(self.address,location[gl1].raw['formatted_address']) 
            
    def testAddressSingleChanges(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address,userlocation=self.userlocation,exactly_one=True)            
        self.assertIn(self.address,location.raw['formatted_address'])

    def testAddressMultipleChanges(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address,userlocation=self.userlocation,exactly_one=False)    
        for gl1 in range(len(location)):
            self.assertIn(self.address,location[gl1].raw['formatted_address'])       
    
    def testOrderedData(self):
        #time.sleep(2)
        location = self.geolocator5.geocode(self.address,userlocation=self.userlocation,exactly_one=False)    

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
