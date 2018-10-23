
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
	@staticmethod
	def create_Nodes(tx):
		result = tx.run('''
			LOAD CSV FROM "file:///starboyExportedLyrics.csv" AS line
			FIELDTERMINATOR ' '
			FOREACH (w IN RANGE(0, SIZE(line)-2) | 
			MERGE (lx:lyrics{word:line[w]})
				ON CREATE SET lx.count = 1
				ON MATCH SET lx.count = lx.count + 1
			MERGE (mx:lyrics{word:line[w+1]})
				ON CREATE SET mx.count = 1
				ON MATCH SET mx.count = mx.count + (case when w = SIZE(line)-2 then 1 else 0 end)
			MERGE (lx)-[r:next]->(mx)
				ON CREATE SET r.count = 1
				ON MATCH SET r.count = r.count +1)
			RETURN line''')
		return result
	@staticmethod
	def listWordFreq(driver):
		with driver.session() as session:
			return session.run('''
				MATCH (w:lyrics)
				RETURN w.word, w.count
				ORDER BY w.count DESC
				''')
	@staticmethod
	def listWordPairFreq(driver):
		with driver.session() as session:
			return session.run('''
				MATCH (w1:lyrics)-[r:next]->(w2:lyrics)
				RETURN [w1.word, w2.word] AS word_pair, r.count AS count
				ORDER BY r.count DESC
				''')


graph = Graph(uri, user, password)
graph.clearGraph(graph._driver)

wDict={}
def wordFreq_wDict():
	with graph._driver.session() as tx:
		for record in tx.run('''MATCH (w:lyrics)
		RETURN w.word, w.count
		ORDER BY w.count DESC'''):
			wDict[record["w.word"]]=record["w.count"]

def print_wDict():
	for x, y in wDict.items():
		print(x, y)

wordFreq_wDict()
print_wDict()

wpDict={}
def wordPairFreq_wpDict():
	with graph._driver.session() as tx:
		for record in tx.run('''MATCH (w1:lyrics)-[r:next]->(w2:lyrics)
		RETURN [w1.word, w2.word] AS word_pair, r.count AS count
		ORDER BY r.count DESC'''):
			wpDict[tuple(record["word_pair"])]=record["count"]

def print_wpDict():
	for i in wpDict.items():
		print (i[0], i[1])

wordPairFreq_wpDict()
print_wpDict()

#Getting Lyrics
import json, requests
def call_API(method, parameters):
	response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + api_key ).text
	callback_To_Json = response.replace( "callback(" , "").replace( ");" , "" )
	return json.loads(callback_To_Json)


def get_Lyrics_From_Track_ID(track_id):
	method = "track.lyrics.get"
	parameters = "&track_id=" + str(track_id)
	return call_API(method, parameters)


#Mining

def create_Nodes():
		with graph._driver.session() as session:
			session.write_transaction(graph.create_Nodes)

fetchedLyrics = get_Lyrics_From_Track_ID(115237681)
lyrics, disclaimer = fetchedLyrics["message"]["body"]["lyrics"]["lyrics_body"].split("...\n\n*******")

while "(" in lyrics and ")" in lyrics:
	before, rest = lyrics.split("(",maxsplit=1)
	inside, after = rest.split(")",maxsplit=1)
	lyrics = before + after
lyrics = lyrics.replace("\n\n","\n").replace(",","").replace("!","") #.replace("\n"," ")
lyricsLine = lyrics.split("\n")
import csv
with open (r'starboyExportedLyrics.csv', 'wb') as write_file:
	write=csv.writer(write_file)
	write.writerows([r] for r in lyricsLine)

print("Starboy lyrics added to the graph")


paradigmatic_Query='''
// Mining Paradigmatic Word Associations using Jaccard Index to compute similarity
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

# paradigmatic_Query_Response='''MATCH (s:lyrics)-[r:RELATED_TO]->(o:lyrics) RETURN s.word,o.word,r.paradig ORDER BY r.paradig DESC;'''
# def paradigmatic_Query_Response_Function(tx):
# 	for record in tx.run(paradigmatic_Query_Response):
# 		# print(record["s.word"], record["o.word"], record["sim"])
# 		list_Of_Tracks[song_Name]["jaccard"].append({tuple([record["s.word"], record["o.word"]]): record["r.paradig"]})

# with graph._driver.session() as session:
	 # session.run(paradigmatic_Query)
# with graph._driver.session() as session:
# 	 session.read_transaction(paradigmatic_Query_Response_Function)

# print("Starboy MINED FOR PARADIGMATIC SIMILARITY USING JACCARD INDEX")

graph.close()
