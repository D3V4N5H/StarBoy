from __future__ import print_function
from config import *
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions

service = NaturalLanguageUnderstandingV1(version='2018-03-16',url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19',username=IBM_api_username,password=IBM_api_password)

def Watson_Analyze(text):
	return service.analyze(text= text,features=Features(	emotion=EmotionOptions()) ).get_result()
						# concepts=ConceptsOptions(limit=10),
						# categories=CategoriesOptions(),
						# entities=EntitiesOptions(),
						# keywords=KeywordsOptions(),
						 
 
# print(json.dumps(response, indent=2))

def infer_IBM_Watson_Emotions(response):
	emotion_Dictionary=response['emotion']['document']['emotion']
	sadness = emotion_Dictionary['sadness']
	sadnessPercentage = str(round(sadness*100,2))
	joy = emotion_Dictionary['joy']
	joyPercentage = str(round(joy*100,2))+'%'
	fear = emotion_Dictionary['fear']
	fearPercentage = str(round(fear*100,2))+'%'
	disgust = emotion_Dictionary['disgust']
	disgustPercentage = str(round(disgust*100,2))+'%'
	anger = emotion_Dictionary['anger']
	angerPercentage = str(round(anger*100,2))+'%'
	return {'sadness': sadnessPercentage,'joy': joyPercentage,'fear': fearPercentage,'disgust': disgustPercentage,'anger': angerPercentage}
