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

// Finding words related to a PARTICULAR_WORD
MATCH (s:lyrics {word: 'PARTICULAR_WORD'} )-[r:RELATED_TO]->(o) RETURN s.word,o.word,r.paradig as sim ORDER BY sim DESC;

// Finding words that a PARTICULAR_WORD is related to
MATCH (s)-[r:RELATED_TO]->(o:lyrics {word: 'PARTICULAR_WORD'} ) RETURN s.word,o.word,r.paradig as sim ORDER BY sim DESC;

// Finding all word-pair relations and their Paradigmatic similarity according to Jaccard index
MATCH (s)-[r:RELATED_TO]->(o) RETURN s.word,o.word,r.paradig AS sim ORDER BY sim DESC;
