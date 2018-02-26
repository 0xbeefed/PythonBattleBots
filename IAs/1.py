import lib

mId = lib.myId()
pos = lib.getCell(mId)
enemy = lib.getEnemyId()
enemyPos = lib.getCell(enemy)

for i in range(3):
    if (enemyPos[0] > pos[0]):
        pos = [pos[0] + 1, pos[1]]
    elif (enemyPos[0] < pos[0]):
        pos = [pos[0] - 1, pos[1]]
    elif (enemyPos[1] > pos[1]):
        pos = [pos[0], pos[1] + 1]
    elif (enemyPos[1] < pos[1]):
        pos = [pos[0], pos[1] - 1]
        
    lib.moveOn(pos[0], pos[1])

