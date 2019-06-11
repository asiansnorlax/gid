from tkinter import *
import os
import tkinter.messagebox
from PIL import ImageTk, Image
import requests, json
import shutil
from google_images_download import googleimagesdownload as gID
#Display Commands
def showCommands():
    def clearCommands():
        showText.configure(text = "Choose an Option")
        forgetTkinterStuff([clearCommandsButton])                  #Clear old buttons
    stringArgs = "Usage: google_images_download.py"
    stringArgs +="\n[suffix_keywords {Word} (Denotes additional words added after main keyword)]"
    stringArgs +="\n[prefix_keywords {Word} (Denotes additional words added before main keyword)]"
    stringArgs +="\n[limit {Any positive integer} (Number of Images to be downloaded for each keyword)]"
    stringArgs +="\n[format {jpg,gif,png,bmp,svg,webp,ico} (Format/extension of the image)]"
    stringArgs +="\n[url {URL} (Download all images On the URL Page)]"
    stringArgs +="\n[image_directory {<image_directory>} (lets you specify a directory inside of the main directory (output_directory) in which the images will be saved)] [-n] [-d DELAY]"
    stringArgs +="\n[color {red,orange,yellow,green,teal,blue,purple,pink,white,gray,black,brown}]"
    stringArgs +="\n[color_type {full-color,black-and-white,transparent}]"
    stringArgs +="\n[usage_rights {labeled-for-reuse-with-modifications,labeled-for-reuse,labeled-for-noncommercial-reuse-with-modification,labeled-for-nocommercial-reuse}]"
    stringArgs +="\n[size {large,medium,icon,>400*300,>640*480,>800*600,>1024*768,>2MP,>4MP,>6MP,>8MP,>10MP,>12MP,>15MP,>20MP,>40MP,>70MP}]"
    stringArgs +="\n[type {face,photo,clipart,line-drawing,animated}]"
    stringArgs +="\n[time {past-24-hours,past-7-days,past-month,past-year}]"
    stringArgs +="\n[aspect_ratio {tall,square,wide,panoramic}]"
    stringArgs +="\n[print_size {True/False} (Prints the size of the images on the console)]"
    stringArgs +="\n[metadata {True/False} (Prints the metada of the image on the console)]"
    stringArgs +="\n[extract_metadata {True/False} (Save metadata of all the downloaded images in a JSON file)]"
    stringArgs +="\n[thumbnail or thumbnail_only {True/False}]"
    stringArgs +="\n[language {Arabic,Chinese Simplified),Chinese (Traditional,Czech,Danish,Dutch,English,Estonian,Finnish,French,German"
    stringArgs +="\nGreek,Hebrew,Hungarian,Icelandic,Italian,Japanese,Korean,Latvian,Lithuanian,Norwegian,Portuguese,Polish,Romanian,Russian,Spanish,Swedish,Turkish}]"
    stringArgs +="\n[prefix {Word} (A word that you would want to prefix in front of actual image name)]"
    stringArgs +="\n[safe_search {True/False} (Searches for images with the Safe Search filter On)]"
    stringArgs +="\n[no_numbering {True/False} (If true, the script does not add ordered numbering as prefix to the images it downloads)]"
    stringArgs +="\n[of OFFSET] [nd] [sil]"
    showText.configure(text=stringArgs)
    clearCommandsButton = Button(text="Clear Commands", command = clearCommands,bg="black",fg="white")             #Button to Clear Commands
    clearCommandsButton.grid(row=7, column=3,columnspan=5,pady=5)
#Check for valid keywords entered, returns True is keywords are entered, False if Entry is blank
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
        
#Split input String into array depending on the second input. 
def splitString(string, splitType):
    return string.split(splitType)

#Show Message in Tkinter on separate Message Box
def showMessageBox(messageTitle,string):
    tkinter.messagebox.showinfo(messageTitle,string)
    
#Delete char in string    
def stringRemoveChar(string, removeChar):
    for i in removeChar:
        string = string.replace(i, '')
    return string

