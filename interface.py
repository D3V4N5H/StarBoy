#!/usr/bin/python3
from __future__ import print_function
from config import *
from TopLyrics import *
from tkinter import *
from tkinter import ttk
# import tkinter
# import _tkinter
# tkinter._test()


class Interface:
	def __init__(self, master):
		
		import json
		from watson_developer_cloud import NaturalLanguageUnderstandingV1
		from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions
		service = NaturalLanguageUnderstandingV1(version='2018-03-16',url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19',username=IBM_api_username,password=IBM_api_password)

		master.title('Flubber')
		master.resizable(False,False)
		master.configure(background= '#ececec')

		style = ttk.Style()
		style.configure('WhiteFont.TLabel', font= ('Arial', 18, 'bold') )

		title = ttk.Label(master, text= 'Flubber - Your Music Connoisseur')
		title.config(justify= CENTER, font= ('Courier',32,'bold'))
		title.pack(pady= 20, padx= 10)
		
		main_Frame = ttk.Frame(master)
		main_Frame.config(height= 400, width= 600)
		main_Frame.pack()
		global option
		option = StringVar(main_Frame)
		India_Radio_Button = ttk.Radiobutton(main_Frame, text= 'India', variable= option, value= 'in')
		India_Radio_Button.grid(row= 0, column= 0, columnspan= 2)
		US_Radio_Button = ttk.Radiobutton(main_Frame, text= 'US', variable= option, value= 'us')
		US_Radio_Button.grid(row= 1, column= 0, columnspan= 2)

		ttk.Label(main_Frame, text= "Lyrics", style= 'Header.TLabel').grid(row= 2, column= 1)
		fetching_Label = ttk.Label(main_Frame, text= "Fetching...")
		fetching_Label.grid(row= 2, column= 0)
		fetching_Label.grid_forget()
		track_List_Display = ttk.Treeview(main_Frame)

		def update_Selected_Top_Track(event):
			global selected
			selected = track_List_Display.selection()

		track_List_Display.bind('<<TreeviewSelect>>', update_Selected_Top_Track)
		track_List_Display.grid(row= 3, column=0)
		track_List_Display.heading('#0',text= "Track List")
		lyrics_Display = Text(main_Frame, width= 40, height= 10, wrap= 'word')
		lyrics_Display.grid(row= 3, column=1)

		def on_Click_Fetch_Top_Tracks():
			global option
			fetching_Label.grid(row= 2, column= 0)
			fetch_Top_10_Button.state([('disabled')])
			global tracks_Names_And_Their_Artists
			tracks_Names_And_Their_Artists = get_Top_Tracks_Names_And_Their_Artists(option.get())
			for track in tracks_Names_And_Their_Artists:
				track_List_Display.insert('', 'end', track, text= track)
			fetch_Top_10_Button.state([('!disabled')])
			fetching_Label.grid_forget()
			fetch_Top_10_Button.config(text= "Fetch Top 10 Tracks")
			

		fetch_Top_10_Button = ttk.Button(main_Frame, text = "Fetch Top 10 Tracks", command= on_Click_Fetch_Top_Tracks)

		def on_Click_Fetch_Track_Lyrics():
			global selected
			global tracks_Names_And_Their_Artists
			artist_Name=''
			for track in tracks_Names_And_Their_Artists:
				if selected[0] == track:
						print(track)
						artist_Name = tracks_Names_And_Their_Artists[track]
			lyrics_Display.delete(1.0,END)
			print('track_Name:',selected)
			print('artist_Name:',artist_Name)
			track_Lyrics = get_Lyrics_From_Track_Name_And_Artist_Name(selected[0], artist_Name)
			print('Lyrics:\n',track_Lyrics)
			lyrics_Display.insert( 1.0 , str(track_Lyrics['lyrics']) )
			# lyrics_Display.config(state= 'disabled')

		fetch_Top_10_Button.grid(row= 4, column= 0)
		fetch_Lyrics_Button = ttk.Button(main_Frame, text= "Fetch Lyrics of selected Track", command= on_Click_Fetch_Track_Lyrics)
		fetch_Lyrics_Button.grid(row= 4, column= 1)
		emotion_IBM_Label = ttk.Label(main_Frame, text= "Emotions by IBM:")
		emotion_IBM_Label.grid(row= 5, column= 0)

		def Watson_Analyze(text):
			return service.analyze(text= text,features=Features(	emotion=EmotionOptions()) ).get_result()


		def infer_IBM_Watson_Emotions(response):
			emotion_Dictionary=response['emotion']['document']['emotion']
			sadness = emotion_Dictionary['sadness']
			sadnessPercentage = str(round(sadness*100,2))+'%'
			joy = emotion_Dictionary['joy']
			joyPercentage = str(round(joy*100,2))+'%'
			fear = emotion_Dictionary['fear']
			fearPercentage = str(round(fear*100,2))+'%'
			disgust = emotion_Dictionary['disgust']
			disgustPercentage = str(round(disgust*100,2))+'%'
			anger = emotion_Dictionary['anger']
			angerPercentage = str(round(anger*100,2))+'%'
			return {'sadness': sadnessPercentage,'joy': joyPercentage,'fear': fearPercentage,'disgust': disgustPercentage,'anger': angerPercentage}

		def on_Click_Watson_Emotion_Button():
			lyrics = lyrics_Display.get('1.0', 'end')
			lyrics
			emotions = infer_IBM_Watson_Emotions(Watson_Analyze(lyrics))
			sad_Value_IBM_Label.config(text= emotions['sadness'])
			joy_Value_IBM_Label.config(text= emotions['joy'])
			fear_Value_IBM_Label.config(text= emotions['fear'])
			disgust_Value_IBM_Label.config(text= emotions['disgust'])
			anger_Value_IBM_Label.config(text= emotions['anger'])

		watson_Emotion_Button = ttk.Button(main_Frame, text="IBM Watson Sentiment Analysis", command= on_Click_Watson_Emotion_Button)
		watson_Emotion_Button.grid(row= 5, column= 1)
		sad_IBM_Label = ttk.Label(main_Frame, text="Sad")
		sad_IBM_Label.grid(row= 6, column= 0)
		sad_Value_IBM_Label = ttk.Label(main_Frame)
		sad_Value_IBM_Label.grid(row= 6, column= 1)
		joy_IBM_Label = ttk.Label(main_Frame, text="Joy")
		joy_IBM_Label.grid(row= 7, column= 0)
		joy_Value_IBM_Label = ttk.Label(main_Frame)
		joy_Value_IBM_Label.grid(row= 7, column= 1)
		fear_IBM_Label = ttk.Label(main_Frame, text="Fear")
		fear_IBM_Label.grid(row= 8, column= 0)
		fear_Value_IBM_Label = ttk.Label(main_Frame)
		fear_Value_IBM_Label.grid(row= 8, column= 1)
		disgust_IBM_Label = ttk.Label(main_Frame, text="Disgust")
		disgust_IBM_Label.grid(row= 9, column= 0)
		disgust_Value_IBM_Label = ttk.Label(main_Frame)
		disgust_Value_IBM_Label.grid(row= 9, column= 1)
		anger_IBM_Label = ttk.Label(main_Frame, text="Anger")
		anger_IBM_Label.grid(row= 10, column= 0)
		anger_Value_IBM_Label = ttk.Label(main_Frame)
		anger_Value_IBM_Label.grid(row= 10, column= 1)
		

		# coverFile = PhotoImage(file= 'havana.gif')
		# coverArt = Label(master, image= coverFile)
		# coverArt.pack()
		
		# bio = ttk.Label(master, text= 'Havana', wraplength= 150)
		# bio.pack()


def main():			
	
	root = Tk()
	interface = Interface(root)
	root.mainloop()

if __name__ == "__main__": main()

