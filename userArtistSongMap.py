import requests
import json
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
    def clearGraph(driver):
        with driver.session() as session:
            return session.run("MATCH (n)"
                               "DETACH DELETE n")
    
def makeNodesFromAPI(driver, uName, aName, sName):
    with driver.session() as session:
        return session.run('''
        CREATE (u1:USER {name: $uname}),
        (s1:SONG {songName: $sname}),
        (m1:METADATA {data: $aname}),
        (u1)-[:LIKED]->(s1),
        (s1)-[:ARTIST]->(m1)
            ''', uname=uName, aname=aName, sname=sName)

graph = Graph(uri, user, password)
graph.clearGraph(graph._driver)


def callAPI(url):
    response = requests.get( url + "&apikey=" +apikey ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)


topArtistsIndiaURL = "https://api.musixmatch.com/ws/1.1/chart.artists.get?format=jsonp&callback=callback&country=in"
topArtistsIndiaData = callAPI(topTracksIndiaURL)
# topArtistsIndiaData["message"]["body"]["artist_list"][i]["artist"]["artist_name"]
listOfArtists=[]
for i in range(len(topArtistsIndiaData["message"]["body"]["artist_list"])):
    listOfArtists.append(topArtistsIndiaData["message"]["body"]["artist_list"][i]["artist"]["artist_name"])


topTracksIndiaURL = "https://api.musixmatch.com/ws/1.1/chart.tracks.get?format=jsonp&callback=callback&country=in"
topTracksIndiaData = callAPI(topTracksIndiaURL)
listOfTracks=[]
for i in range(len(topTracksIndiaData["message"]["body"]["track_list"])):
    listOfTracks.append(topTracksIndiaData["message"]["body"]["track_list"][i]["track"]["track_name"])


def getTrackListOfArtist(name):
    searchTracksOfArtistURL = "https://api.musixmatch.com/ws/1.1/track.search?format=jsonp&callback=callback&q_artist="+name+"&quorum_factor=1&apikey="+apikey
    searchTracksOfArtistData = callAPI(searchTracksOfArtistURL)
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
userNameCount=0
for artist in listOfArtists:
    songs=getTrackListOfArtist(artist)
    makeNodesFromAPI(graph._driver, userNameCount, artist, songs[0])
    if userNameCount<10:
        userNameCount+=1
