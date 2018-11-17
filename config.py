import configparser
creds = configparser.ConfigParser()
creds.read('config.txt')

Watson_Ears=creds['IBM STT']['Flubber_Ears_API_key']
Watson_Gateway_URL = creds['IBM STT']['Flubber_Gateway_URL']
# creds['IBM NLU']['Watson_URL']

IBM_api_username = creds['IBM NLU']['Watson_Username']
IBM_api_password = creds['IBM NLU']['Waston_Password']

MxM_API_key = creds['MusixMatch']['API_key']
MxM_Base_URL = creds['MusixMatch']['Base_URL']

Genius_Bearer = creds['Genius']['Bearer']

Neo4j_Bolt_URI = creds['Neo4j']['Bolt_URI']
Neo4j_User = creds['Neo4j']['User']
Neo4j_Password = creds['Neo4j']['Password']
Neo4j_Import_Directory_Path = creds['Neo4j']['Import Path']

