// Delete existing nodes in the Graph
MATCH (n)
DETACH DELETE n

// Import, Create and Match word nodes
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

// List Word Frequencies
MATCH (w:lyrics)
RETURN w.word, w.count
ORDER BY w.count DESC

// List Word-Pair Frequencies
MATCH (w1:lyrics)-[r:next]->(w2:lyrics)
RETURN [w1.word, w2.word] AS word_pair, r.count AS count
ORDER BY r.count DESC

// Left1 for a particular word
MATCH (s:lyrics{word: "PARTICULAR_WORD"})
MATCH (w:lyrics)-[:next]->(s)
RETURN w.word AS word

// Right1 for a particular word
MATCH (s:lyrics{word: "PARTICULAR_WORD"})
MATCH (w:lyrics)<-[:next]-(s)
RETURN w.word AS word

// Count number of distinct Left1 words for a particular word
MATCH (s:lyrics{word: "PARTICULAR_WORD"})
MATCH (w:lyrics)-[:next]->(s)
RETURN count(w.count)

// Count number of distinct Right1 words for a particular word
MATCH (s:lyrics{word: "PARTICULAR_WORD"})
MATCH (w:lyrics)<-[:next]-(s)
RETURN count(w.count)

// Find out which word has the highest number of distinct Left1 words 
MATCH (o)
WITH o
MATCH (n)
MATCH (s{word:o.word})
MATCH (w:lyrics)-[:next]->(s)
RETURN 
CASE
WHEN count(DISTINCT w.word)>THRESHOLD_
THEN o.word END

// Find out which word has the highest number of distinct Right1 words 
MATCH (o)
WITH o
MATCH (n)
MATCH (s{word:o.word})
MATCH (w:lyrics)<-[:next]-(s)
RETURN 
CASE
WHEN count(DISTINCT w.word)>THRESHOLD_
THEN o.word END
