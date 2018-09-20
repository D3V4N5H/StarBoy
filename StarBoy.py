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
    def createNodes(driver):
        with driver.session() as session:
            return session.run('''
                LOAD CSV FROM "file:///starboy.csv" AS line
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
                RETURN line
                ''')

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
graph.createNodes(graph._driver)
graph.listWordFreq(graph._driver)
graph.listWordPairFreq(graph._driver)

wdict={}
def wordFreqToWdict():
    with graph._driver.session() as tx:
        for record in tx.run('''MATCH (w:lyrics)
        RETURN w.word, w.count
        ORDER BY w.count DESC'''):
            wdict[record["w.word"]]=record["w.count"]

def printWdict():
    for x, y in wdict.items():
        print(x, y)

wordFreqToWdict()
printWdict()

graph.close()
