import sys
sys.path.append(sys.path[0] + "/..")
import lib

mId = lib.myId()
pos = lib.getCell(mId)

enemyCell = lib.getCell(lib.getEnemyId())

tab = []
OBSTACLES = lib.getObstacles()

def cellDistance(pos, pos2):
    return abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1])


def astar(start, end):
    openList = [start]
    closedList = []
    parents = {}
    
    while len(openList) != 0:
        
        current = openList[0]
        for tmp in openList:
            if cellDistance(start, tmp) + cellDistance(tmp, end) < cellDistance(start, current) + cellDistance(current, end):
                current = tmp
        
        if current == enemyCell:
            break
        
        del openList[openList.index(current)]
        closedList.append(current)
        
        for a,b in [[0,1], [0,-1], [1,0], [-1,0]]:
            X = current[0] + a
            Y = current[1] + b
            if lib.getCellContent(X, Y) == -2 or [X,Y] in closedList:
                continue
            elif not [X,Y] in openList:
                openList.append([X,Y])
                parents[str([X,Y])] = current
            else:
                if not str([X,Y]) in parents:
                    parents[str([X,Y])] = current
     
    if current != enemyCell:
        return -1
    
    tmp = parents[str(end)]
    path = []
    while tmp != start:
        path.append(tmp)
        tmp = parents[str(tmp)]
    
    return path


path = lib.getPath(pos, enemyCell)
if path == -1:
    lib.mark(pos[0], pos[1], 'black')
else:
    for cell in path:
        lib.mark(cell[0], cell[1], 'green')

 
