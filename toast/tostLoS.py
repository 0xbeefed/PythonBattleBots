from tkinter import *
import time
import random

root = Tk()

def lineOfSight(start, end, dm):
    if start[1] > end[1]:
        lineOfSight(end, start, dm)
    elif start[0] == end[0]:
        pos = start
        tab = [start]
        print('SAME X COORD')
        while pos != end:
            print(pos, end)
            pos[1]+dm
            tab.append(pos)
        print(tab)
        for i in range(len(tab)):
            cell = tab[i]
            tab[i] = toastCanvas.create_rectangle(cell[0]-20, cell[1]-20, cell[0]+20, cell[1]+20, fill = 'blue')
            toastCanvas.tag_lower(tab[i])
            root.update()
            
    elif start[0] != end[0]:

        m = (end[1]-start[1])/(end[0]-start[0])
        p = start[1] - m * start[0]
        print(m)
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
            
                
            if m*xh+p <= yh:
                posH = [xh, yh]
            else:
                posH = [xh-dx, yh+dy]
            
            if m*xb+p < yb:
                posB = [xb+dx, yb-dy]
            else:
                posB = [xb, yb]
            
            if (posH[0]-20)%40 == 0 and (posH[1]-20)%40 == 0:
                tab.append(posH)
                
            if (posB[0]-20)%40 == 0 and (posB[1]-20)%40 == 0:
                tab.append(posB)
                  
            #lines.append(toastCanvas.create_line(tmpH[0], tmpH[1], posH[0], posH[1], fill = 'red'))
            #lines.append(toastCanvas.create_line(tmpB[0], tmpB[1], posB[0], posB[1], fill = 'green'))
            #root.update()

        print(tab)
        for i in range(len(tab)):
            cell = tab[i]
            tab[i] = toastCanvas.create_rectangle(cell[0]-20, cell[1]-20, cell[0]+20, cell[1]+20, fill = 'blue')
            toastCanvas.tag_lower(tab[i])
            root.update()

        #time.sleep(2)
        #for line in lines:
        #    toastCanvas.delete(line)
        #for cell in tab:
        #    toastCanvas.delete(cell)
                    
def refreshMap():
    toastCanvas.delete(ALL)
    for x in range(16):
        toastCanvas.create_line(0, x*40, 640, x*40)
        toastCanvas.create_line(x*40, 0, x*40, 640)

def create_lines():
    refreshMap()
    pos1 = [random.randint(0,15), random.randint(0,15)]
    pos2 = pos1
    while pos2 == pos1:
        pos2 = [random.randint(0,15), random.randint(0,15)]
    print("Line of sight between ", pos1, pos2)

    pos1[0] = pos1[0] * 40 + 20
    pos1[1] = pos1[1] * 40 + 20
    pos2[0] = pos2[0] * 40 + 20
    pos2[1] = pos2[1] * 40 + 20
    
    toastCanvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1])
    lineOfSight(pos1, pos2, 20)

toastCanvas = Canvas(root, width = 640, height = 640, bg = 'white')
toastCanvas.pack()

for x in range(16):
    toastCanvas.create_line(0, x*40, 640, x*40)
    toastCanvas.create_line(x*40, 0, x*40, 640)

startButton = Button(root, text = 'start', command = create_lines)
startButton.pack()

root.mainloop()
