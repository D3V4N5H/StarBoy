from textblob import TextBlob

import json, requests
def call_API(method, parameters):
	response = requests.get( "https://api.musixmatch.com/ws/1.1/"+ method + "?format=jsonp&callback=callback" + parameters + "&apikey=" + api_key ).text
	callback_To_Json = response.replace( "callback(" , "").replace( ");" , "" )
	return json.loads(callback_To_Json)


from urllib.parse import quote as encode
def get_Lyrics(track_Name, artist_Name):
	method = "matcher.lyrics.get"
	title = "&q_track="
	artist = "&q_artist="
	_title= encode(track_Name)
	_artist = encode(artist_Name)
	parameters = title + _title + artist + _artist
	return call_API(method,parameters)

method = "chart.tracks.get"
parameters = "&country=in"
top_Tracks_India_Data = call_API(method,parameters)
list_Of_Tracks = {}

for track_Dictionary in top_Tracks_India_Data["message"]["body"]["track_list"]:
	for dictionary in track_Dictionary.items():
		fetchedLyrics = get_Lyrics(dictionary[1]["track_name"], dictionary[1]["artist_name"])["message"]["body"]["lyrics"]["lyrics_body"]
		lyrics, disclaimer = fetchedLyrics.split("...\n\n*******")
		while ("(" in lyrics and ")" in lyrics):
			before, rest = lyrics.split("(",maxsplit=1)
			inside, after = rest.split(")",maxsplit=1)
			lyrics = before + after
		while ("\n\n" in lyrics):
			lyrics = lyrics.replace("\n\n","\n")
		lyrics=lyrics.replace(",","").replace("!","")		
		list_Of_Tracks[ dictionary[1]["track_name"]] = {"track_id": dictionary[1]["track_id"], "lyrics": lyrics, "sentiment": blob.sentiment.polarity}

for track in list_Of_Tracks:
	lyrics=list_Of_Tracks[track]["lyrics"]
	blob=TextBlob(lyrics)
	print("Song: ", track)
	print("Sentiment:", blob.sentiment.polarity, "\n")
	print(blob.noun_phrases)
	for sentence in blob.sentences:
		print(sentence)
		print(sentence.sentiment.polarity, "\n")
