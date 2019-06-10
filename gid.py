from tkinter import *
from PIL import ImageTk, Image
from google_images_download import googleimagesdownload as gID

def splitString(string):
    return string.split()

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
    stringArgs +="\n                                 Example: --limit 5  --language \"Czech\""
    showText.configure(text=stringArgs)
def formArguments():
    entry = keywordsEntry.get()
    otherEntries = otherEntry.get()
    if otherEntries !="":           #Check if Entry is null
        otherEntriesArray = splitString(otherEntries) #Separate variables
        for i in range(0,(len(otherEntriesArray))//2):
            Records[otherEntriesArray[i*2]] =otherEntriesArray[(i*2) +1]
    Records['keywords'] = entry
    return Records
    
def normalActivity():
    buttonList =[previewButton, normalButton, placeholderButton, commandsButton, keywordsEntryText, keywordsEntry, otherEntryText, otherEntry, otherEntryText]
    forgetButton(buttonList) #clear old buttons
    Menu.title("Google Images/GIF Downloader")
    Records = formArguments()
    #Records['limit'] = '3'
    response = gID()            
    absolute_image_paths = response.download(Records)
    
    return
def forgetButton(buttons):
    for button in buttons:
        button.grid_forget()
    return
def previewActivity():
    global img      #So Image is not cleared by stack
    
    buttonList =[previewButton, normalButton, placeholderButton, commandsButton, keywordsEntryText, keywordsEntry, otherEntryText, otherEntry, keywordsExampleText]
    forgetButton(buttonList) #clear old buttons
    showText.configure(text="Preview")
    showText.grid(row=8, column=3,columnspan=3,pady=5)
    canv = Canvas(Menu, width=800, height=500, bg='white')
    canv.grid(row=2, column=3)
    img = ImageTk.PhotoImage(Image.open("1.wmpvownqus8xwvylswsr.jpg"))  # PIL solution
    canv.create_image(20, 20, anchor=NW, image=img)
    keepButton=Button(text="Keep",bg="blue",fg="white").grid(row=9, column=2,columnspan=3,pady=5)
    deleteButton=Button(text="Delete",bg="black",fg="white").grid(row=10, column=2,columnspan=3,pady=5)
#Main Program
Records = {}
#inputOption=[]
inputOption = ["Entry"]
formatList = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
userRightList =["labeled-for-reuse-with-modifications","labeled-for-reuse","labeled-for-noncommercial-reuse-with-modification","labeled-for-nocommercial-reuse"]
languageList = ["Arabic", "Chinese (Simplified)", "Chinese (Traditional)", "Czech", "Danish", "Dutch", "English", "Estonian. Finnish", "French", "German", "Greek", "Hebrew", "Hungarian", "Icelandic", "Italian", "Japanese", "Korean", "Latvianm", "Lithuanian", "Norwegian", "Portuguese", "Polish", "Romanian", "Russian", "Spanish", "Swedish", "Turkish"]
sizeList =["large", "medium", "icon", ">400*300", ">640*480", ">800*600", ">1024*768", ">2MP", ">4MP", ">6MP", ">8MP", ">10MP", ">12MP", ">15MP", ">20MP", ">40MP", ">70MP"]

    
Menu = Tk() #Initialise Tkinter Window
Menu.title("Google Images/GIF Downloader Preview Mode")         #Set Title of Window

showText = Label(Menu,text = "Choose an Option")
showText.grid(row=1, column=2,pady=5)
suggestText = Label(Menu,text = "Get Keywords Suggestions")
suggestText.grid(row=1, column=3)
keywordsEntryText = Label(Menu,text = "Enter the keywords")
keywordsEntryText.grid(row=2, column=1)
keywordsExampleText = Label(Menu,text = "Example: Supergirl, Donald Trump")
keywordsExampleText.grid(row=3, column=2)
otherEntryText = Label(Menu,text = "Enter the other arguments")
otherEntryText.grid(row=4, column=1)
otherEntryText = Label(Menu,text = "Example: limit 20 language czech")
otherEntryText.grid(row=5, column=2)

keywordsEntry = Entry(bd =5, width=45)             #Used to collect What item to search for by user ("Superman", "Donald Trump") etc
keywordsEntry.grid(row=2, column=2)
otherEntry = Entry(bd =5, width=45)                #Used to collect other variables (Limit:"20", Language:"Czech") et
otherEntry.grid(row=4, column=2,pady=5)

commandsButton = Button(text ="Show commands", command = getCommands,bg="white",fg="black",justify=CENTER)
commandsButton.grid(row=7, column=2,columnspan=5,pady=5)
previewButton = Button(text ="Preview", command = previewActivity,bg="white",fg="blue",justify=CENTER)
previewButton.grid(row=8, column=2,columnspan=5,pady=5)
normalButton = Button(text ="Normal Download", command = normalActivity,bg="gray",fg="white",justify=CENTER)  #Configure Buttons
normalButton.grid(row=9, column=2,columnspan=5,pady=5)
placeholderButton = Button(text="???")
placeholderButton.grid(row=10, column=2,columnspan=5,pady=5)
suggestButton = Button(text="Suggest")
suggestButton.grid(row=2, column=3,columnspan=5)

Menu.mainloop()



