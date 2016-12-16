from geopy.distance import vincenty
def calculations(url,places):
	tempdistance = []
	temparray = []
	for gl in range(len(places)):		
		tempdistance.append((vincenty(url,(places[gl].latitude,places[gl].longitude)),places[gl]))
	'''for gl1 in range(len(tempdistance)):
		print tempdistance[gl1]'''
	tempdistance.sort()
	'''print " "
	for gl1 in range(len(tempdistance)):
		print tempdistance[gl1]'''
	for i in range(len(tempdistance)):		
		tempdistance[i] =  tempdistance[i][1]


	#print tempdistance
	#print tempdistance
	return tempdistance
