#!/usr/bin/python3
from TopLyrics import *
from tkinter import *
from tkinter import ttk
# import tkinter
# import _tkinter
# tkinter._test()
class Interface:

	def __init__(self, master):
		style= ttk.Style(master)
		# style.theme_use('default')
		
		title = ttk.Label(master, text= 'Flubber - Your Music Connoisseur')
		title.config(justify= CENTER, font= ('Courier',32,'bold'))
		title.pack(pady= 20, padx= 10)
		
		main_Frame = ttk.Frame(master)
		main_Frame.config(height= 400, width= 600)
		main_Frame.pack()
		option = StringVar(main_Frame)
		India_Radio_Button = ttk.Radiobutton(main_Frame, text= 'India', variable= option, value= 'in')
		India_Radio_Button.grid(row= 0, column= 0, columnspan= 2)
		US_Radio_Button = ttk.Radiobutton(main_Frame, text= 'US', variable= option, value= 'us')
		US_Radio_Button.grid(row= 1, column= 0, columnspan= 2)

		ttk.Label(main_Frame, text= "Track List").grid(row= 2, column= 0)
		ttk.Label(main_Frame, text= "Lyrics").grid(row= 2, column= 1)
		track_List_Display = Text(main_Frame, width= 40, height= 10)
		track_List_Display.grid(row= 3, column=0)
		lyrics_Display = Text(main_Frame, width= 40, height= 10, wrap= 'word')
		lyrics_Display.grid(row= 3, column=1)
		
		def on_Click_Fetch_Top_Tracks():
			self.fetch_Top_10_Button.state([('disabled')])
			top_Tracks_Dict = get_Top_Tracks(option.get())
			print('\033[1m Dictionary downloaded \033[0m ')
			for track in top_Tracks_Dict:
				# def on_Click_Top_Track():
				# 	selected = treeview.selection()
				# treeview.bind('<<TreeviewSelect>>', on_Click_Top_Track)
				track_List_Display.insert(END, track+'\n')
			# for track in top_Tracks_Dict:
			# 	lyrics=re.split(', | |\n',top_Tracks_Dict[track]['lyrics'])
			# 	lyrics_Display.insert('1.0', lyrics)
			self.fetch_Top_10_Button.state([('!disabled')])
			self.fetch_Top_10_Button.config(text= "Fetch")

		def on_Click_Fetch_Track_Lyrics():
			pass


		self.fetch_Top_10_Button = ttk.Button(main_Frame, text = "Fetch Top 10 Tracks", command= on_Click_Fetch_Top_Tracks)
		self.fetch_Top_10_Button.grid(row= 4, column= 0)
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

