from config import *
import requests, json

url = MxM_Base_URL + "chart.artists.get?format=jsonp&callback=callback&country=us&apikey="+MxM_API_key
response=requests.get(url)
stringWithoutCallbackHead=response.text.replace( "callback(" , "")
stringWtihoutCallbackHeadAndTail=stringWithoutCallbackHead.replace( ");" , "" )
data=json.loads(stringWtihoutCallbackHeadAndTail)
# print( json.dumps( data, sort_keys=True, indent=1 ) )

for artist in data["message"]["body"]["artist_list"]:
	print(artist["artist"]["artist_name"])