#Function that uses Google Images Download Code to download Images
def download():
    global absolute_image_paths, Records, keywordString
    response = gID()
    absolute_image_paths = response.download(Records)
    
#Collect All Arguments from the GUI, collate it into a dictionary List and returns it
def formArguments():
    entry = keywordsEntry.get()                                             #Get keywords from keywords entry
    #entry = stringRemoveChar(entry,' ')                                    #Remove All spaces
    otherEntries = otherEntry.get()                                         #Get other Arguments from arguments entry
    if otherEntries !="":                                                   #Check if Entry is null
        if ',' in otherEntries:                                             
            otherEntries = stringRemoveChar(otherEntries, ',')              #Remove commas so search queries does not contain commas
        otherEntriesArray = splitString(otherEntries , ' ')                 #Separate variables
        for i in range(0,(len(otherEntriesArray))//2):
            Records[otherEntriesArray[i*2]] = otherEntriesArray[(i*2) +1]   #E.g [0] = format, [1] = jpg, [2] = size, [3] = large
    if "limit" not in Records:                                              #Set Limit to 5 if limit is not set 
        Records['limit'] = "5"
    Records['keywords'] = entry
    return Records
def clearActivity():
    global keywordString
    keywordsEntry.delete(0,END)
    keywordString = ""
#Show Keyword Suggestion based on the Current Keyword
def suggestKeywordActivity():
    #Once pressed, selected suggested keyword will overwrite the current keyword entry. Previous keywords entered will not be affected
    def confirmSuggestion():
        global keywordString
        keywordsEntry.delete(0,END)                                             #Clear Everything in Keyword Entry Box
        if not keywordString:   #If there are no previous keywords, Populate Entry box with Suggested Keyword
            keywordString = elementShown.get()                                  #Clear Everything in Keyword Entry Box
            keywordsEntry.insert(0,elementShown.get())                          #Populate Entry Box with the Keywords that user has chosen from suggested keywords
        else:                   #There are previous keywords, Populate Entry box with Previous Keywords + Suggested Keyword
            keywordString = keywordString + ',' + elementShown.get()            #Update KeywordString with latest Keyword            
            keywordsEntry.insert(0,keywordString)                               #Populate Entry Box with the Keywords that user has chosen from suggested keywords
        forgetTkinterStuff([keywordSuggestionMenu, confirmSuggestionButton])    #Clear tkinter stuff so they wont stack ontop of one another
    global keywordString
    keyword = keywordsEntry.get() 
    keywordStatus = checkForKeywords()
    if keywordStatus ==True:                                                    #Check if keywords Entry is not Empty
        if keywordString != "":                                                 #Removes the Previous keyword(s) from current string
            keyword = keyword[len(keywordString):]                                      #So only Current String is Searched
        URL="http://suggestqueries.google.com/complete/search?client=firefox&q="
        URL += keyword
        headers = {'User-agent':'Mozilla/5.0'}
        response = requests.get(URL, headers=headers)
        result = json.loads(response.content.decode('utf-8'))
        if result[1]:                                                           #If Searched Query has returned Results
            elementShown = StringVar(Menu)                                      #Holds a String
            elementShown.set(result[1][0])                                      #Sets the Default string to be shown in drop down Menu
            keywordSuggestionMenu = OptionMenu(Menu,elementShown, *result[1])   #Configure drop Down Menu
            keywordSuggestionMenu.grid(row=2, column=4,columnspan=2)
            confirmSuggestionButton = Button(text="Confirm suggestion", command = confirmSuggestion,bg="black",fg="white") #Configure Button to confirm keyword Suggestion
            confirmSuggestionButton.grid(row=3, column=4,columnspan=2)
        else:                                                           #If Searched Query has no Results
            showMessageBox("No Results", "Error! No results for current keyword"+keywordsEntry.get()+". Please Try another Keyword")
            keywordsEntry.delete(0,END)                                 #Clear Entry. No results found for current keyword Entry
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword") #Show Error Message when Keywords entry is empty

#Normal Google Image Downloader
#Takes in Argument from the GUI and downloads the corresponding Image(s)
def normalActivity():
    keyword = checkForKeywords()
    if keyword == True:                                                 #Check if keywords Entry is not Empty
        Menu.title("Google Images/GIF Downloader")
        Records = formArguments()                                       #Collate all Arguments taken from GUI into a Dictionary List
        download()                                                      #Function to Download images
        showMessageBox("Program Finish", "The download has finished")
        Records={}                                                      #Clears all User Arguments      
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword") #Show Error Message when Keywords entry is empty
    
#Modify Arguments based on User's choice (Keep or don't keep Image)
def formPreviewedArguments():
    global itemsToBeKept, Records
    items = ""
    for i in itemsToBeKept:
        items = items + ',' + i                                         #Convert Array Into String
    keywordsEntry.delete(0,END)                                         #Clear Everything in Keyword Entry Box
    keywordsEntry.insert(0,items[1:])                                   #Populate Entry Box Only with the Keywords that user has Wants from the Preview
    Records = {}
    Records = formArguments()                     
    Records['thumbnail_only']=False                                     #Do not download Thumbnails
     
#Download only images(keywords) that the user wants to keep
def downloadPreviewItems():
    global previewQueue, previewQueueCounter, itemsToBeKept, Records
    if len(itemsToBeKept) == 0:                                         #User kept NO items, no download is required
        showMessageBox("No Downloads", "Preview is Over. All items were rejected, going back to Main Menu")
    else:                                                               #User kept Some or All items, Download is required
        formPreviewedArguments() 
        showMessageBox("Download Items", "All items have been previewed. Downloading Items now!")
        download()
#Delete Thumbnail and Preview Folder to tidy up and Neaten Download Folder
def clearPreviewFiles():
    if Records['output_directory']==None and Records['image_directory']==None:                  #If Image and Output directory are not specified
        #shutil.rmtree(dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter])                
        shutil.rmtree(dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail") 
    elif Records['output_directory']!=None and Records['image_directory']==None:                #If Image directory is specified and output directory is not
        #shutil.rmtree(dir_path +"\\"+Records['output_directory']+'\\'+previewQueue[previewQueueCounter])                
        shutil.rmtree(dir_path +"\\"+Records['output_directory']+'\\'+previewQueue[previewQueueCounter]+" - thumbnail") 
    elif Records['output_directory']==None and Records['image_directory']!=None:                #If Image directory is not specified and output directory is
        #shutil.rmtree(dir_path +"\downloads"+'\\'+Records['image_directory'])                
        shutil.rmtree(dir_path +"\downloads"+'\\'+Records['image_directory']+" - thumbnail") 
    else:                                                                                       #If Image and Output Directory are specified
        #shutil.rmtree(dir_path +"\\"+Records['output_directory']+'\\'+Records['image_directory'])
        shutil.rmtree(dir_path +"\\"+Records['output_directory']+'\\'+Records['image_directory']+" - thumbnail")

#Preview Pictures of keywords that user has entered. 
def previewActivity():
    #Increase Preview Counter, Put Item that User wants to keep into to be downloaded queue, Delete thumbnail folder, Go back to Preview Activity
    def previewItemKeep():
        global previewQueueCounter, dir_path, previewQueue, itemsToBeKept
        itemsToBeKept.append(previewQueue[previewQueueCounter])
        clearPreviewFiles()             #Clear Preview Directory
        previewQueueCounter+=1              #Increase the counter
        previewActivity()
        
    #Increase Preview Counter, Delete thumbnail folder, Go back to Preview Activity
    def previewItemDelete():
        global previewQueueCounter, previewQueue, dir_path
        clearPreviewFiles()             #Clear Preview Directory
        previewQueueCounter+=1              #Increase the counter
        previewActivity()
        
    global img, previewQueue, previewQueueCounter, itemsToBeKept, absolute_image_paths, tempRecords, canv, previewMenu, dir_path
    keyword = checkForKeywords()
    if keyword == True:                                                     #Check if keywords Entry is not Empty
        #-------------------------------------------------------First Run, Initialise Values-------------------------------------------------------#
        if previewQueueCounter == 0:                                        #Initialise Values
            Records = formArguments()                                       #Get Arguments from GUI
            if ',' in Records["keywords"]:                                  #Check for more than 1 keywords.
                previewQueue = splitString(Records["keywords"],',')         #Store all keywords(String, seperated by a comma) into an Array
            else:
                previewQueue.append(Records["keywords"])
            previewMenu = Toplevel()                                        #Initialise New Tkinter Window
            previewMenu.title("Google Images Preview")                      #Set Title of Window
            Records = formArguments()
            tempRecords = Records                                           #Hold Current Arguments in temp Array
            canv = Canvas(master=previewMenu, width=500, height=300, bg='white')
            canv.grid(row=2, column=3)
            itemKeepButton = Button(master =previewMenu, text ="This is what i am looking for", command = previewItemKeep,bg="blue",fg="white",justify=CENTER) #Button to keep Search Item in Download Queue
            itemKeepButton.grid(row=8, column=2,columnspan=5,pady=5)
            itemDeleteButton = Button(master =previewMenu,text ="I don't want this", command = previewItemDelete,bg="gray",fg="white",justify=CENTER)         #Button to delete Search Item in Download Queue
            itemDeleteButton.grid(row=9, column=2,columnspan=5,pady=5)
        #-------------------------------------------------------Preview Items-------------------------------------------------------#
        if previewQueueCounter < len(previewQueue): #Check if there are still items to preview
            Records = tempRecords
            Records['keywords'] = previewQueue[previewQueueCounter]
            Records['thumbnail_only']=True
            Records['limit'] = "12"                                         #Download 12 thumbnails for each Item in case some are duds
            download()                                                      #Download Thumbnails for preview Purposes
            #Get Image Path, and open Image
            dir_path = os.path.dirname(os.path.realpath(__file__))          #Current Working Directory
            thumbnailName = os.listdir(dir_path+"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail")[0]
            thumbnailPath = dir_path +"\downloads"+'\\'+previewQueue[previewQueueCounter]+" - thumbnail"+'\\'+thumbnailName
            img = ImageTk.PhotoImage(Image.open(thumbnailPath))             #Get Preview Image path
            canv.create_image(10, 10, anchor=NW, image=img)                 #Open Preview Image from Directory
            canv.img=img                                                              
        #-------------------------------------------------------Download Preview Items-------------------------------------------------------#
        else:                                                               #No more items to preview, Time to download Kept Items
            downloadPreviewItems()                                          #Get Modified Arguments that accounts for the Items that the User Kept and Not Kept
            Records , tempRecords, items, itemsToBeKept = {} , {} , "" , [] #Reset all
            previewQueue, previewQueueCounter = [], 0
            showMessageBox("Preview Over", "Activity is done! The preview window will be closed!")    
            previewMenu.destroy()                                           #Destroy Preview Window
    else:showMessageBox("No keywords", "Error! Please Enter a Keyword")     #Show Error Message when Keywords entry is empty
    
#-----------------------------------------------------------------------Main Program-----------------------------------------------------------------------#
keywordString = ""            #String Used to record the previous keywords entered. This string is minused from the total keywords so Current Keywords can be properly queried
Records = {}                  #Dictionary used to store all the Arguments to be send into google downloader
tempRecords = {}              #Dictionary used to hold on to the Original arguments for preview Purposes 
#suggestionMenuDuplicate = False         #Used to determine whether there is duplicate Suggestion Drop Down Menu
abc = 0
inputOption = ["Entry"]
previewQueue = []             #Array used to store the Keywords queue for Preview Purposes
previewQueueCounter = 0       #Used to note the current preview Queue
itemsToBeKept = []            #Array used to store the Items that the user wants to download after Preview (User may not want certain Items after Preview)
formatList = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
userRightList =["labeled-for-reuse-with-modifications","labeled-for-reuse","labeled-for-noncommercial-reuse-with-modification","labeled-for-nocommercial-reuse"]
languageList = ["Arabic", "Chinese (Simplified)", "Chinese (Traditional)", "Czech", "Danish", "Dutch", "English", "Estonian. Finnish", "French", "German", "Greek", "Hebrew", "Hungarian", "Icelandic", "Italian", "Japanese", "Korean", "Latvianm", "Lithuanian", "Norwegian", "Portuguese", "Polish", "Romanian", "Russian", "Spanish", "Swedish", "Turkish"]
sizeList =["large", "medium", "icon", ">400*300", ">640*480", ">800*600", ">1024*768", ">2MP", ">4MP", ">6MP", ">8MP", ">10MP", ">12MP", ">15MP", ">20MP", ">40MP", ">70MP"]
#-------------------------------------------------------------Set up and Configure Tkinkter GUI-------------------------------------------------------------#  
Menu = Tk() #Initialise Tkinter Window
Menu.title("Google Images Downloader")         #Set Title of Window
#------------------------------------------------------------Tkinter Text------------------------------------------------------------#
showText = Label(Menu,text = "Choose an Option")
showText.grid(row=1, column=2)
suggestText = Label(Menu,text = "Get Keywords Suggestions")
suggestText.grid(row=2, column=3)
keywordsEntryText = Label(Menu,text = "Enter the keywords *")                       #Keyword Entry Label
keywordsEntryText.grid(row=3, column=1)
keywordsExampleText = Label(Menu,text = "Example: Supergirl, Donald Trump")         #Keyword Hint
keywordsExampleText.grid(row=4, column=2)
clearText = Label(Menu,text = "Clear Entry and History")                            #Keyword Hint
clearText.grid(row=4, column=3)
otherEntryText = Label(Menu,text = "Enter the arguments")                           #Other Arguments Entry Label
otherEntryText.grid(row=5, column=1)
otherEntryText = Label(Menu,text = "Example: limit 20 language czech format jpg")   #Other Arguments Hint
otherEntryText.grid(row=6, column=2)
otherEntryText1 = Label(Menu,text = "Default limit is 5")                           #Default Limit is 5 images
otherEntryText1.grid(row=7, column=1)
#------------------------------------------------------------Tkinter Entry Box------------------------------------------------------------#
keywordsEntry = Entry(bd =5, width=45)                                          #Used to collect What item to search for by user (Superman,Donald Trump) etc
keywordsEntry.grid(row=3, column=2)
otherEntry = Entry(bd =5, width=45)                                             #Used to collect other Arguments (limit 20 language czech ) etc
otherEntry.grid(row=5, column=2,pady=5)
#------------------------------------------------------------Tkinter Button------------------------------------------------------------#
suggestButton = Button(text="Suggest", command = suggestKeywordActivity,bg="black",fg="white")                  #Button to show keyword Suggestion for entered keyword
suggestButton.grid(row=3, column=3,columnspan=2)
ClearButton = Button(text="Clear", command = clearActivity,bg="red",fg="white")                      #Button to clear Entry and History
ClearButton.grid(row=5, column=3,columnspan=2)
commandsButton = Button(text ="Show commands", command = showCommands,bg="white",fg="black",justify=CENTER)     #Button to show Commands
commandsButton.grid(row=7, column=2,columnspan=5,pady=5)
previewButton = Button(text ="Preview", command = previewActivity,bg="blue",fg="white",justify=CENTER)          #Button for starting Picture Preview Mode
previewButton.grid(row=8, column=2,columnspan=5,pady=5)
normalButton = Button(text ="Normal Download", command = normalActivity,bg="gray",fg="white",justify=CENTER)    #Button for normal image Download
normalButton.grid(row=9, column=2,columnspan=5,pady=5)

Menu.mainloop()
