#!/usr/bin/python3
from TopLyrics import *
from tkinter import *
from tkinter import ttk
# import tkinter
# import _tkinter
# tkinter._test()
class Interface:

	def __init__(self, master):
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

		ttk.Label(main_Frame).grid(row= 2, column= 0)
		ttk.Label(main_Frame, text= "Lyrics").grid(row= 2, column= 1)
		track_List_Display = ttk.Treeview(main_Frame)

		def update_Selected_Top_Track():
			global selected
			selected = track_List_Display.selection()

		track_List_Display.bind('<<TreeviewSelect>>', lambda e:update_Selected_Top_Track())
		track_List_Display.grid(row= 3, column=0)
		track_List_Display.heading('#0',text= "Track List")
		lyrics_Display = Text(main_Frame, width= 40, height= 10, wrap= 'word')
		lyrics_Display.grid(row= 3, column=1)

		def on_Click_Fetch_Top_Tracks():
			global option
			fetch_Top_10_Button.state([('disabled')])
			tracks_Names_And_Their_Artists = get_Top_Tracks_Names_And_Their_Artists(option.get())
			for track in top_Tracks_Dict:
				track_List_Display.insert('', 'end', 'track '+str(track_Count), text= track)

		fetch_Top_10_Button = ttk.Button(main_Frame, text = "Fetch Top 10 Tracks", command= on_Click_Fetch_Top_Tracks)

		def on_Click_Fetch_Track_Lyrics():
			global selected
			lyrics_Display.delete(1.0,'end')
			track_Lyrics = get_Lyrics_From_Track_Name_And_Artist_Name
			lyrics_Display.insert(1.0, )
			# lyrics_Display.config(state= 'disabled')
			# fetch_Top_10_Button.state([('!disabled')])
			# fetch_Top_10_Button.config(text= "Fetch")

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

