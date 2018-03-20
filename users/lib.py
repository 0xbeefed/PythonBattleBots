import sys
import os
import json
global actions

actions = []
mapData = []
GAME_DAT = []
PLAYERS_DAT = []
MAP_DAT = []


# GLOBALS
CELL_EMPTY = -1
CELL_OBSTACLE = -2
CELL_PLAYER = 1


# INFO FUNCTIONS
def myId():
    """Returns the id of your player"""
    global GAME_DAT
    return GAME_DAT['whoPlays']

def getEnemyId():
    """Returns the id of your opponent"""
    global PLAYERS_DAT
    for player in PLAYERS_DAT:
        if player['id'] != myId():
            return player['id']

def getMapWidth():
    """Returns the width of the map"""
    return len(MAP_DAT)

def getMapHeight():
    """Returns the height of the map"""
    return len(MAP_DAT[0])

def getCell(entity):
    """Returns the cell where the entity is"""
    global PLAYERS_DAT
    return [PLAYERS_DAT[entity]['x'], PLAYERS_DAT[entity]['y']]

def getCellContent(x, y):
    """Returns the contents of the cell [x, y]"""
    global MAP_DAT
    if y >= 0 and x >= 0 and y < len(MAP_DAT) and x < len(MAP_DAT[y]):
        if MAP_DAT[y][x] == -2:
            return CELL_OBSTACLE
        elif MAP_DAT[y][x] == -1:
            return CELL_EMPTY
        else:
            return CELL_PLAYER
    else:
        return CELL_OBSTACLE

def getObstacles():
    """Returns the list of obstacles on the map"""
    global MAP_DAT
    obstacles = []
    for y in range(len(MAP_DAT)):
        for x in range(len(MAP_DAT[0])):
            if getCellContent(x,y) == CELL_OBSTACLE:
                obstacles.append([x,y])
    return obstacles

def getLineOfSight(pos, pos2):
    """Returns 1 if there are a line of sight between pos1 and pos2"""
    obstacles = getObstacles()      
    if pos2[0] != pos[0]:
        for obstacle in obstacles:
            u = 0
            d = 0
            if (obstacle[0] > pos[0]) == (pos2[0] > pos[0]) and (obstacle[1] > pos[1]) == (pos2[1] > pos[1]) and abs(obstacle[0]-pos[0])+abs(obstacle[1]-pos[1]) < abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1]) and obstacle != pos:
                for a, b in [[0,0], [0,1], [1,0], [1,1]]: # Check that the 4 corners of the obstacle are below or above the line between pos and [x,y]
                    if obstacle[1]+b > ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        u += 1
                    elif obstacle[1]+b < ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        d += 1
                    else:
                        u += 1
                        d += 1
                if d != 4 and u != 4:
                    #print(pos2[0],pos2[1],obstacle)
                    return 0
    else:
        for obstacle in obstacles:
            if obstacle[0] == pos2[0] and (min(pos[1], pos2[1]) < obstacle[1] < max(pos[1], pos2[1])):
                return 0    
    return 1
    
def getDistance(pos, pos2):
    """Returns the Manhattan distance between pos1 and pos2"""
    return abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1])

def getPath(start, end):
    """Returns a path between start and end, if it exists"""
    openList = [start]
    nodes = {str(start) : ['',0]} # nodes['[x, y]'] = [parent, distance from the start]
    closedList = []
    
    while len(openList) != 0:
        
        current = openList[0]
        for tmp in openList:
            if nodes[str(tmp)][1] + getDistance(tmp, end) < nodes[str(current)][1] + getDistance(current, end):
                current = tmp
        
        if current == end:
            break
        
        del openList[openList.index(current)]
        closedList.append(current)
        
        for a,b in [[0,1], [0,-1], [1,0], [-1,0]]:
            X = current[0] + a
            Y = current[1] + b
            if getCellContent(X, Y) == CELL_OBSTACLE or [X,Y] in closedList:
                continue
            elif not [X,Y] in openList:
                openList.append([X,Y])
                nodes[str([X,Y])] = [current, nodes[str(current)][1] + 1]
            elif not str([X,Y]) in nodes or nodes[str([X,Y])][1] > nodes[str(current)][1] + 1:
                nodes[str([X,Y])] = [current, nodes[str(current)][1] + 1]
     
    if current != end: # if the path does not exist
        return -1 
    
    tmp = nodes[str(end)][0]
    path = [end]
    while tmp != start: # rewind the parents of the nodes to get the path
        path.append(tmp)
        tmp = nodes[str(tmp)][0]
    return path[::-1]


# ACTION FUNCTIONS

def moveOn(x, y):
    """Move your player closer to a cell [x, y]"""
    actions.append(['[MOVE]', x, y])
    return 1

def mark(x, y, color):
    """Marks the cell [x, y] with the color in parameter"""
    actions.append(['[MARK]', x, y, color])
    return 1

def attackOn(x, y):
    """Attack with the current weapon on the cell [x, y]"""
    actions.append(['[ATTACK]', x, y])
    return 1
