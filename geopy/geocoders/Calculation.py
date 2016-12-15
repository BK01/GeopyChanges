from geopy.distance import vincenty
def calculations(url,places):
	tempdistance = []
	temparray = []
	#print places
	for gl in range(len(places)):
		#print gl
		tempdistance.append((vincenty(url,(places[gl].latitude,places[gl].longitude)),places[gl]))
	tempdistance.sort()
	
	for i in range(len(tempdistance)):
		#print tempdistance[i]
		tempdistance[i] =  tempdistance[i][1]


	#print tempdistance
	#print tempdistance
	return tempdistance
				
