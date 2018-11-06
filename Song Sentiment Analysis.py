
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
	percentage = int(polarity*100)
	return "Pattern Analyzer Sentiment: "+str(percentage)+"% Happy 😀" if polarity > 0 else "\t"*6+"Pattern Analyzer Sentiment: "+str(abs(percentage))+"% Sad ☹️"

def infer_NaiveBayes_Sentiment(sentimentObject):
	if sentimentObject.classification == 'pos':
		return "Naive Bayes Sentiment: "+str(int(sentimentObject.p_pos*100)) + "% Happy 😀"
	else:
		return "\t"*6+"Naive Bayes Sentiment: "+str(abs(int(sentimentObject.p_neg*100))) + "% Sad ☹️"

IBM_url="https://gateway.watsonplatform.net/natural-language-understanding/api"

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


from textblob.sentiments import NaiveBayesAnalyzer

for track in list_Of_Tracks:
	lyrics=list_Of_Tracks[track]["lyrics"]
	languageAccordingToAPI = list_Of_Tracks[track]["language"]
	languageAccordingToAI = TextBlob(lyrics.replace("\n"," ")).detect_language()
	if languageAccordingToAPI=='en' and languageAccordingToAI=='en':
		blob=TextBlob(lyrics.replace("\n"," "))
		Naive_Bayes_blob=TextBlob(lyrics.replace("\n"," "), analyzer=NaiveBayesAnalyzer())
		if blob.sentiment.polarity!=0:
			print("\n\nSong: ", track)
			print(infer_Sentiment(blob.sentiment.polarity))
			print(infer_NaiveBayes_Sentiment(Naive_Bayes_blob.sentiment), "\n")
			# print("\n\tPhrases:\n\t", blob.noun_phrases,"\n\n")
			sentences = lyrics.split("\n")
			for sentence in sentences:
				sentence_Blob=TextBlob(sentence)
				Naive_Bayes_sentence_Blob=TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
				if sentence_Blob.sentiment.polarity!=0:
					print("\n☞", sentence)
					print(infer_Sentiment(sentence_Blob.sentiment.polarity))
					print(infer_NaiveBayes_Sentiment(Naive_Bayes_sentence_Blob.sentiment))

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
