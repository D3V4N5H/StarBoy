#!/usr/bin/python3
from TopLyrics import *
from tkinter import *
from tkinter import ttk
# import tkinter
# import _tkinter
# tkinter._test()
import asyncio
class Interface:
	def __init__(self, master):
		master.title('Flubber')
		master.resizable(False,False)
		master.configure(background= '#ececec')

		style = ttk.Style()
		# style.configure('TFrame', background= "", )
		# style.configure('TButton', background="", )
		# style.configure('TLabel', background="", )
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
			# print('type of selection:',type(track_List_Display.selection()))
			# for item in track_List_Display.selection():
			# 	item_text = track_List_Display.item(item,"text")
			# 	print(item_text)
				# print('type of item:',type(item))				
			# print(track_List_Display.item(0,"text"))
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
			# if track_Name!='':
			track_Lyrics = get_Lyrics_From_Track_Name_And_Artist_Name(selected[0], artist_Name)
			print('Lyrics:\n',track_Lyrics)
			lyrics_Display.insert( 1.0 , str(track_Lyrics) )
			# lyrics_Display.config(state= 'disabled')

		fetch_Top_10_Button.grid(row= 4, column= 0)
		fetch_Lyrics_Button = ttk.Button(main_Frame, text= "Fetch Lyrics of selected Track", command= on_Click_Fetch_Track_Lyrics)
		fetch_Lyrics_Button.grid(row= 4, column= 1)
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

