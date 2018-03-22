from tkinter import *
import random

root = Tk()

CELL_SIZE = 40

def lineOfSight(start, end, dm):
    global CELL_SIZE
    if start[1] > end[1]:
        lineOfSight(end, start, dm)
    elif start[0] == end[0]:
        pos = start
        tab = [start.copy()]
        while pos != end:
            pos[1] = pos[1]+dm
            if (pos[0]-CELL_SIZE//2)%CELL_SIZE == 0 and (pos[1]-CELL_SIZE//2)%CELL_SIZE == 0:
                tab.append(pos.copy())
                
        for i in range(len(tab)):
            cell = tab[i]
            tab[i] = toastCanvas.create_rectangle(cell[0]-CELL_SIZE//2, cell[1]-CELL_SIZE//2, cell[0]+CELL_SIZE//2, cell[1]+CELL_SIZE//2, fill = 'blue')
            toastCanvas.tag_lower(tab[i])
            root.update()
            
    elif start[1] == end[1]:
        if start[0] > end[0]:
            dm = -dm
        pos = start
        tab = [start.copy()]
        while pos != end:
            pos[0] = pos[0]+dm
            if (pos[0]-CELL_SIZE//2)%CELL_SIZE == 0 and (pos[1]-CELL_SIZE//2)%CELL_SIZE == 0:
                tab.append(pos.copy())
        
        for i in range(len(tab)):
            cell = tab[i]
            tab[i] = toastCanvas.create_rectangle(cell[0]-CELL_SIZE//2, cell[1]-CELL_SIZE//2, cell[0]+CELL_SIZE//2, cell[1]+CELL_SIZE//2, fill = 'blue')
            toastCanvas.tag_lower(tab[i])
            root.update()
    else:
        m = (end[1]-start[1])/(end[0]-start[0])
        p = start[1] - m * start[0]
        posH = start
        posB = start
        lines = []
        tab = [start]
        tab2 = []
        dx = dm
        dy = dm

        if m < 0:
            m = (start[1]-end[1])/(start[0]-end[0])
            dx = -dm
        
        while posH != end:
            tmpH = posH
            xh = posH[0] + dx
            yh = posH[1]

            tmpB = posB
            xb = posB[0]
            yb = posB[1] +dy
            
            if round(m*xh+p, 2) <= yh:
                posH = [xh, yh]
            else:
                posH = [xh-dx, yh+dy]
            
            if m*xb+p < yb:
                posB = [xb+dx, yb-dy]
            else:
                posB = [xb, yb]
            
            if (posH[0]-CELL_SIZE//2)%CELL_SIZE == 0 and (posH[1]-CELL_SIZE//2)%CELL_SIZE == 0:
                tab.append(posH)
                
            if (posB[0]-CELL_SIZE//2)%CELL_SIZE == 0 and (posB[1]-CELL_SIZE//2)%CELL_SIZE == 0:
                tab.append(posB)
                  
            lines.append(toastCanvas.create_line(tmpH[0], tmpH[1], posH[0], posH[1], fill = 'red'))
            lines.append(toastCanvas.create_line(tmpB[0], tmpB[1], posB[0], posB[1], fill = 'green'))
            root.update()

        for i in range(len(tab)):
            cell = tab[i]
            tab[i] = toastCanvas.create_rectangle(cell[0]-CELL_SIZE//2, cell[1]-CELL_SIZE//2, cell[0]+CELL_SIZE//2, cell[1]+CELL_SIZE//2, fill = 'blue')
            toastCanvas.tag_lower(tab[i])
            root.update()
                    
def refreshMap():
    global CELL_SIZE
    toastCanvas.delete(ALL)
    for x in range(16):
        toastCanvas.create_line(0, x*CELL_SIZE, 16*CELL_SIZE, x*CELL_SIZE)
        toastCanvas.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, 16*CELL_SIZE)

def create_lines():
    startButton.config(state = DISABLED)
    global CELL_SIZE
    refreshMap()
    pos1 = [random.randint(0,15), random.randint(0,15)]
    pos2 = pos1
    while pos2 == pos1:
        pos2 = [random.randint(0,15), random.randint(0,15)]

    print("Line of sight between ", pos1, pos2)

    pos1[0] = CELL_SIZE * (pos1[0]+0.5)
    pos1[1] = CELL_SIZE * (pos1[1]+0.5)
    pos2[0] = CELL_SIZE * (pos2[0]+0.5)
    pos2[1] = CELL_SIZE * (pos2[1]+0.5)

    toastCanvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1])
    lineOfSight(pos1, pos2, CELL_SIZE//2)
    startButton.config(state = NORMAL)

toastCanvas = Canvas(root, width = 16*CELL_SIZE, height = 16*CELL_SIZE, bg = 'white')
toastCanvas.pack()

for x in range(16):
    toastCanvas.create_line(0, x*CELL_SIZE, 16*CELL_SIZE, x*CELL_SIZE)
    toastCanvas.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, 16*CELL_SIZE)

startButton = Button(root, text = 'start', command = create_lines)
startButton.pack()

root.mainloop()
