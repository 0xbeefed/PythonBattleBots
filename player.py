from tkinter import *
import time
import sys
import json
from threading import Thread

class replayThread(Thread):

    def __init__(self, path):
        Thread.__init__(self)

        # GET FIGHT DATA
        with open(path, 'r') as file:
            self.replay = file.read().split('\n')

        self.players = json.loads(self.replay[0])
        root.title(' vs '.join([i['pseudo'] for i in self.players]))
        self.weapons = json.loads(self.replay[1])
        self.map = json.loads(self.replay[2])
        self.replay = self.replay[3:]
        self.game = {'width': len(self.map), 'height': len(self.map[0]), 'cellSize': 32}
        self.fightLog = []
        gameCanvas.config(height = self.game['width']*self.game['cellSize'], width = self.game['height']*self.game['cellSize'])
        pickTurnScale.config(length=self.game['width']*self.game['cellSize'])

        # INIT GUI
        # Grid
        for x in range(self.game['width']):
            gameCanvas.create_line(x*self.game['cellSize'], 0, x*self.game['cellSize'], self.game['height']*self.game['cellSize'], width=1, fill='black')
        for y in range(self.game['height']):
            gameCanvas.create_line(0, y*self.game['cellSize'], self.game['width']*self.game['cellSize'], y*self.game['cellSize'], width=1, fill='black')

        # Numerotation
        for x in range(self.game['width']):
            for y in range(self.game['height']):
                gameCanvas.create_text((x+0.5)*self.game['cellSize'], (y+0.5)*self.game['cellSize'], text='[{0}, {1}]'.format(x, y), justify='center', font=("Arial", 5), fill='white' if self.map[y][x] == -2 else 'black')

        # Obstacles
        for y in range(self.game['height']):
            for x in range(self.game['width']):
                if self.map[y][x] == -2:
                    obs = gameCanvas.create_rectangle(x*self.game['cellSize'],y*self.game['cellSize'], (x+1)*self.game['cellSize'], (y+1)*self.game['cellSize'], fill='black')
                    gameCanvas.tag_lower(obs)
                elif self.map[y][x] == -3:
                    lav = gameCanvas.create_rectangle(x*self.game['cellSize'],y*self.game['cellSize'], (x+1)*self.game['cellSize'], (y+1)*self.game['cellSize'], fill='red')
                    gameCanvas.tag_lower(lav)

        # Players
        for i in range(len(self.players)):
            self.players[i]['icon'] = gameCanvas.create_oval(self.players[i]['x']*self.game['cellSize'], self.players[i]['y']*self.game['cellSize'], (self.players[i]['x']+1)*self.game['cellSize'], (self.players[i]['y']+1)*self.game['cellSize'], fill=self.players[i]['color'])
            self.players[i]['hpBar'] = [gameCanvas.create_rectangle(self.players[i]['x']*self.game['cellSize'],
                                                                   (self.players[i]['y']-0.15)*self.game['cellSize'],
                                                                   (self.players[i]['x']+1)*self.game['cellSize'],
                                                                   self.players[i]['y']*self.game['cellSize'],
                                                                   fill='red'),
                                        gameCanvas.create_rectangle(self.players[i]['x']*self.game['cellSize'],
                                                                   (self.players[i]['y']-0.15)*self.game['cellSize'],
                                                                   ((self.players[i]['x']+1)*self.game['cellSize'])*(self.players[i]['hp']/self.players[i]['maxHp']),
                                                                   self.players[i]['y']*self.game['cellSize'],
                                                                   fill='green')]
            self.players[i]['pseudoLabel'] = gameCanvas.create_text((self.players[i]['x']+0.5)*self.game['cellSize'],
                                                                   (self.players[i]['y']+0.5)*self.game['cellSize'],
                                                                   text=self.players[i]['pseudo'][:5],
                                                                   anchor='center',
                                                                   fill='white')

    def run(self):
        global playing, pickTurn
        while True:
            self.game['whoPlays'] = 0
            self.game['turn'] = 0
            marks = []
            for action in self.replay:
                while not playing:
                    continue
                action = action.split(' ')
                delay = 0

                if action[0] == '[MOVE]':
                    x = int(action[1])
                    y = int(action[2])

                    print((self.players[self.game['whoPlays']]['hp']/self.players[self.game['whoPlays']]['maxHp']))

                    self.players[self.game['whoPlays']]['x'] = x
                    self.players[self.game['whoPlays']]['y'] = y
                    gameCanvas.coords(self.players[self.game['whoPlays']]['icon'], self.players[self.game['whoPlays']]['x']*self.game['cellSize'], self.players[self.game['whoPlays']]['y']*self.game['cellSize'], (self.players[self.game['whoPlays']]['x']+1)*self.game['cellSize'], (self.players[self.game['whoPlays']]['y']+1)*self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][0],
                                      self.players[self.game['whoPlays']]['x']*self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y']-0.15)*self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['x']+1)*self.game['cellSize'],
                                      self.players[self.game['whoPlays']]['y']*self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][1],
                                      self.players[self.game['whoPlays']]['x']*self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y']-0.15)*self.game['cellSize'],
                                      ((self.players[self.game['whoPlays']]['x']+(self.players[self.game['whoPlays']]['hp']/self.players[self.game['whoPlays']]['maxHp']))*self.game['cellSize']),
                                      self.players[self.game['whoPlays']]['y']*self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['pseudoLabel'], (self.players[self.game['whoPlays']]['x']+0.5)*self.game['cellSize'], (self.players[self.game['whoPlays']]['y']+0.5)*self.game['cellSize'])

                    root.update()
                    time.sleep(0.12)

                elif action[0] == '[MARK]':
                    cellsToMark = json.loads(''.join(action[1:-1]))
                    color = action[-1]
                    for cell in cellsToMark:
                        x = int(cell[0])
                        y = int(cell[1])
                        #color = action[3]
                        marks.append(gameCanvas.create_rectangle(x*self.game['cellSize'], y*self.game['cellSize'], (x+1)*self.game['cellSize'], (y+1)*self.game['cellSize'], fill=color, stipple='gray50'))
                        gameCanvas.tag_lower(marks[len(marks) - 1])

                elif action[0] == '[ATTACK]':
                    x = int(action[1])
                    y = int(action[2])
                    weapon = self.players[self.game['whoPlays']]['currentWeapon']
                    self.fightLog.append(self.players[self.game['whoPlays']]['pseudo'] + ' attaque sur [' + str(x) + ', ' + str(y) + ']')

                    target = -1
                    for i in range(len(self.players)):
                        if self.players[i]['x'] == x and self.players[i]['y'] == y:
                            target = i
                            break

                    if (target != -1):
                        self.fightLog.append(self.players[target]['pseudo'] + ' perd ' + str(self.weapons[weapon]['damage']) + 'HP')
                        self.players[target]['hp'] = max(self.players[target]['hp'] - self.weapons[weapon]['damage'], 0)
                        gameCanvas.coords(self.players[target]['hpBar'][0], self.players[target]['x']*self.game['cellSize'], (self.players[target]['y']-0.15)*self.game['cellSize'], (self.players[target]['x']+1)*self.game['cellSize'], self.players[target]['y']*self.game['cellSize'])
                        gameCanvas.coords(self.players[target]['hpBar'][1], self.players[target]['x']*self.game['cellSize'], (self.players[target]['y']-0.15)*self.game['cellSize'], ((self.players[target]['x']+(self.players[target]['hp']/self.players[target]['maxHp']))*self.game['cellSize']), self.players[target]['y']*self.game['cellSize'])
                        root.update()


                elif action[0] == '[WHOPLAYS]':
                    root.update()
                    time.sleep(0.25) # wait before erasing marks

                    self.game['whoPlays'] = int(action[1])
                    for mark in marks:
                        gameCanvas.delete(mark)
                    marks = []
                    root.update()


                elif action[0] == '[TURN]':
                    self.game['turn'] = int(action[1])
                    pickTurnScale.set(self.game['turn'])
                    self.fightLog.append('Tour ' + str(self.game['turn']))
                    root.update()
                    time.sleep(0.15)

                elif action[0] == '[SET_WEAPON]':
                    self.players[self.game['whoPlays']]['currentWeapon'] = int(action[1])
                    self.fightLog.append(self.players[self.game['whoPlays']]['pseudo'] + ' equipe l\'arme ' + action[2])
                    root.update()
                    
                elif action[0] == '[DEATH]':
                    self.fightLog.append(self.players[int(action[1])]['pseudo'] + ' est mort.')                        

                elif action[0] == '[END]':
                    self.fightLog.append('Fin de la partie.')
                    
                if len(self.fightLog) > (self.game['height']*self.game['cellSize'])/20:
                    del self.fightLog[0]
                logLabel['text'] = '\n'.join(self.fightLog)
                               
            togglePlaying()


