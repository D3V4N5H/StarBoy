from config import *

import googlemaps

gmaps=googlemaps.Client(key= Google_GeoLocation_API_Key)

print(gmaps.geolocate())
