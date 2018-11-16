import configparser
config = configparser.ConfigParser()
config.read('config.txt')
apikey=config['MusixMatch']['API_key']

#API
import json, requests
def callAPI(method, parameters):
    response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + apikey ).text
    callbackToJson = response.replace( "callback(" , "").replace( ");" , "" )
    return json.loads(callbackToJson)

#Fetching
method = "track.lyrics.get"
parameters = "&track_id=115237681"
TrackLyrics = callAPI(method, parameters)

#Graph
from neo4j import GraphDatabase
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
            RETURN $word, $nextWord''', word=word, nextWord=nextWord )
        return result
    
graph = Graph(uri, user, password)
graph.clearGraph()

#Import
def createNodes(word, nextWord):
        with graph._driver.session() as session:
            greeting = session.write_transaction(graph.createNodes, word, nextWord)
            print(greeting)


for dictionary in TrackLyrics.items():
    lyrics, disclaimer = dictionary[1]["body"]["lyrics"]["lyrics_body"].split("...\n\n*******")
    while "(" in lyrics and ")" in lyrics:
        before, rest = lyrics.split("(",maxsplit=1)
        inside, after = rest.split(")",maxsplit=1)
        lyrics = before + after
    lyrics=lyrics.replace("\n\n","\n")
    lyrics=lyrics.replace("\n"," ")
    lyrics=lyrics.replace(",","")
    lyrics=lyrics.replace("!","")
    words=lyrics.split()
    

for i in range(len(words)-1):
    createNodes(words[i],words[i+1])

#Mining
paradigmaticQuery='''
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

paradigmaticQueryResponse='''MATCH (s)-[r:RELATED_TO]->(o) RETURN s.word,o.word,r.paradig AS sim ORDER BY sim DESC;'''

with graph._driver.session() as session:
    session.run(paradigmaticQuery)

with graph._driver.session() as session:
    session.run(paradigmaticQueryResponse)
