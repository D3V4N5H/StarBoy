from config import *
import requests
from bs4 import BeautifulSoup
import json, requests
from urllib.parse import quote as encode
import difflib

def find_Closest_Match(result, full_Name):
	words = full_Name.split()
	two = [' '.join([i,j]) for i,j in zip(words, words[1:])]
	two_Word_Pair_Matches=0
	for hit in result:
		name_From_Result = hit['result']['full_title']
		close_Matches = difflib.get_close_matches(name_From_Result, two, cutoff=0.2)
		score = len(close_Matches)
		if score > two_Word_Pair_Matches:
			print('\n'+name_From_Result)
			print('score:', score)
			two_Word_Pair_Matches = score
			id=hit['result']['id']	
	print('\nsong_ID:')
	return id


def remove_Section_Names(lyrics):
	while ("[" in lyrics and "]" in lyrics):
		before, rest = lyrics.split("[",maxsplit=1)
		inside, after = rest.split("]",maxsplit=1)
		lyrics = before + after
	return lyrics

def get_Genius_Lyrics_From_Song_ID(song_ID):
	search_url = genius_Base_Url + '/songs/'+str(song_ID)+'?text_format=plain'
	response=requests.get(search_url, headers=headers)
	if response.json()['meta']['status']==200:
		url = response.json()['response']['song']['url']
		if url:
			page = requests.get(url)
			html = BeautifulSoup(page.text, "html.parser")
			return html.find("div", class_="lyrics").get_text()

def get_Genius_Song_ID_From_Track_Name_And_Artist_Name(track_Name, artist):
	full_Name = track_Name+' '+artist
	query=encode(full_Name)
	search_url = genius_Base_Url + '/search?q='+query
	response=requests.get(search_url, headers=headers)
	result=response.json()['response']['hits']
	if result!=[]:
		song_ID=find_Closest_Match(result, full_Name)
		return song_ID
