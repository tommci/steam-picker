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
        self.gameList = []
        self.gameListUnplayed = []
    def setID(self, steamID):
        self.id = steamID
    def getID(self):
        return self.id
    def setKey(self, keyFile):
        with open(keyFile, "r") as file:
            self.key = file.readline()
    def getKey(self):
        return self.key
    def setJSONData(self, data, addLibrary):
        self.jsonData = data
        self.generateLists(addLibrary) # generates the lists of game names after setting
    def getJSON(self):
        return self.jsonData
    def saveInfo(self):
        with open("./users/" + self.id + ".json", "w") as file:
            json.dump(self.jsonData, file)
    def loadInfo(self, addLibrary):
        with open("./users/" + self.id + ".json", "r") as file:
            self.jsonData = json.load(file)
        self.generateLists(addLibrary)
    def generateLists(self, addLibrary):
        for game in self.getJSON()["response"]["games"]:
            self.gameList.append(game["name"])
            if game["playtime_forever"] == 0 and not addLibrary:
                self.gameListUnplayed.append(game["name"])
    def getRandomGame(self):
        return random.choice(self.gameList)
    def getRandomUnplayedGame(self):
        return random.choice(self.gameListUnplayed)

class MainScreen:
    def __init__(self):
        self.gameName = ttk.Label(tk)
        self.textPrompt = ttk.Label(tk)
        self.newGameButton = ttk.Button(tk)
        self.entryField = ttk.Entry(tk)
        self.confirm = ttk.Button(tk)
        self.deny = ttk.Button(tk)
        self.settingsButton = ttk.Button(tk)
        self.playtimeCheck = ttk.Checkbutton(tk)
        self.addLibraryButton = ttk.Button(tk)
        self.quitButton = ttk.Button(tk)

        self.filterUnplayed = IntVar(tk, value=0)
        self.addLibrary = False
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
        self.settingsButton.destroy()
        self.playtimeCheck.destroy()
        self.addLibraryButton.destroy()
        self.quitButton.destroy()
    # first screen upon launching, gets steamid64
    def getIDScreen(self, addingLibrary):
        self.destroyItems()

        self.addLibrary = addingLibrary
        self.textPrompt = ttk.Label(tk, text="enter steamid64 (decimal).\nnone of the steam data retrieved will be stored on a server.\nyou will be given the option to store retrieved data on your local machine.\nyou MUST PROVIDE your OWN steam web api key!\nview the readme for more info.")
        self.textPrompt.place(relx=0.5, rely=0.4, anchor="center")

        self.entryField = ttk.Entry(tk, width=20)
        self.entryField.place(relx=0.5, rely=0.6, anchor="center")

        self.confirm = ttk.Button(tk, text="Confirm", command=self.getIDInfo)
        self.confirm.place(relx=0.5, rely=0.7, anchor="center")

        if self.addLibrary:
            self.deny = ttk.Button(tk, text="Cancel", command=self.settings)
            self.deny.place(relx=0.5, rely=0.8, anchor="center")
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

        self.deny = ttk.Button(tk, text="No", command=self.callAPIForGames)
        self.deny.place(relx=0.6, rely=0.7, anchor="center")
    def setSaveToFile(self):
        # this flags the system to know to save it to a file after it is retrieved from steamweb
        self.saveToFile = True
        self.callAPIForGames()
    def callAPIForGames(self):
        # get the api key from file system
        self.userData.setKey("./steamweb.key")
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + self.userData.getKey() + "&steamid=" + self.userData.getID() + "&include_appinfo=1&include_played_free_games=1&format=json"
        # TODO: check if the information was retrieved correctly
        self.userData.setJSONData(requests.get(url).json(), self.addLibrary) # set the json data, also generates list in UserData
        if (self.saveToFile): # this would have been set earlier
            self.userData.saveInfo()
        
        if self.addLibrary: self.main("Additional user library added to pool.")
        else: self.main("Press the button below to select a random game from your library!")
    def loadFromFile(self):
        self.userData.loadInfo(self.addLibrary) # also generates list in UserData
        if self.addLibrary: self.main("Additional user library added to pool.")
        else: self.main("Press the button below to select a random game from your library!")
    def main(self, gameName):
        self.destroyItems()
        self.addLibrary = False

        self.gameName = ttk.Label(tk, text=gameName)
        self.gameName.place(relx=0.5, rely=0.4, anchor="center")

        self.newGameButton = ttk.Button(tk, text="Pick New Game", command=self.generateNewGame)
        self.newGameButton.place(relx=0.5, rely=0.6, anchor="center")

        self.settingsButton = ttk.Button(tk, text="Settings", command=self.settings)
        self.settingsButton.place(relx=0.1, rely=0.1, anchor="center")

        self.quitButton = ttk.Button(tk, text="Quit", command=self.quit)
        self.quitButton.place(relx=0.5, rely=0.8, anchor="center")
    def generateNewGame(self):
        if (self.filterUnplayed.get()): self.main(self.userData.getRandomUnplayedGame())
        else: self.main(self.userData.getRandomGame())
    def settings(self):
        self.destroyItems()
        self.addLibrary = False

        self.playtimeCheck = ttk.Checkbutton(tk, text="Generate Only Unplayed Games", variable=self.filterUnplayed, onvalue=1, offvalue=0)
        self.playtimeCheck.place(relx=0.5, rely=0.3, anchor="center")

        self.addLibraryButton = ttk.Button(tk, text="Add Another User's Library...", command= lambda: self.getIDScreen(True))
        self.addLibraryButton.place(relx=0.5, rely=0.4, anchor="center")

        self.confirm = ttk.Button(tk, text="Confirm", command= lambda: self.main("Press the button below to select a random game from your library!"))
        self.confirm.place(relx=0.5, rely=0.6, anchor="center")
    def quit(self):
        tk.destroy()

if __name__ == '__main__':
    mainScreen = MainScreen()

    mainScreen.getIDScreen(False)
    tk.mainloop()
    