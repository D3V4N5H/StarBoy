#Graph
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
    @staticmethod
    def createNodes(tx, word, nextWord):
        result = tx.run('''
            MERGE (lx:lyrics{word:$word})
                ON CREATE SET lx.count = 1
                ON MATCH SET lx.count = lx.count + 1
            MERGE (mx:lyrics{word:$nextWord})
                ON CREATE SET mx.count = 1
                ON MATCH SET mx.count = mx.count + 1
            MERGE (lx)-[r:next]->(mx)
                ON CREATE SET r.count = 1
                ON MATCH SET r.count = r.count +1
            RETURN $word, $nextWord''', word=word, nextWord=nextWord)
        return result

    
graph = Graph(uri, user, password)
graph.clearGraph()

#API Helper
import json, requests
def callAPI(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + apikey ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)


def getLyrics(trackName, artistName):
	method = "matcher.lyrics.get"
	title = "&q_track="
	artist = "&q_artist="
	_title= encode(trackName)
	_artist = encode(artistName)
	parameters = title + _title + artist + _artist
	return callAPI(method,parameters)


#Fetching List Of Top Tracks
from urllib.parse import quote as encode
from dateutil.parser import parse

def parseAndReadable(weirdDateAndTime):
    dateTimeObject = parse(weirdDateAndTime)
    return dateTimeObject.date().strftime("%d %B, %Y (%A)")

method = "chart.tracks.get"
parameters = "?format=jsonp&callback=callback&country=in"
topTracksIndiaData = callAPI(method,parameters)
listOfTracks = {}
for trackDictionary in topTracksIndiaData["message"]["body"]["track_list"]:
    for dictionary in trackDictionary.items():
        lyrics = getLyrics(dictionary[1]["track_name"], dictionary[1]["artist_name"])
        listOfTracks[ dictionary[1]["track_name"]] = \
        {
            "track_id": dictionary[1]["track_id"],
            "first_release_date": parseAndReadable(dictionary[1]["first_release_date"]),
            "artist_name": dictionary[1]["track_name"],
            "lyrics": lyrics["message"]["body"]["lyrics"]["lyrics_body"]
        }


#Import Each Song
def createNodes(word, nextWord):
        with graph._driver.session() as session:
            greeting = session.write_transaction(graph.createNodes, word, nextWord)
            print(greeting)


def getLyricsFromTrackID(track_id):
	method = "track.lyrics.get"
	parameters = "&track_id=" + str(track_id)
	return callAPI(method, parameters)

allTracksLyricsForGraph={}
for trackDictionary in topTracksIndiaData["message"]["body"]["track_list"]:
    for dictionary in trackDictionary.items():
        allTracksLyricsForGraph[dictionary[1]["track_id"]] = getLyricsFromTrackID(dictionary[1]["track_id"])

addSongNameAsLabel='''
	MATCH (n:lyrics)
	call apoc.create.addLabels([id(n)],[$songName]) YIELD node
	RETURN node
	'''
removeLyricsLabel='''
	MATCH (n:lyrics)
	call apoc.create.removeLabels([id(n)],['lyrics']) YIELD node
	RETURN node
	'''


for key in allTracksLyricsForGraph:
	data = allTracksLyricsForGraph[key]["message"]["body"]["lyrics"]["lyrics_body"]
	lyrics, disclaimer = data.split("...\n\n*******")
	while "(" in lyrics and ")" in lyrics:
		before, rest = lyrics.split("(",maxsplit=1)
		inside, after = rest.split(")",maxsplit=1)
		lyrics = before + after
	lyrics=lyrics.replace("\n\n","\n")
	lyrics=lyrics.replace("\n"," ")
	lyrics=lyrics.replace(",","")
	lyrics=lyrics.replace("!","")
	words=lyrics.split()
	for name, values in listOfTracks.items():
		if values["track_id"] == key:
			songName = name
	for i in range(len(words)-1):
		createNodes(words[i], words[i+1])
	with graph._driver.session() as session:
		session.run(addSongNameAsLabel,songName=songName)
	with graph._driver.session() as session:
		session.run(removeLyricsLabel)
	
