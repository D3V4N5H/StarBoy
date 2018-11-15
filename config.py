import configparser
config = configparser.ConfigParser()
config.read('config.txt')
config['IBM STT']['Flubber_Ears_API_key']
config['IBM STT']['Flubber_Gateway_URL']
config['IBM NLU']['Watson_URL']
config['IBM NLU']['Watson_Username']
config['IBM NLU']['Waston_Password']
config['MusixMatch']['API_key']
config['MusixMatch']['Base_URL']
config['Genius']['Bearer']
config['Neo4j']['Bolt_URI']
config['Neo4j']['User']
config['Neo4j']['Password']
