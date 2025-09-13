import requests
import json
from os import listdir

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

if __name__ == '__main__':
    usersOnFile = listdir("./steam-picker/users/") # get the users in the users dir
    # print(usersOnFile[0][:-5])
    key = getKey("./steam-picker/steamweb.key") # get API key from file
    print("enter steamid64 (decimal): ")
    steamID = input()

    loadFromFile = "\0"
    if (steamID + ".json" in usersOnFile): # check if user id is already saved to a file to avoid api call
        loadFromFile = "\0"
        while (loadFromFile.lower() != "y" and loadFromFile.lower() != "n"):
            print("user info is currently saved to a local file. load it? (y/n)\n" \
            "(this is opposed to calling the steamweb api)")
            loadFromFile = input()

    jsonData = {}
    if (loadFromFile.lower() == "y"):
        jsonData = loadInfoFromFile(steamID)
    else:
        saveToFile = "\0"
        while (saveToFile.lower() != "y" and saveToFile.lower() != "n"):
            print("save owned game information to local file? (y/n)")
            saveToFile = input()

        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + key + "&steamid=" + steamID + "&include_appinfo=1&include_played_free_games=1&format=json"
        jsonData = requests.get(url).json()
        
        if (saveToFile.lower() == "y"):
            saveInfo(steamID, jsonData)
    
    for game in jsonData["response"]["games"]:
        print(game["name"])
