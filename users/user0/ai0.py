import sys
sys.path.append(sys.path[0] + '/users/')
import lib



def main():
    # Variables
    mId = lib.myId()
    pos = lib.getCell(mId)
    enemy = lib.getEnemyId()
    enemyPos = lib.getCell(enemy)

    path = lib.getPath(pos, enemyPos)

    if path != -1:
        for move in path:
            lib.mark(move[0], move[1], 'black')
            lib.moveOn(move[0], move[1])
        lib.attackOn(enemyPos[0], enemyPos[1])
            

