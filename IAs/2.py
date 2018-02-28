import lib

mId = lib.myId()
pos = lib.getCell(mId)

enemyCell = lib.getCell(lib.getEnemyId())

tab = []
OBSTACLES = lib.getObstacles()

def cellDistance(pos, pos2):
    return abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1])


openList = [pos]
closedList = []
parents = {}
h = True
        
while len(openList) != 0 and h:
    
    current = openList[0]
    for tmp in openList:
        if cellDistance(pos, tmp) + cellDistance(tmp, enemyCell) < cellDistance(pos, current) + cellDistance(current, enemyCell):
            current = tmp
    del openList[openList.index(current)]
    closedList.append(current)
    
    if current == enemyCell:
        break

    for a,b in [[0,1], [0,-1], [1,0], [-1,0]]:
        X = current[0] + a
        Y = current[1] + b
        if lib.getCellContent(X, Y) == -2 or [X,Y] in closedList: continue
        elif not [X,Y] in openList: openList.append([X,Y]); parents[str([X,Y])] = current
        else:
            if not str([X,Y]) in parents:
                parents[str([X,Y])] = current
        
        
tmp = parents[str(enemyCell)]
path = []
while tmp != pos:
    path.append(tmp)
    tmp = parents[str(tmp)]
    
print(*path)

for cell in path:
    lib.mark(cell[0], cell[1], 'green')


