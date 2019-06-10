import tkinter 
import tkinter.messagebox
from tkinter import *
Menu = tkinter.Tk()                            #Create Window
OptionsText = Label(Menu,text ="Options")      #Configure text in window
OptionsText.pack()                             #Pack Text into Window 'Menu'

A = tkinter.Button(Menu, text ="1. Show Adjacency List", command = PrintAdjacencyList,bg="blue",fg="white")  #Configure Buttons
B = tkinter.Button(Menu, text ="2. Add Link", command = AddLink,bg="black",fg="white")
C = tkinter.Button(Menu, text ="3. Remove Link", command = RemoveLink,bg="black",fg="white")
D = tkinter.Button(Menu, text ="4. Trasverse the network", command = NetworkTraversal,bg="black",fg="white")
E = tkinter.Button(Menu, text ="5. Show Neighbours of a city", command = ShowNeighbour,bg="black",fg="white")
F = tkinter.Button(Menu, text ="6. Show Activity Log", command = ShowActivityLog,bg="purple",fg="white")

A.pack(fill = X)    #Pack Button into Window
B.pack(fill = X)
C.pack(fill = X)
D.pack(fill = X)
E.pack(fill = X)
F.pack(fill = X)

Menu.mainloop()  #InfiteLoop
