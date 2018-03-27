import sys
sys.path.append(sys.path[0] + '/users/')
import lib



def getCellContent(pos, grid):
    if 0 <= pos[0] and pos[0] < lib.getMapHeight() and 0 <= pos[1] and pos[1] < lib.getMapWidth():
        if grid[pos[1]][pos[0]] == -3:
            return lib.LAVA_HOLE
        elif grid[pos[1]][pos[0]] == -2:
            return lib.CELL_OBSTACLE
        elif grid[pos[1]][pos[0]] == -1:
            return lib.CELL_EMPTY
        else:
            return lib.CELL_PLAYER
    else:
        return lib.CELL_OBSTACLE

def minimax(start, mp, grid):
    for cells in mp:
        if lib.getDistance(start, lib.getCell(lib.getEnemyId())):
            for d in [(0,1), (1,0), (-1,0), (0,-1)]:
                cell = [start[0] + d[0], start[1] + d[1]]
                if getCellContent(cell, grid) == lib.CELL_EMPTY:
                    pass


def main():
    # Variables
    lib.setWeapon(lib.WEAPON_SWORD)
    print('toast')
    print(lib.getWeaponEffects(lib.WEAPON_SWORD))
    print(lib.getWeaponEffects(lib.WEAPON_SIMPLE_GUN))
    mId = lib.getMyId()
    pos = lib.getCell(mId)
    enemy = lib.getEnemyId()
    enemyPos = lib.getCell(enemy)

    if lib.getHp(mId)+8 < lib.getMaxHp(mId):
        lib.useHeal(pos)
    
    tabToMarkY = []
    tabToMarkR = []
    for x in range(lib.getMapWidth()):
        for y in range(lib.getMapHeight()):
            if lib.getLineOfSight(pos, [x,y]):
                tabToMarkY.append([x,y])
            else:
                tabToMarkR.append([x,y])

    lib.mark(tabToMarkY, 'yellow')
    lib.mark(tabToMarkR, 'red')

    

    path = lib.getPath(pos, enemyPos)

    if path != -1:
        for move in path:
            #lib.mark(move, 'black')
            lib.moveOn(move)
        lib.attackOn(enemyPos)

    #grid = lib.MAP_DAT
