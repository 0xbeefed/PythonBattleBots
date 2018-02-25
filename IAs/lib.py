import sys
import os
import json

# GLOBALS
CELL_EMPTY = 0
CELL_OBSTACLE = 1

# GRABBING INFOS
PATH = os.getcwd().replace('\\', '/') + '/' + sys.argv[1]
#PATH = 'C:/Users/arthc/Desktop/PythonBattleBots/Fights/1/'
with open(PATH + 'game.dat', 'r') as file:
    GAME_DAT = json.loads(file.read())
with open(PATH + 'players.dat', 'r') as file:
    PLAYERS_DAT = json.loads(file.read())
with open(PATH + 'map.dat', 'r') as file:
    MAP_DAT = json.loads(file.read())

# INFO FUNCTIONS
def myId():
    global GAME_DAT
    return GAME_DAT['whoPlays']

def getEnemyId():
    global PLAYERS_DAT
    for player in PLAYERS_DAT:
        if player['id'] != myId():
            return player['id']

def getCell(entity):
    global PLAYERS_DAT
    return [PLAYERS_DAT[entity]['x'], PLAYERS_DAT[entity]['y']]

def getCellContent(x, y):
    global MAP_DAT
    if y > 0 and x > 0 and y < len(MAP_DAT) and x < len(MAP_DAT[y]):
        return 0 if MAP_DAT[y][x] == -1 else 1
    else:
        return -1

    

# ACTION FUNCTIONS
def moveOn(x, y):
    print('[MOVE] {0} {1}'.format(x, y))
    return 1
