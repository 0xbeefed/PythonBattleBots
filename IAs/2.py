import lib

mId = lib.myId()
pos = lib.getCell(mId)

enemyCell = lib.getCell(lib.getEnemyId())

tab = []
OBSTACLES = []
for y in range(16):
    tab.append([0]*16)
    for x in range(16):
        if lib.getCellContent(x,y):
            tab[y][x] = 0
            OBSTACLES.append([x,y])
        else:
            tab[y][x] = 1
            
print(tab)
print('OBSTACLES : ', OBSTACLES)

def ldv(pos, pos2):
    if pos2[0] != pos[0]:
        for obstacle in OBSTACLES:
            u = 0
            d = 0
            if (obstacle[0] > pos[0]) == (pos2[0] > pos[0]) and (obstacle[1] > pos[1]) == (pos2[1] > pos[1]) and abs(obstacle[0]-pos[0])+abs(obstacle[1]-pos[1]) < abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1]) and obstacle != pos:
                for a, b in [[0,0], [0,1], [1,0], [1,1]]: # Check that the 4 corners of the obstacle are below or above the line between pos and [x,y]
                    if obstacle[1]+b > ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        u += 1
                    if obstacle[1]+b < ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        d += 1
                    if obstacle[1]+b == ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        u += 1
                        d += 1
                if d != 4 and u != 4:
                    print(pos2[0],pos2[1],obstacle)
                    return 0
    else:
        for obstacle in OBSTACLES:
            if obstacle[0] == pos2[0] and (min(pos[1], pos2[1]) < obstacle[1] < max(pos[1], pos2[1])):
                return 0    
    return 1


for y in range(16):
    for x in range(16):
        if not ldv(pos, [x, y]):
            lib.mark(x, y, 'red')
        else:
            lib.mark(x, y, 'black')
