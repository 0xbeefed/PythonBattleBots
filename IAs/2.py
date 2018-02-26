import lib

mId = lib.myId()
pos = lib.getCell(mId)


for i in range(3):
    for coord in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
        if lib.getCellContent(pos[0] + coord[0], pos[1] + coord[1]) == 0:
            lib.moveOn(pos[0] + coord[0], pos[1] + coord[1])
            pos = [pos[0] + coord[0], pos[1] + coord[1]]
            break
