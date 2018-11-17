from config import *
import json, requests
def call_API(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + MxM_API_key ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)
