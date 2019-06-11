from tkinter import *
import os
import tkinter.messagebox
from PIL import ImageTk, Image
import requests, json
import shutil
from google_images_download import googleimagesdownload as gID
def getCommands():
    def clearCommands():
        showText.configure(text = "Choose an Option")
        forgetTkinterStuff([clearCommandsButton])                  #clear old buttons
    stringArgs = "usage: google_images_download.py [h] [k KEYWORDS] [kf KEYWORDS_FROM_FILE]"
    stringArgs +="\n                                 [sk SUFFIX_KEYWORDS] [pk PREFIX_KEYWORDS]"
    stringArgs +="\n                                 [l LIMIT]"
    stringArgs +="\n                                 [f {jpg,gif,png,bmp,svg,webp,ico}] [u URL]"
    stringArgs +="\n                                 [x SINGLE_IMAGE] [-o OUTPUT_DIRECTORY]"
    stringArgs +="\n                                 [i IMAGE_DIRECTORY] [-n] [-d DELAY]"
    stringArgs +="\n                                 [co {red,orange,yellow,green,teal,blue,purple,pink,white,gray,black,brown}]"
    stringArgs +="\n                                 [ct {full-color,black-and-white,transparent}]"
    stringArgs +="\n                                 [r {labeled-for-reuse-with-modifications,labeled-for-reuse,labeled-for-noncommercial-reuse-with-modification,labeled-for-nocommercial-reuse}]"
    stringArgs +="\n                                 [s {large,medium,icon,>400*300,>640*480,>800*600,>1024*768,>2MP,>4MP,>6MP,>8MP,>10MP,>12MP,>15MP,>20MP,>40MP,>70MP}]"
    stringArgs +="\n                                 [es EXACT_SIZE]"
    stringArgs +="\n                                 [t {face,photo,clipart,line-drawing,animated}]"
    stringArgs +="\n                                 [w {past-24-hours,past-7-days,past-month,past-year}]"
    stringArgs +="\n                                 [wr TIME_RANGE]"
    stringArgs +="\n                                 [a {tall,square,wide,panoramic}]"
    stringArgs +="\n                                 [si SIMILAR_IMAGES] [ss SPECIFIC_SITE] [-p]"
    stringArgs +="\n                                 [ps] [pp] [m] [e] [st SOCKET_TIMEOUT]"
    stringArgs +="\n                                 [th] [tho]"
    stringArgs +="\n                                 [la {Arabic,Chinese Simplified),Chinese (Traditional,Czech,Danish,Dutch,English,Estonian,Finnish,French,German"
    stringArgs +="\n                                 Greek,Hebrew,Hungarian,Icelandic,Italian,Japanese,Korean,Latvian,Lithuanian,Norwegian,Portuguese,Polish,Romanian,Russian,Spanish,Swedish,Turkish}]"
    stringArgs +="\n                                 [pr PREFIX] [px PROXY] [cd CHROMEDRIVER]"
    stringArgs +="\n                                 [ri] [sa] [nn] [of OFFSET] [nd] [sil]"
    stringArgs +="\n                                 [is SAVE_SOURCE]"
    showText.configure(text=stringArgs)
    clearCommandsButton = Button(text="Clear Commands", command = clearCommands,bg="black",fg="white")             #Button to Clear keyword Suggestion
    clearCommandsButton.grid(row=7, column=3,columnspan=5,pady=5)
#Check for valid keywords entered, returns True is keywords are entered, False if not
def checkForKeywords():
    keywords = keywordsEntry.get()
    keywords = stringRemoveChar(keywords,' ')
    if not keywords:
        return False
    else:
        return True;
#Forgets Tkinter items in the input array
def forgetTkinterStuff(stuff):
    for thing in stuff:
        thing.grid_forget()
#Split String into array depending on the second input. 
def splitString(string, splitType):
    return string.split(splitType)

#Show Message in Tkinter on separate Message Box
def showMessageBox(messageTitle,string):
    tkinter.messagebox.showinfo(messageTitle,string)
    
def stringRemoveChar(string, removeChar):
    for i in removeChar:
        string = string.replace(i, '')
    return string
#Function that uses Google Images Download Code to download Images
def download():
    global absolute_image_paths
    response = gID()
    absolute_image_paths = response.download(Records)
