MATCH (n)
DETACH DELETE n
CREATE (u1:USER {name: "Devansh"}),
(s1:SONG {songName: "starboy"}),
(k1:KEYWORD {keyword: "cars"}),
(k2:KEYWORD {keyword: "money"}),
(m1:METADATA {data: "2016"}),
(m2:METADATA {data: "R&B"}),
(m3:METADATA {data: "Soul"}),
(m4:METADATA {data: "Daft Punk"}),
(u1)-[:LIKED]->(s1),
(s1)-[:IS_ABOUT]->(k1),
(s1)-[:IS_ABOUT]->(k2),
(s1)-[:RELEASE_DATE]->(m1),
(s1)-[:GENRE]->(m2),
(s1)-[:GENRE]->(m3),
(s1)-[:FEATURES]->(m4)