def togglePlaying():
    global playing
    togglePlayingButton['text'] = 'Play' if playing else 'Pause'
    playing = not playing
    root.update()

def pickTurnUpdate(e):
    global pickTurn
    #turn = pickTurnScale.get()

# Check if a path is given
if (len(sys.argv) > 1):
    path = sys.argv[1]
else:
    path = 'replay.dat'

# Globals
playing = False
pickTurn = 0

# GUI
root = Tk()
gameCanvas = Canvas(root, width=100, height=100, background='white')
gameCanvas.grid(row=0, column=0)

# Player frame
playerFrame = Frame(root)
playerFrame.grid(row=1, column=0)
pickTurnScale = Scale(playerFrame, from_=0, to=16, tickinterval=1, length=600, orient=HORIZONTAL, command=pickTurnUpdate)
pickTurnScale.grid(row=0, column=0)
togglePlayingButton = Button(playerFrame, text='Play', command=lambda: togglePlaying())
togglePlayingButton.grid(row=1, column=0)

# Infos frame
infosFrame = Frame(root, width=20)
infosFrame.grid(row=0, column=1)
logLabel = Label(infosFrame, text='Information Frame here', anchor="nw", justify=LEFT, width=20, font=("Helvetica", 10, "normal"))
logLabel.grid(row=0, column=0)

# Fight Thread
fightThread = replayThread(path)
fightThread.start()

root.mainloop()
fightThread.join()
