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

def ldv(pos, x, y):
    if x != pos[0]:
        for obstacle in OBSTACLES:
            u = 0
            d = 0
            if abs(obstacle[0]-pos[0])+abs(obstacle[1]-pos[1]) < abs(pos[0]-x)+abs(pos[1]-y) and obstacle != pos:
                for a, b in [[0,0], [0,1], [1,0], [1,1]]: # Check that the 4 corners of the obstacle are below or above the line between pos and [x,y]
                    if obstacle[1]+b > ((pos[1]-y)/(pos[0]-x))*(obstacle[0]+a-x-0.5)+y+0.5:
                        u += 1
                    if obstacle[1]+b < ((pos[1]-y)/(pos[0]-x))*(obstacle[0]+a-x-0.5)+y+0.5:
                        d += 1
                    if obstacle[1]+b == ((pos[1]-y)/(pos[0]-x))*(obstacle[0]+a-x-0.5)+y+0.5:
                        u += 1
                        d += 1
                if d != 4 and u != 4:
                    print(x,y,obstacle)
                    return 0
    else:
        for obstacle in OBSTACLES:
            if obstacle[0] == x and (min(pos[1], y) < obstacle[1] < max(pos[1], y)):
                return 0    
    return 1

for y in range(16):
    for x in range(16):
        if not ldv(pos, x, y):
            lib.mark(x, y, 'red')
        else:
            lib.mark(x, y, 'black')
