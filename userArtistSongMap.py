import configparser
config = configparser.ConfigParser()
config.read('config.txt')
apikey=config['MusixMatch']['API_key']

import json
import requests
from dateutil.parser import parse
from urllib.parse import quote as encode

from neo4j import GraphDatabase
uri = config['Neo4j']['Bolt_URI']
user = config['Neo4j']['User']
password = config['Neo4j']['Password']

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


def callAPI(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + apikey ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)


method = "chart.artists.get"
parameters= "&country=in"
topArtistsIndiaData = callAPI(method, parameters)
# topArtistsIndiaData["message"]["body"]["artist_list"][i]["artist"]["artist_name"]
listOfArtists=[]
for i in range(len(topArtistsIndiaData["message"]["body"]["artist_list"])):
    listOfArtists.append(topArtistsIndiaData["message"]["body"]["artist_list"][i]["artist"]["artist_name"])


def parseAndReadable(weirdDateAndTime):
    dateTimeObject = parse(weirdDateAndTime)
    return dateTimeObject.date().strftime("%d %B, %Y (%A)")


method="chart.tracks.get"
parameters = "?format=jsonp&callback=callback&country=in"
topTracksIndiaData = callAPI(method,parameters)
listOfTracks={}
for trackDictionary in topTracksIndiaData["message"]["body"]["track_list"]:
    for dictionary in trackDictionary.items():
        title = "&q_track="
        artist = "&q_artist="
        _title= encode(dictionary[1]["track_name"])
        _artist = encode(dictionary[1]["artist_name"])
        parameters = title + _title + artist + _artist
        method="matcher.lyrics.get"
        lyrics = callAPI(method,parameters)
        listOfTracks[ dictionary[1]["track_name"]] = \
        {
            "track_id": dictionary[1]["track_id"],
            "first_release_date": parseAndReadable(dictionary[1]["first_release_date"]),
            "artist_name": dictionary[1]["track_name"],
            "lyrics": lyrics["message"]["body"]["lyrics"]["lyrics_body"]
        }
#track_id = 86487954


for track_name, trackInfo in listOfTracks.items():
    print("\nTrack:", track_name)
    
    for key in trackInfo:
        print(key + ':', trackInfo[key])


def getTrackListOfArtist(name):
    method = "track.search"
    parameters = "&q_artist="+name+"&quorum_factor=1&apikey="+apikey
    searchTracksOfArtistData = callAPI(method, parameters)
    songsOfArtist=[]
    for i in range(len(searchTracksOfArtistData["message"]["body"]["track_list"])):
        songsOfArtist.append(searchTracksOfArtistData["message"]["body"]["track_list"][i]["track"]["track_name"])
    return songsOfArtist


for artist in listOfArtists:
    print(artist + ":")
    print()
    count=0
    for song in getTrackListOfArtist(artist):
        count = count + 1
        print( count, end=". " )
        print( song )
    print()
    print()

# genre= searchTracksOfArtistData["message"]["body"]["track_list"][i]["track"]["primary_genres"]["music_genre_list"][0]["music_genre"]["music_genre_name"]
def makeNodesFromAPI(driver, uName, aName, sName):
    with driver.session() as session:
        return session.run('''
        CREATE (u1:USER {name: $uname}),
        (s1:SONG {songName: $sname}),
        (m1:METADATA {data: $aname}),
        (u1)-[:LIKED]->(s1),
        (s1)-[:ARTIST]->(m1)
            ''', uname=uName, aname=aName, sname=sName)

userNameCount=0
for artist in listOfArtists:
    songs=getTrackListOfArtist(artist)
    makeNodesFromAPI(graph._driver, userNameCount, artist, songs[0])
    if userNameCount<10:
        userNameCount+=1

INSERT_LIKED_TRACKS='''
    MERGE (u:User {name: {userName}})
    MERGE (a:Track {track: {songName}})
    CREATE UNIQUE (u)-[:LIKED]->(a)
'''

def insertLikedTracks(userName, songName):
    with graph._driver.session() as session:
        return session.run(INSERT_LIKED_TRACKS, {"userName": userName, "songName": songName})

for track in listOfTracks:
    insertLikedTracks("Indians", track)
