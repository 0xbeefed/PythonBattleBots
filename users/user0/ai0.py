import sys
sys.path.append(sys.path[0] + '/users/')
import lib



def main():
    # Variables

    print('toast')
    mId = lib.getMyId()
    pos = lib.getCell(mId)
    enemy = lib.getEnemyId()
    enemyPos = lib.getCell(enemy)

    
    for x in range(lib.getMapWidth()):
        for y in range(lib.getMapHeight()):
            #print('ia1', x,y)
            if lib.getLineOfSight(pos, [x,y]):
                lib.mark(x, y, 'yellow')
            else:
                lib.mark(x,y,'red')
    """          
    path = lib.getPath(pos, enemyPos)

    if path != -1:
        for move in path:
            lib.mark(move[0], move[1], 'black')
            lib.moveOn(move[0], move[1])
        lib.attackOn(enemyPos[0], enemyPos[1])"""
            

