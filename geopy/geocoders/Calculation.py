from geopy.distance import vincenty
def calculations(url,places):
	tempplaces= ""
	tempdistance = []
	for gl in range(len(places)):
		distance = vincenty(url,(places[gl].latitude,places[gl].longitude)).km
		tempdistance.append(distance)

	for i in range(len(tempdistance)-1):
		for j in range(len(tempdistance)-1):
			if tempdistance[j] > tempdistance[j+1]:
				tempplaces = places[j]
				places[j] = places[j+1]
				places[j+1]= tempplaces

	return places
				
