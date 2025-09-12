import random
import sys
import pygame
import xml.etree.ElementTree as ET

pygame.init()
pygame.display.set_caption("Steam Game Picker")

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

DISP = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FPS = 60

# game colors
COLOR_BG = (255, 255, 255)
COLOR_BUTTON = (0, 100, 0)
COLOR_BLACK = (0, 0, 0)

# fonts
FONT_MAIN = pygame.font.SysFont("arial", 32)

class Button:
    def __init__(self, buttonText, x, y):
        self.text = buttonText
        self.x = x
        self.y = y
        self.width = 20
        self.height = 50
        self.leftBound = self.x - (len(self.text) * (self.width // 2))
        self.rightBound = self.x + (len(self.text) * self.width)
        self.textSurface = FONT_MAIN.render(buttonText, False, COLOR_BLACK)
    def draw(self):
        pygame.draw.rect(DISP, COLOR_BUTTON, (self.leftBound, self.y, (len(self.text) * self.width), self.height), width=0)
        DISP.blit(self.textSurface, (self.leftBound, self.y + 5))
    def checkBounds(self,mousePos): # mousePos is a tuple [int,int]
        # print(mousePos[0], mousePos[1])
        # print((self.x - (len(self.text) * (self.width // 2))), (len(self.text) * self.width))
        if(mousePos[0] > self.leftBound and mousePos[0] < self.rightBound and mousePos[1] > self.y and mousePos[1] < (self.y + self.height)):
            return True
        else:
            return False

class TextDisplay:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.textSurface = FONT_MAIN.render(text, False, COLOR_BLACK)
    def draw(self):
        DISP.blit(self.textSurface, (self.x, self.y))
    def setText(self, newText):
        self.textSurface = FONT_MAIN.render(newText, False, COLOR_BLACK)

def parseXML(file):
    gameList = []

    tree = ET.parse(file)
    root = tree.getroot()
    for game in root.findall('./games/game/name'):
        gameList.append(game.text)

    return gameList

def selectRandomItem(list):
    return list[random.randint(0,len(list) - 1)]

randomizeGameButton = Button("New Game",250,300)
gameDisplay = TextDisplay("", 125, 150)

if __name__ == "__main__":
    # setup xml file into list
    fullGameList = parseXML('steam-picker/tomgames.xml') + parseXML('steam-picker/savgames.xml')
    fullGameList = set(fullGameList)
    fullGameList = list(fullGameList)

    tickCount = 0

    rolling = False
    counter = 0

    # gameloop
    while(True):
        DISP.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if (randomizeGameButton.checkBounds(pygame.mouse.get_pos()) and not rolling):
                    rolling = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if rolling:
            if counter < tickCount:
                gameDisplay.setText(selectRandomItem(fullGameList))
                counter += 1
                print(counter)
            else:
                rolling = False
                counter = 0

        randomizeGameButton.draw()
        gameDisplay.draw()
        pygame.display.update()

        pygame.time.Clock().tick(FPS)
        tickCount = (tickCount + 1) % 60