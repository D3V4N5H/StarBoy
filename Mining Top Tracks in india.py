
from neo4j.v1 import GraphDatabase
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

add_Song_Name_As_Label='''
	MATCH (n:lyrics)
	call apoc.create.addLabels([id(n)],[$song_Name]) YIELD node
	RETURN node
	'''
remove_Lyrics_Label='''
	MATCH (n:lyrics)
	call apoc.create.removeLabels([id(n)],['lyrics']) YIELD node
	RETURN node
	'''

class Graph(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))    
    def close(self):
        self._driver.close()
    @staticmethod
    def clear_Graph():
        with graph._driver.session() as session:
            return session.run("MATCH (n)"
                               "DETACH DELETE n")
    @staticmethod
    def create_Nodes(tx, word, next_Word):
        result = tx.run('''
            MERGE (lx:lyrics{word:$word})
            	ON CREATE SET lx.word = $word
                ON CREATE SET lx.count = 1
                ON MATCH SET lx.count = lx.count + 1
            MERGE (mx:lyrics{word:$next_Word})
                ON CREATE SET mx.word = $word
                ON CREATE SET mx.count = 1
                ON MATCH SET mx.count = mx.count + 1
            MERGE (lx)-[r:next]->(mx)
                ON CREATE SET r.count = 1
                ON MATCH SET r.count = r.count +1
            RETURN $word, $next_Word''', word=word, next_Word=next_Word)
        return result

import json, requests
def call_API(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + api_key ).text
    callback_To_Json = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callback_To_Json)

def get_Lyrics(track_Name, artist_Name):
	method = "matcher.lyrics.get"
	title = "&q_track="
	artist = "&q_artist="
	_title= encode(track_Name)
	_artist = encode(artist_Name)
	parameters = title + _title + artist + _artist
	return call_API(method,parameters)

from urllib.parse import quote as encode
from dateutil.parser import parse

def parse_And_Readable(weird_Date_And_Time):
    date_Time_Object = parse(weird_Date_And_Time)
    return date_Time_Object.date().strftime("%d %B, %Y (%A)")

def get_Lyrics_From_Track_ID(track_id):
	method = "track.lyrics.get"
	parameters = "&track_id=" + str(track_id)
	return call_API(method, parameters)

def create_Nodes(word, next_Word):
        with graph._driver.session() as session:
            greeting = session.write_transaction(graph.create_Nodes, word, next_Word)
            print(greeting)


graph = Graph(uri, user, password)
graph.clear_Graph()

method = "chart.tracks.get"
parameters = "&country=in"
top_Tracks_India_Data = call_API(method,parameters)
list_Of_Tracks = {}
for track_Dictionary in top_Tracks_India_Data["message"]["body"]["track_list"]:
    for dictionary in track_Dictionary.items():
        lyrics = get_Lyrics(dictionary[1]["track_name"], dictionary[1]["artist_name"])
        list_Of_Tracks[ dictionary[1]["track_name"]] = \
        {
            "track_id": dictionary[1]["track_id"],
            "first_release_date": parse_And_Readable(dictionary[1]["first_release_date"]),
            "artist_name": dictionary[1]["track_name"],
            "lyrics": lyrics["message"]["body"]["lyrics"]["lyrics_body"]
        }

all_Tracks_Lyrics_For_Graph={}
for track_Dictionary in top_Tracks_India_Data["message"]["body"]["track_list"]:
    for dictionary in track_Dictionary.items():
        all_Tracks_Lyrics_For_Graph[dictionary[1]["track_id"]] = get_Lyrics_From_Track_ID(dictionary[1]["track_id"])


for key in all_Tracks_Lyrics_For_Graph:
	for name, values in list_Of_Tracks.items():
		if values["track_id"] == key:
			song_Name = name
	data = all_Tracks_Lyrics_For_Graph[key]["message"]["body"]["lyrics"]["lyrics_body"]
	lyrics, disclaimer = data.split("...\n\n*******")
	while "(" in lyrics and ")" in lyrics:
		before, rest = lyrics.split("(",maxsplit=1)
		inside, after = rest.split(")",maxsplit=1)
		lyrics = before + after
	lyrics=lyrics.replace("\n\n","\n").replace("\n"," ").replace(",","").replace("!","")
	words=lyrics.split()
	for i in range(len(words)-1):
		create_Nodes(words[i], words[i+1])
	print(song_Name+" lyrics added to the graph")
	paradigmatic_Query='''
	MATCH (s:lyrics)
	// Get right1, left1
	MATCH (w:lyrics)-[:next]->(s)
	WITH collect(DISTINCT w.word) as left1, s
	MATCH (w:lyrics)<-[:next]-(s)
	WITH left1, s, collect(DISTINCT w.word) as right1
	// Match every other word
	MATCH (o:lyrics) WHERE NOT s = o
	WITH left1, right1, s, o
	// Get other right, other left1
	MATCH (w:lyrics)-[:next]->(o)
	WITH collect(DISTINCT w.word) as left1_o, s, o, right1, left1
	MATCH (w:lyrics)<-[:next]-(o)
	WITH left1_o, s, o, right1, left1, collect(DISTINCT w.word) as right1_o
	// compute right1 union, intersect
	WITH FILTER(x IN right1 WHERE x IN right1_o) as r1_intersect,
	  (right1 + right1_o) AS r1_union, s, o, right1, left1, right1_o, left1_o
	// compute left1 union, intersect
	WITH FILTER(x IN left1 WHERE x IN left1_o) as l1_intersect,
	  (left1 + left1_o) AS l1_union, r1_intersect, r1_union, s, o
	WITH DISTINCT r1_union as r1_union, l1_union as l1_union, r1_intersect, l1_intersect, s, o
	WITH 1.0*length(r1_intersect) / length(r1_union) as r1_jaccard,
	  1.0*length(l1_intersect) / length(l1_union) as l1_jaccard,
	  s, o
	WITH s, o, r1_jaccard, l1_jaccard, r1_jaccard + l1_jaccard as sim
	CREATE UNIQUE (s)-[r:RELATED_TO]->(o) SET r.paradig = sim;
	'''
	with graph._driver.session() as session:
	    session.run(paradigmatic_Query,song_Name=song_Name)
	paradigmatic_Query_Response='''MATCH (s:lyrics)-[r:RELATED_TO]->(o:lyrics) RETURN s.word,o.word,r.paradig AS sim ORDER BY sim DESC;'''
	with graph._driver.session() as session:
	    weighted_Keywords=session.run(paradigmatic_Query_Response)
	with graph._driver.session() as session:
		session.run(add_Song_Name_As_Label,song_Name=song_Name)
	with graph._driver.session() as session:
		session.run(remove_Lyrics_Label)
	print(song_Name+" MINED FOR PARADIGMATIC SIMILARITY USING JACCARD INDEX")
	print(weighted_Keywords)
