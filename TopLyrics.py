from MusixMatch import *
from Genius import *


def clean_Up_Lyrics(lyrics):
	while ("\n\n" in lyrics):
		lyrics = lyrics.replace("\n\n","\n")
	lyrics=lyrics.replace(",","").replace("!","")
	return lyrics


def get_Top_Tracks_Lyrics(countryCode):
	list_Of_Tracks = {}
	
	top_Tracks_Data = get_MusixMatch_Top_Tracks_By_Country(countryCode)

	for track_Dictionary in top_Tracks_Data["message"]["body"]["track_list"]:
		for dictionary in track_Dictionary.items():
			track_Name=dictionary[1]["track_name"]
			artist_Name=dictionary[1]["artist_name"]
			print('\n'+track_Name, '-', artist_Name)

			genius_Song_ID=get_Genius_Song_ID_From_Track_Name_And_Artist_Name(track_Name, artist_Name)
			lyrics = get_Genius_Lyrics_From_Song_ID(genius_Song_ID)
			if lyrics:
				print("✅ Lyrics found from Genius.com")
				lyrics = remove_Section_Names(lyrics)
			
			if not lyrics:
				print("❌ Lyrics NOT found in Genius.com")
				track_Data = get_MusixMatch_Lyrics_From_Track_Name_And_Artist_Name(track_Name, artist_Name)
				language_According_To_MusixMatch = track_Data["message"]["body"]["lyrics"]["lyrics_language"]
				musixmatch_Lyrics = track_Data["message"]["body"]
				if isinstance(musixmatch_Lyrics, dict):
					print("😇 But found on MusixMatch")
					fetchedLyrics=musixmatch_Lyrics['lyrics']['lyrics_body']
					lyrics, disclaimer = fetchedLyrics.split("...\n\n*******")
					lyrics=remove_Background_Vocals_In_Brackets(lyrics)
			
			if lyrics:
				clean_Up_Lyrics(lyrics)
				list_Of_Tracks[ track_Name ] = {"track_id": dictionary[1]["track_id"], "lyrics": lyrics, 'artist_name': artist_Name}
	
	return list_Of_Tracks
