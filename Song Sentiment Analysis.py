from __future__ import print_function

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions
from textblob import TextBlob

service = NaturalLanguageUnderstandingV1(version='2018-03-16',url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19',username=IBM_api_username,password=IBM_api_password)

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
	percentage = round(polarity*100,2)
	return "Pattern Analyzer Sentiment: "+str(percentage)+"% Happy 😀" if polarity > 0 else "\t"*6+"Pattern Analyzer Sentiment: "+str(abs(percentage))+"% Sad ☹️"

def infer_NaiveBayes_Sentiment(sentimentObject):
	if sentimentObject.classification == 'pos':
		return "Naive Bayes Sentiment: "+str(round(sentimentObject.p_pos*100,2)) + "% Happy 😀"
	else:
		return "\t"*6+"Naive Bayes Sentiment: "+str(abs(round(sentimentObject.p_neg*100,2))) + "% Sad ☹️"

def infer_IBM_Watson_Emotions(response):
	emotion_Dictionary=response['emotion']['document']['emotion']
	return '\t'*2+'IBM Watson 🧠 Sadness: '+str(round(emotion_Dictionary['sadness']*100,2))+'%  Joy: '+str(round(emotion_Dictionary['joy']*100,2))+'%'

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
			print("\n\nSong: ", track,"\n")
			print(infer_Sentiment(blob.sentiment.polarity))
			print(infer_NaiveBayes_Sentiment(Naive_Bayes_blob.sentiment), "\n")
			if blob.sentiment.polarity>0 and Naive_Bayes_blob.sentiment.classification=='neg' or blob.sentiment.polarity<0 and Naive_Bayes_blob.sentiment.classification=='pos':
				print(infer_IBM_Watson_Emotions(service.analyze( text=lyrics.replace("\n"," "), features=Features(emotion=EmotionOptions()) ).get_result()))
			# print("\n\tPhrases:\n\t", blob.noun_phrases,"\n\n")
			sentences = lyrics.split("\n")
			for sentence in sentences:
				sentence_Blob=TextBlob(sentence)
				Naive_Bayes_sentence_Blob=TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
				if sentence_Blob.sentiment.polarity!=0:
					sentiment_According_To_PA=infer_Sentiment(sentence_Blob.sentiment.polarity)
					sentiment_According_To_NB=infer_NaiveBayes_Sentiment(Naive_Bayes_sentence_Blob.sentiment)
					if sentence_Blob.sentiment.polarity>0 and Naive_Bayes_sentence_Blob.sentiment.classification=='neg' or sentence_Blob.sentiment.polarity<0 and Naive_Bayes_sentence_Blob.sentiment.classification=='pos' :
						print("\n\n☞", sentence, "\n")
						print(sentiment_According_To_PA)
						print(sentiment_According_To_NB)
						sentiment_According_To_IBM=infer_IBM_Watson_Emotions(service.analyze( text=sentence, features=Features(emotion=EmotionOptions()) ).get_result())
						print("\n", sentiment_According_To_IBM)


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
