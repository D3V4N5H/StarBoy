#For API
import json
import requests
from dateutil.parser import parse
from urllib.parse import quote as encode

def callAPI(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + apikey ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)

#For Graph
from neo4j.v1 import GraphDatabase
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

class Graph(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))    
    def close(self):
        self._driver.close()
    @staticmethod
    def clearGraph():
        with graph._driver.session() as session:
            return session.run("MATCH (n)"
                               "DETACH DELETE n")
    
graph = Graph(uri, user, password)
graph.clearGraph()

#Fetching
method = "track.lyrics.get"
parameters = "&track_id=115237681"
StarBoyLyrics = callAPI(method, parameters)

#Mining
for dictionary in StarBoyLyrics.items():
	lyrics, disclaimer = dictionary[1]["body"]["lyrics"]["lyrics_body"].split("...\n\n*******")
	while "(" in lyrics and ")" in lyrics:
		before, rest = lyrics.split("(",maxsplit=1)
		inside, after = rest.split(")",maxsplit=1)
		lyrics = before + after
	words = lyrics.replace("\n","").split(" ")
	lyrics = []
	for word in words:
		word.replace(",","")
		lyrics.append(word)
	print(lyrics)
