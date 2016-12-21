from geopy.distance import vincenty
def calculations(url,places):
	tempdistance = []
	temparray = []
	
	#To calculate distance and make the result of distance calculation and address become tuple
	for gl in range(len(places)):
		try:			
			tempdistance.append((vincenty(url,(places[gl].latitude,places[gl].longitude)), places[gl]))
		except ValueError:
			return places # in case vincenty method does not converge
	
	#Sorting the distance from nearest to farthest
	tempdistance.sort()
	
	#to make tempdistance just consist of addresses
	for i in range(len(tempdistance)):		
		tempdistance[i] =  tempdistance[i][1]

	return tempdistance