#Collect All Arguments from the GUI, collate it into a dictionary List and returns it
def formArguments():
    entry = keywordsEntry.get()     #Get keywords from keywords entry
    entry = stringRemoveChar(entry,' ') #Remove All spaces
    otherEntries = otherEntry.get() #Get other Arguments from arguments entry
    if otherEntries !="":           #Check if Entry is null
        if ',' in otherEntries:
            otherEntries = stringRemoveChar(otherEntries, ',')
        otherEntriesArray = splitString(otherEntries , ' ') #Separate variables
        for i in range(0,(len(otherEntriesArray))//2):
            Records[otherEntriesArray[i*2]] = otherEntriesArray[(i*2) +1]
    Records['keywords'] = entry
    return Records

#Show Keyword Suggestion based on the Current Keyword
def suggestKeywordActivity():
    #Once pressed, selected suggested keyword will overwrite the current keyword entry. Previous keywords entered will not be affected
    def confirmSuggestion():
        global keywordString
        if not keywordString:
            keywordString = elementShown.get()
            keywordsEntry.delete(0,END)                     #Clear Everything in Keyword Entry Box
            keywordsEntry.insert(0,elementShown.get())      #Populate Entry Box with the Keywords that user has chosen from suggested keywords
        else:
            keywordString = keywordString + ',' + elementShown.get()    #Update KeywordString with latest Keyword
            keywordsEntry.delete(0,END)                     #Clear Everything in Keyword Entry Box
            keywordsEntry.insert(0,keywordString)           #Populate Entry Box with the Keywords that user has chosen from suggested keywords
        forgetTkinterStuff([keywordSuggestionMenu, confirmSuggestionButton])  #Clear tkinter stuff so they wont stack ontop of one another        
    global keywordString,suggestionMenuDuplicate
    #if suggestionMenuDuplicate == True:
     #   forgetTkinterStuff([keywordSuggestionMenu])
      #  suggestionMenuDuplicate = False   
    keyword = checkForKeywords()
    if keyword ==True:                   #Check if keywords Entry is not Empty
        if keywordString != "":                                                      #Removes the Previous keyword(s) from current string
            keyword = stringRemoveChar(keyword, [keywordString, ','])                #So only Current String is Searched
        URL="http://suggestqueries.google.com/complete/search?client=firefox&q="
        URL += keywordsEntry.get()
        headers = {'User-agent':'Mozilla/5.0'}
        response = requests.get(URL, headers=headers)
        result = json.loads(response.content.decode('utf-8'))
        print(result)
        elementShown = StringVar(Menu)                                   #Holds a String
        elementShown.set(result[1][0])                                   #Set default string to be shown in drop down Menu
        keywordSuggestionMenu = OptionMenu(Menu,elementShown, *result[1])    #Configure drop Down Menu
        keywordSuggestionMenu.grid(row=2, column=4,columnspan=2)
        confirmSuggestionButton = Button(text="Confirm suggestion", command = confirmSuggestion,bg="black",fg="white") #Configure Button to confirm keyword Suggestion
        confirmSuggestionButton.grid(row=3, column=4,columnspan=2)
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword")  #Show Error Message when Keywords entry is empty

#Normal Google Image Downloader
#Takes in Argument from the GUI and downloads the corresponding Image(s)
def normalActivity():
    global keywordString
    #buttonList =[previewButton, normalButton, placeholderButton, commandsButton, keywordsEntryText, keywordsEntry, otherEntryText, otherEntry, otherEntryText, keywordsExampleText]
    #forgetTkinterStuff(buttonList) #clear old buttons
    keyword = checkForKeywords()
    if keyword == True:                   #Check if keywords Entry is not Empty
        Menu.title("Google Images/GIF Downloader")
        Records = formArguments()           #Collate all Arguments taken from GUI into a Dictionary List
        print(Records)
        if "limit" not in Records:          #If no limits are set, Set Download Limit as 5 Images
            Records['limit'] = "5"
        download()                      #Function to Download images
        print(absolute_image_paths,"Path")
        print("\n",absolute_image_paths[0])
        #print("\n",absolute_image_paths[0][keywordsEntry.get()][0])     #keywordsEntry.get() have to be splitString for multiple keywords
        showMessageBox("Program Finish", "The download has finished")
        keywordString=""                    #Clear Entry String
        Records={}                          #Clear User Input
        
        
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword")  #Show Error Message when Keywords entry is empty

    
def previewActivity():
        #Increase Preview Counter, Go back to Preview Activity
    def previewItemKeep():
        global previewQueueCounter, dir_path, previewQueue
        itemsToBeKept.append(previewQueue[previewQueueCounter])
        shutil.rmtree(dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail")
        previewQueueCounter+=1              #Increase the counter
        previewActivity()
    #Increase Preview Counter, Put Item that User does not want to keep into not to be downloaded queue, Go back to Preview Activity
    def previewItemDelete():
        global previewQueueCounter, itemsToBeKept, previewQueue, dir_path
        shutil.rmtree(dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail")
        previewQueueCounter+=1              #Increase the counter
        previewActivity()
    #global img      #So Image is not cleared by stack
    global img1, previewQueue, previewQueueCounter, itemsToBeKept, absolute_image_paths, tempRecords, canv, previewMenu, dir_path
    keyword = checkForKeywords()
    if keyword == True:                   #Check if keywords Entry is not Empty
        if previewQueueCounter == 0:                #Initialise Values
            Records = formArguments()               #Get Arguments from GUI
            #if ' ' in Records["keywords"]:          #Remove spaces in Keywords
             #   Records["keywords"]=stringRemoveChar(Records["keywords"], ' ')
            if ',' in Records["keywords"]:          #Check for more than 1 keywords.
                previewQueue = splitString(Records["keywords"],',')
            else:
                previewQueue.append(Records["keywords"])

            print (previewQueue,'previewQueue') 
            previewMenu = Toplevel() #Initialise Tkinter Window
            previewMenu.title("Google Images Preview")         #Set Title of Window
            showText.configure(text="Picture Preview")
            showText.grid(row=8, column=3,columnspan=3,pady=5)
            Records = formArguments()
            tempRecords = Records
            canv = Canvas(master=previewMenu, width=400, height=250, bg='white')
            canv.grid(row=2, column=3)
            itemKeepButton = Button(master =previewMenu, text ="This is what i am looking for", command = previewItemKeep,bg="white",fg="blue",justify=CENTER) #Button to keep Search Item in Download Queue
            itemKeepButton.grid(row=8, column=2,columnspan=5,pady=5)
            itemDeleteButton = Button(master =previewMenu,text ="I don't want this", command = previewItemDelete,bg="gray",fg="white",justify=CENTER)         #Button to delete Search Item in Download Queue
            itemDeleteButton.grid(row=9, column=2,columnspan=5,pady=5)

        if previewQueueCounter < len(previewQueue): #Check if there are still items to preview
            Records = tempRecords
            Records['keywords'] = previewQueue[previewQueueCounter]
            Records['thumbnail_only']=True
            Records['limit'] = "5"
            download()
            #Get Image Path, and open
            
            print(absolute_image_paths[0][previewQueue[previewQueueCounter]][0])
            dir_path = os.path.dirname(os.path.realpath(__file__))  #C:\Users\PHOEN\AppData\Local\Programs\Python\Python37-32\Projects\PSB OSD
            print(dir_path)
            thumbnailName = os.listdir(os.path.dirname(os.path.realpath(__file__))+"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail")[0]
            print(thumbnailName)
            thumbnailPath = dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail"+'\\'+thumbnailName
            img = ImageTk.PhotoImage(Image.open(thumbnailPath))  # PIL solution
            canv.create_image(10, 10, anchor=NW, image=img)
            canv.img=img
        else:
            print(tempRecords,'temp')
            if len(itemsToBeKept) == 0:
                showMessageBox("No Downloads", "Preview is Over. All items were rejected, going back to Main Menu")
                Records , tempRecords = {} , {}
            elif len(itemsToBeKept) == len(tempRecords['keywords']):
                showMessageBox("Download Items", "Preview is Over. Downloading Items now!")
                Records = formArguments()
                print(Records)
                download()
                Records , tempRecords = {} , {}
            else:
                Records = formArguments()
                print(Records)
                for i in itemsToBeKept:
                    Records['keywords'] = itemsToBeKept
                showMessageBox("Download Items", "Preview is Over. Downloading Items now!")
                download()
                Records , tempRecords = {} , {}
            previewMenu.destroy()       
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword")  #Show Error Message when Keywords entry is empty
    

    
#-----------------------------------------------------------------------Main Program-----------------------------------------------------------------------#
keywordString = ""            #String Used to record the keywords entered
Records = {}                  #Dictionary used to store all the Arguments to be send into google downloader
tempRecords = {}              #Dictionary used to store the Original arguments 
#suggestionMenuDuplicate = False         #Used to determine whether there is duplicate Suggestion Drop Down Menu
inputOption = ["Entry"]
previewQueue = []             #Array used to store the Keywords queue for Preview Purposes
previewQueueCounter = 0       #Used to note the current preview Queue
itemsToBeKept = []         #Array used to store the Items that the user do not want to download after Preview (User may no want certain Items after Preview)
formatList = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
userRightList =["labeled-for-reuse-with-modifications","labeled-for-reuse","labeled-for-noncommercial-reuse-with-modification","labeled-for-nocommercial-reuse"]
languageList = ["Arabic", "Chinese (Simplified)", "Chinese (Traditional)", "Czech", "Danish", "Dutch", "English", "Estonian. Finnish", "French", "German", "Greek", "Hebrew", "Hungarian", "Icelandic", "Italian", "Japanese", "Korean", "Latvianm", "Lithuanian", "Norwegian", "Portuguese", "Polish", "Romanian", "Russian", "Spanish", "Swedish", "Turkish"]
sizeList =["large", "medium", "icon", ">400*300", ">640*480", ">800*600", ">1024*768", ">2MP", ">4MP", ">6MP", ">8MP", ">10MP", ">12MP", ">15MP", ">20MP", ">40MP", ">70MP"]
  
Menu = Tk() #Initialise Tkinter Window
Menu.title("Google Images Downloader")         #Set Title of Window
#---------------Tkinter Text---------------#
showText = Label(Menu,text = "Choose an Option")
showText.grid(row=1, column=2,pady=5)
suggestText = Label(Menu,text = "Get Keywords Suggestions")
suggestText.grid(row=1, column=3)
keywordsEntryText = Label(Menu,text = "Enter the keywords *")
keywordsEntryText.grid(row=2, column=1)
keywordsExampleText = Label(Menu,text = "Example: Supergirl, Donald Trump")
keywordsExampleText.grid(row=3, column=2)
otherEntryText = Label(Menu,text = "Enter the arguments")
otherEntryText.grid(row=4, column=1)
otherEntryText = Label(Menu,text = "Example: limit 20 language czech")
otherEntryText.grid(row=5, column=2)
#---------------Tkinter Entry Box---------------#
keywordsEntry = Entry(bd =5, width=45)             #Used to collect What item to search for by user ("Superman", "Donald Trump") etc
keywordsEntry.grid(row=2, column=2)
otherEntry = Entry(bd =5, width=45)                #Used to collect other variables (Limit:"20", Language:"Czech") et
otherEntry.grid(row=4, column=2,pady=5)
#---------------Tkinter Button---------------#
commandsButton = Button(text ="Show commands", command = getCommands,bg="white",fg="black",justify=CENTER)
commandsButton.grid(row=7, column=2,columnspan=5,pady=5)
previewButton = Button(text ="Preview", command = previewActivity,bg="white",fg="blue",justify=CENTER)          #Button for starting Picture Preview Mode
previewButton.grid(row=8, column=2,columnspan=5,pady=5)
normalButton = Button(text ="Normal Download", command = normalActivity,bg="gray",fg="white",justify=CENTER)    #Button for normal image Download
normalButton.grid(row=9, column=2,columnspan=5,pady=5)
#placeholderButton = Button(text="???")
#placeholderButton.grid(row=10, column=2,columnspan=5,pady=5)
suggestButton = Button(text="Suggest", command = suggestKeywordActivity,bg="black",fg="white")                         #Button to show keyword Suggestion
suggestButton.grid(row=2, column=3,columnspan=2)
Menu.mainloop()



