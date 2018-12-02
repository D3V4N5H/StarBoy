from tkinter import *
from tkinter import ttk
import tkinter
import _tkinter
# tkinter._test()
root = Tk()

title = ttk.Label(root, text= 'Flubber - Your Music Connoisseur', justify= CENTER)
title.pack()

bio = ttk.Label(root, text= 'Havana', wraplength= 150)
bio.pack()

coverFile = PhotoImage(file= 'havana.gif')
coverArt = Label(root, image= coverFile)
coverArt.pack()

root.mainloop()
