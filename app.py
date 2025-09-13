import requests
import json
from os import listdir
from tkinter import *
from tkinter import ttk

tk = Tk(className=" Steam Game Picker")
tk.geometry("500x500")

def getKey(keyFile):
    with open(keyFile, "r") as file:
        key = file.readline()
    return key

def saveInfo(user, data):
    with open("./steam-picker/users/" + user + ".json", "w") as file:
        json.dump(data, file)

def loadInfoFromFile(user):
    with open("./steam-picker/users/" + user + ".json", "r") as file:
        data = json.load(file)
    return data

class UserData:
    def __init__(self):
        self.id = 0
    def setID(self, steamID):
        self.id = steamID
    def getID(self):
        return self.id

class MainScreen:
    def __init__(self):
        self.gameName = Label(tk)
        self.textPrompt = Label(tk)
        self.newGameButton = Button(tk)
        self.entryField = Entry(tk)
        self.confirm = Button(tk)
        self.deny = Button(tk)

        self.userData = UserData()
        self.saveToFile = False
    # clear the tkinter items from the screen for new screen scenes
    def destroyItems(self):
        self.gameName.destroy()
        self.textPrompt.destroy()
        self.newGameButton.destroy()
        self.entryField.destroy()
        self.confirm.destroy()
        self.deny.destroy()
    # first screen upon launching, gets steamid64
    def getIDScreen(self):
        self.destroyItems()

        self.textPrompt = ttk.Label(tk, text="enter steamid64 (decimal).")
        self.textPrompt.place(relx=0.5, rely=0.5, anchor="center")

        self.entryField = ttk.Entry(tk, width=20)
        self.entryField.place(relx=0.5, rely=0.6)

        self.confirm = ttk.Button(tk, text="Confirm", command=self.getIDInfo)
        self.confirm.place(relx=0.5, rely=0.7)
    def getIDInfo(self):
        self.userData.setID(self.entryField.get())
        self.destroyItems()

        # TODO: check if steamid64 is valid

        # if the id is in the files, prompt loading from it instead
        usersOnFile = listdir("./steam-picker/users/")
        if (self.userData.getID() + ".json" in usersOnFile):
            self.textPrompt = ttk.Label(tk, text="user info is currently saved to a local file. load it?\nthis will not call the steamweb api.")
            self.textPrompt.place(relx=0.5, rely=0.5, anchor="center")

            # yes loads it from a file
            self.confirm = ttk.Button(tk, text="Yes", command=self.loadFromFile)
            self.confirm.place(relx=0.4, rely=0.7)

            # no skips to prompting user to save info
            self.deny = ttk.Button(tk, text="No", command=self.saveInfoPrompt)
            self.deny.place(relx=0.6, rely=0.7)
        else:
            # if id is not in files, prompt user to save
            self.saveInfoPrompt()
    def saveInfoPrompt(self):
        self.destroyItems()
        self.textPrompt = ttk.Label(tk, text="save owned game information to local file?\nthis will update any info saved to local files, or create a file if there is none.")
        self.textPrompt.place(relx=0.5, rely=0.5, anchor="center")

        self.confirm = ttk.Button(tk, text="Yes", command=self.setSaveToFile)
        self.confirm.place(relx=0.4, rely=0.7)

        self.deny = ttk.Button(tk, text="No", command=self.callAPI)
        self.deny.place(relx=0.6, rely=0.7)
    def setSaveToFile(self):
        # this flags the system to know to save it to a file after it is retrieved from steamweb
        self.saveToFile = True
        self.callAPI()
    def callAPI(self):
        pass
    def loadFromFile(self):
        pass
    def main(self):
        self.destroyItems()

        self.gameName = ttk.Label(tk, text="Placeholder")
        self.gameName.place(relx=0.5, rely=0.3, anchor="center")

if __name__ == '__main__':
    # usersOnFile = listdir("./steam-picker/users/") # get the users in the users dir
    # # print(usersOnFile[0][:-5])
    # key = getKey("./steam-picker/steamweb.key") # get API key from file
    # print("enter steamid64 (decimal): ")
    # steamID = input()

    # loadFromFile = "\0"
    # if (steamID + ".json" in usersOnFile): # check if user id is already saved to a file to avoid api call
    #     loadFromFile = "\0"
    #     while (loadFromFile.lower() != "y" and loadFromFile.lower() != "n"):
    #         print("user info is currently saved to a local file. load it? (y/n)\n" \
    #         "(this is opposed to calling the steamweb api)")
    #         loadFromFile = input()

    # jsonData = {}
    # if (loadFromFile.lower() == "y"):
    #     jsonData = loadInfoFromFile(steamID)
    # else:
    #     saveToFile = "\0"
    #     while (saveToFile.lower() != "y" and saveToFile.lower() != "n"):
    #         print("save owned game information to local file? (y/n)")
    #         saveToFile = input()

    #     url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + key + "&steamid=" + steamID + "&include_appinfo=1&include_played_free_games=1&format=json"
    #     jsonData = requests.get(url).json()
        
    #     if (saveToFile.lower() == "y"):
    #         saveInfo(steamID, jsonData)
    
    # for game in jsonData["response"]["games"]:
    #     print(game["name"])

    mainScreen = MainScreen()

    mainScreen.getIDScreen()
    tk.mainloop()
    