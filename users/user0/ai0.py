import sys
sys.path.append(sys.path[0] + '/users/')
import lib



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

    tabToMarkY = []
    tabToMarkR = []
    for x in range(lib.getMapWidth()):
        for y in range(lib.getMapHeight()):
            #print('ia1', x,y)
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
