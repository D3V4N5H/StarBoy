import requests
import json
url = "https://api.musixmatch.com/ws/1.1/chart.artists.get?format=jsonp&callback=callback&country=us&apikey="+apikey
r=requests.get(url)
stringWithoutCallbackHead=r.text.replace( "callback(" , "")
stringWtihoutCallbackHeadAndTail=stringWithoutCallbackHead.replace( ");" , "" )
data=json.loads(stringWtihoutCallbackHeadAndTail)
print( json.dumps( data, sort_keys=True, indent=1 ) )

for artist in data["message"]["body"]["artist_list"]:
	print(artist["artist"]["artist_name"])
