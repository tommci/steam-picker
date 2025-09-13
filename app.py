import requests
import json
import random
from os import listdir
from tkinter import *
from tkinter import ttk

tk = Tk(className=" Steam Game Picker")
tk.geometry("500x400")

class UserData:
    def __init__(self):
        self.id = 0
        self.key = ""
        self.jsonData = {}
    def setID(self, steamID):
        self.id = steamID
    def getID(self):
        return self.id
    def setKey(self, keyFile):
        with open(keyFile, "r") as file:
            self.key = file.readline()
    def getKey(self):
        return self.key
    def setJSONData(self, data):
        self.jsonData = data
    def getJSON(self):
        return self.jsonData
    def saveInfo(self):
        with open("./users/" + self.id + ".json", "w") as file:
            json.dump(self.jsonData, file)
    def loadInfo(self):
        with open("./users/" + self.id + ".json", "r") as file:
            self.jsonData = json.load(file)

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
        self.entryField.place(relx=0.5, rely=0.6, anchor="center")

        self.confirm = ttk.Button(tk, text="Confirm", command=self.getIDInfo)
        self.confirm.place(relx=0.5, rely=0.7, anchor="center")
    def getIDInfo(self):
        self.userData.setID(self.entryField.get())
        self.destroyItems()

        # TODO: check if steamid64 is valid

        # if the id is in the files, prompt loading from it instead
        usersOnFile = listdir("./users/")
        if (self.userData.getID() + ".json" in usersOnFile):
            self.textPrompt = ttk.Label(tk, text="user info is currently saved to a local file. load it?\nthis will not call the steamweb api.")
            self.textPrompt.place(relx=0.5, rely=0.5, anchor="center")

            # yes loads it from a file
            self.confirm = ttk.Button(tk, text="Yes", command=self.loadFromFile)
            self.confirm.place(relx=0.4, rely=0.7, anchor="center")

            # no skips to prompting user to save info
            self.deny = ttk.Button(tk, text="No", command=self.saveInfoPrompt)
            self.deny.place(relx=0.6, rely=0.7, anchor="center")
        else:
            # if id is not in files, prompt user to save
            self.saveInfoPrompt()
    def saveInfoPrompt(self):
        self.destroyItems()
        self.textPrompt = ttk.Label(tk, text="save owned game information to local file?\nthis will update any info saved to local files, or create a file if there is none.")
        self.textPrompt.place(relx=0.5, rely=0.5, anchor="center")

        self.confirm = ttk.Button(tk, text="Yes", command=self.setSaveToFile)
        self.confirm.place(relx=0.4, rely=0.7, anchor="center")

        self.deny = ttk.Button(tk, text="No", command=self.callAPI)
        self.deny.place(relx=0.6, rely=0.7, anchor="center")
    def setSaveToFile(self):
        # this flags the system to know to save it to a file after it is retrieved from steamweb
        self.saveToFile = True
        self.callAPI()
    def callAPI(self):
        # get the api key from file system
        self.userData.setKey("./steamweb.key")
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + self.userData.getKey() + "&steamid=" + self.userData.getID() + "&include_appinfo=1&include_played_free_games=1&format=json"
        # TODO: check if the information was retrieved correctly
        self.userData.setJSONData(requests.get(url).json()) # set the json data
        if (self.saveToFile): # this would have been set earlier
            self.userData.saveInfo()
        
        self.main("Press the button below to select a random game from your library!")
    def loadFromFile(self):
        self.userData.loadInfo()
        self.main("Press the button below to select a random game from your library!")
    def main(self, gameName):
        self.destroyItems()

        self.gameName = ttk.Label(tk, text=gameName)
        self.gameName.place(relx=0.5, rely=0.4, anchor="center")

        self.newGameButton = ttk.Button(tk, text="Pick New Game", command=self.generateNewGame)
        self.newGameButton.place(relx=0.5, rely=0.6, anchor="center")
    def generateNewGame(self):
        gameListLen = (len(self.userData.getJSON()["response"]["games"]) - 1)
        gameIdx = random.randint(0,gameListLen)

        self.main(self.userData.getJSON()["response"]["games"][gameIdx]["name"])

if __name__ == '__main__':
    mainScreen = MainScreen()

    mainScreen.getIDScreen()
    tk.mainloop()
    