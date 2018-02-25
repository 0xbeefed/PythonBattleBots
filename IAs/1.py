import lib

print('lib loaded')
mId = lib.myId()
print('id ok')
pos = lib.getCell(mId)


for coord in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
    if lib.getCellContent(pos[0] + coord[0], pos[1] + coord[1]) == 0:
        lib.moveOn(pos[0] + coord[0], pos[1] + coord[1])
        break
