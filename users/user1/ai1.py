import sys
sys.path.append(sys.path[0] + "/users/")
import lib

def moveMap(center, mp):
    moveMap = [center]
    for y in range(lib.getMapHeight()):
        for x in range(lib.getMapWidth()):
            if lib.getDistance([x, y], center) < mp + 1 and lib.getCellContent([x, y]) == lib.CELL_EMPTY:
                path = lib.getPath([x, y], center)
                if path != -1 and len(path) <= mp:
                    moveMap.append([x, y])
    return moveMap 

def main():
    
    lib.setWeapon(lib.WEAPON_SIMPLE_GUN)
    selfId = lib.getMyId()
    selfPos = lib.getCell(selfId)
    selfMp = 3

    enemyId = lib.getEnemyId()
    enemyPos = lib.getCell(enemyId)
    
    tab = []
    OBSTACLES = lib.getObstacles()
    
    # Movemap
    selfMoveMap = moveMap(selfPos, selfMp)
    #for cell in selfMoveMap:
    #    lib.mark(cell[0], cell[1], 'green')

    enemyMoveMap = moveMap(enemyPos, 3)
    #for cell in enemyMoveMap:
    #    lib.mark(cell[0], cell[1], 'red')

    # Find safe cell / attack cell
    canHit = False
    bestMove = [[], -1]
    for simulated in selfMoveMap:
        # Find far cell where we can attack
        if lib.getDistance(simulated, enemyPos) <= 5 and lib.getLineOfSight(simulated, enemyPos):
            if lib.getDistance(simulated, enemyPos) >= bestMove[1]:
                bestMove = [simulated.copy(), lib.getDistance(simulated, enemyPos)]
                canHit = True
    
    if canHit:
        lib.mark(bestMove[0], 'blue')
        path = lib.getPath(selfPos, bestMove[0])
        if path != 1:
            for move in path:
                lib.moveOn(move)
                selfMp -= 1
            lib.attackOn(enemyPos)
            lib.mark(bestMove[0], 'yellow')
            selfPos = bestMove[0]

    # Flee on safe cell
    canFlee = False
    bestFlee = [[], 99999]
    selfMoveMap = moveMap(selfPos, selfMp)           
    for selfSimu in selfMoveMap:
        safeCell = True
        for enemySimu in enemyMoveMap:
            if lib.getDistance(selfSimu, enemySimu) <= 6 and lib.getLineOfSight(selfSimu, enemySimu):
                # If user can hit us, then cell isn't safe
                safeCell = False
                break
        if safeCell:
            lib.mark(selfSimu, 'green')
            canFlee = True
            if (bestFlee[1] >= lib.getDistance(selfSimu, enemyPos)):
                bestFlee = [selfSimu.copy(), lib.getDistance(selfSimu, enemyPos)]
        else:
            lib.mark(selfSimu, 'red')

    if canFlee:
        lib.mark(bestFlee[0], 'blue')
        path = lib.getPath(selfPos, bestFlee[0])
        if path != -1:
            for move in path:
                lib.moveOn(move)
                selfMp -= 1
            selfPos = bestFlee[0]
            




