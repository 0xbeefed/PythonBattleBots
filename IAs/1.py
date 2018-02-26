import lib

def astar(start, end, path, visited):
    global neighbours, bestPath
    visited.append(start)
    
    for n in neighbours[start[1]][start[0]]:
        if n in neighbours[end[1]][end[0]]:
            newPath = path.copy()
            newPath.append(n)
            if len(path) < bestPath[1]:
                bestPath = [newPath, len(newPath)+1]
            break
        else:
            if n not in visited:
                newPath = path.copy()
                newPath.append(n)
                astar(n, end, newPath, visited)

# Variables
mId = lib.myId()
pos = lib.getCell(mId)
enemy = lib.getEnemyId()
enemyPos = lib.getCell(enemy)
bestPath = [[], 9999]

# Neighbours
neighbours = []
for y in range(16):
    neighbours.append([])
    for x in range(16):
        neighbours[y].append([])
        for n in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            nPos = [x + n[0], y + n[1]]
            if nPos[0] >= 0 and nPos[1] >= 0 and nPos[0] < 16 and nPos[1] < 16 and lib.getCellContent(nPos[0], nPos[1]) == 0:
                neighbours[y][x].append(nPos)
        neighbours[y][x] = sorted(neighbours[y][x], key=lambda o: abs(o[0] - enemyPos[0]) + abs(o[1] - enemyPos[1]))

print(neighbours[pos[1]][pos[0]])
astar(pos, enemyPos, [], [])
print(bestPath)
for move in bestPath[0]:
    lib.moveOn(move[0], move[1])
        
