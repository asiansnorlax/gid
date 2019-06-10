import tkinter 
import tkinter.messagebox
import PIL.Image
from PIL import ImageTk
from tkinter import *
import os

def normalActivity():
    string = userEntry.get()
    showText.configure(text=string)
    Menu.title("Google Images/GIF Downloader")
    return

def previewActivity():
    showText.configure(text="Preview") 


    path = "1.wmpvownqus8xwvylswsr.jpg"
    img = PhotoImage(file="1.wmpvownqus8xwvylswsr.jpg")
    img = tkinter.PhotoImage(file="1.wmpvownqus8xwvylswsr.jpg")
    Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.Image.open(path)

    The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Label(Menu, image = img)

    The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    canv = Canvas(Menu, bg='white')

    img = ImageTk.PhotoImage(Image.open("bll.jpg"))  # PIL solution
    canv.create_image(anchor=NW, image=img)

def commands():
    showText.configure(text = getCommands(),font=("Helvetica", 8),justify=LEFT)      #Configure text in window       

def gifActivity():
    showText.configure(text="GIF")
def getCommands():
    stringArgs = "usage: google_images_download.py [-h] [-k KEYWORDS] [-kf KEYWORDS_FROM_FILE]"
    stringArgs +="\n                                 [-sk SUFFIX_KEYWORDS] [-pk PREFIX_KEYWORDS]"
    stringArgs +="\n                                 [-l LIMIT]"
    stringArgs +="\n                                 [-f {jpg,gif,png,bmp,svg,webp,ico}] [-u URL]"
    stringArgs +="\n                                 [-x SINGLE_IMAGE] [-o OUTPUT_DIRECTORY]"
    stringArgs +="\n                                 [-i IMAGE_DIRECTORY] [-n] [-d DELAY]"
    stringArgs +="\n                                 [-co {red,orange,yellow,green,teal,blue,purple,pink,white,gray,black,brown}]"
    stringArgs +="\n                                 [-ct {full-color,black-and-white,transparent}]"
    stringArgs +="\n                                 [-r {labeled-for-reuse-with-modifications,labeled-for-reuse,labeled-for-noncommercial-reuse-with-modification,labeled-for-nocommercial-reuse}]"
    stringArgs +="\n                                 [-s {large,medium,icon,>400*300,>640*480,>800*600,>1024*768,>2MP,>4MP,>6MP,>8MP,>10MP,>12MP,>15MP,>20MP,>40MP,>70MP}]"
    stringArgs +="\n                                 [-es EXACT_SIZE]"
    stringArgs +="\n                                 [-t {face,photo,clipart,line-drawing,animated}]"
    stringArgs +="\n                                 [-w {past-24-hours,past-7-days,past-month,past-year}]"
    stringArgs +="\n                                 [-wr TIME_RANGE]"
    stringArgs +="\n                                 [-a {tall,square,wide,panoramic}]"
    stringArgs +="\n                                 [-si SIMILAR_IMAGES] [-ss SPECIFIC_SITE] [-p]"
    stringArgs +="\n                                 [-ps] [-pp] [-m] [-e] [-st SOCKET_TIMEOUT]"
    stringArgs +="\n                                 [-th] [-tho]"
    stringArgs +="\n                                 [-la {Arabic,Chinese Simplified),Chinese (Traditional,Czech,Danish,Dutch,English,Estonian,Finnish,French,German"
    stringArgs +="\n                                 Greek,Hebrew,Hungarian,Icelandic,Italian,Japanese,Korean,Latvian,Lithuanian,Norwegian,Portuguese,Polish,Romanian,Russian,Spanish,Swedish,Turkish}]"
    stringArgs +="\n                                 [-pr PREFIX] [-px PROXY] [-cd CHROMEDRIVER]"
    stringArgs +="\n                                 [-ri] [-sa] [-nn] [-of OFFSET] [-nd] [-sil]"
    stringArgs +="\n                                 [-is SAVE_SOURCE]"
    stringArgs +="\n                                 Example: --keywords \"Polar Bears, Balloons\" --limit 20"
    return stringArgs
Menu = tkinter.Tk()                            #Create Window
Menu.title("Google Images/GIF Downloader")
                   #Pack Text into Window 'Menu'
showText = Label(text = "Enter a command")
showText.pack()
userEntry = Entry()
userEntry.pack()
    
commandButton = tkinter.Button(Menu, text ="Show Commands", command = commands,bg="white",fg="black",justify=CENTER)
normalButton = tkinter.Button(Menu, text ="Normal Download", command = normalActivity,bg="gray",fg="white",justify=CENTER)  #Configure Buttons
previewButton = tkinter.Button(Menu, text ="Preview Pictures", command = previewActivity,bg="blue",fg="white",justify=CENTER)
gifButton = tkinter.Button(Menu, text ="Download GiFs", command = gifActivity,bg="green",fg="black",justify=CENTER)

commandButton.pack()            #Pack Button into Window
normalButton.pack()    
previewButton.pack()
gifButton.pack()

Menu.mainloop()  #InfiteLoop
