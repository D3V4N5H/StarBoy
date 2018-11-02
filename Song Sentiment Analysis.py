
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

def infer_Sentiment(polarity):
	percentage = str(int(round(polarity,2)*100))+"% "
	return percentage+"Happy" if polarity > 0 else percentage+"Sad"

method = "chart.tracks.get"
parameters = "&country=in"
top_Tracks_India_Data = call_API(method,parameters)
list_Of_Tracks = {}

for track_Dictionary in top_Tracks_India_Data["message"]["body"]["track_list"]:
	for dictionary in track_Dictionary.items():
		if isinstance(get_Lyrics(dictionary[1]["track_name"], dictionary[1]["artist_name"])["message"]["body"], dict):
			track_Data = get_Lyrics(dictionary[1]["track_name"], dictionary[1]["artist_name"])
			language=track_Data["message"]["body"]["lyrics"]["lyrics_language"]
			fetchedLyrics = track_Data["message"]["body"]["lyrics"]["lyrics_body"]
			lyrics, disclaimer = fetchedLyrics.split("...\n\n*******")
			while ("(" in lyrics and ")" in lyrics):
				before, rest = lyrics.split("(",maxsplit=1)
				inside, after = rest.split(")",maxsplit=1)
				lyrics = before + after
			while ("\n\n" in lyrics):
				lyrics = lyrics.replace("\n\n","\n")
			lyrics=lyrics.replace(",","").replace("!","")		
			list_Of_Tracks[ dictionary[1]["track_name"]] = {"track_id": dictionary[1]["track_id"], "lyrics": lyrics, "language": language}

for track in list_Of_Tracks:
	languageAccordingToAPI = list_Of_Tracks[track]["language"]
	languageAccordingToAI = TextBlob(list_Of_Tracks[track]["lyrics"].replace("\n"," ")).detect_language()
	if languageAccordingToAPI!='':
		print("\nSong:", track)
		print("Language According To API:", languageAccordingToAPI)
		print("Language According To AI:", languageAccordingToAI)
# for track in list_Of_Tracks:
# 	lyrics=list_Of_Tracks[track]["lyrics"]
# 	blob=TextBlob(lyrics.replace("\n"," "))
# 	if blob.sentiment.polarity!=0:
# 		print("\n\nSong: ", track)
# 		print("Sentiment:", infer_Sentiment(blob.sentiment.polarity), "\n")
# 		# print(blob.noun_phrases)
# 		sentences = lyrics.split("\n")
# 		for sentence in sentences:
# 			sentence_Blob=TextBlob(sentence)
# 			if sentence_Blob.sentiment.polarity!=0:
# 				print(sentence)
# 				print(infer_Sentiment(sentence_Blob.sentiment.polarity))

#PseudoCode
# import nltk
# text = nltk.tokenize.word_tokenize("I can tag you or you can add the tag yourself")
# for tag in nltk.pos_tag(text):
# 	print(tag)
# for t in list_Of_Tracks:
# 	print(t)
# list_Of_Tracks["Putt Jatt Da"]["lyrics"].replace("\n"," ")
# for line in list_Of_Tracks["Putt Jatt Da"]["lyrics"].split("\n"):
# 	print(line)
# TextBlob(list_Of_Tracks["Putt Jatt Da"]["lyrics"].replace("\n"," ")).detect_language()
