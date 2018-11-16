from __future__ import print_function

import configparser
config = configparser.ConfigParser()
config.read('config.txt')
IBM_api_username = config['IBM NLU']['Watson_Username']
IBM_api_password = config['IBM NLU']['Waston_Password']


import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions

service = NaturalLanguageUnderstandingV1(version='2018-03-16',url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19',username=IBM_api_username,password=IBM_api_password)

response = service.analyze(
	text="I'm tryna put you in the worst mood ah "
	'P1 cleaner than your church shoes ah '
	'Milli point two just to hurt you ah '
	"All red Lamb' just to tease you ah "
	'None of these toys on lease too ah '
	'Made your whole year in a week too yah '
	'Main bitch out your league too ah '
	'Side bitch out of your league too ah '
	'House so empty need a centerpiece '
	'Twenty racks a table cut from ebony '
	'Cut that ivory into skinny pieces '
	'Then she clean it with her face man I love my baby '
	'You talking money need a hearing aid '
	"You talking 'bout me I don't see a shade "
	'Switch up my style I take any lane '
	'I switch up my cup I kill any pain ',
	features=Features(	emotion=EmotionOptions()
						# concepts=ConceptsOptions(limit=10),
						# categories=CategoriesOptions(),
						# entities=EntitiesOptions(),
						# keywords=KeywordsOptions(),

						 ) ).get_result()
 
print(json.dumps(response, indent=2))
