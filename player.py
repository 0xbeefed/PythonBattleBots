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

        self.replayTurns = (''.join(self.replay)).count('[TURN]')
        pickTurnScale.config(from_=1, to=self.replayTurns)

        self.game = {'width': len(self.map), 'height': len(self.map[0]), 'cellSize': 32}
        self.fightLog = []
        gameCanvas.config(height=self.game['width'] * self.game['cellSize'],
                          width=self.game['height'] * self.game['cellSize'])
        pickTurnScale.config(length=self.game['width'] * self.game['cellSize'])

        # Grid
        for x in range(self.game['width']):
            gameCanvas.create_line(x * self.game['cellSize'], 0, x * self.game['cellSize'], self.game['height'] * self.game['cellSize'], width=1, fill='black')
        for y in range(self.game['height']):
            gameCanvas.create_line(0, y * self.game['cellSize'], self.game['width'] * self.game['cellSize'], y * self.game['cellSize'], width=1, fill='black')

        # Numerotation
        for x in range(self.game['width']):
            for y in range(self.game['height']):
                gameCanvas.create_text((x + 0.5) * self.game['cellSize'], (y + 0.5) * self.game['cellSize'],
                                       text='[{0}, {1}]'.format(x, y), justify='center', font=("Arial", 5),
                                       fill='white' if self.map[y][x] == -2 else 'black')

        # Obstacles
        for y in range(self.game['height']):
            for x in range(self.game['width']):
                if self.map[y][x] == -2:
                    obs = gameCanvas.create_rectangle(x * self.game['cellSize'], y * self.game['cellSize'], (x + 1) * self.game['cellSize'], (y + 1) * self.game['cellSize'], fill='black')
                    gameCanvas.tag_lower(obs)
                elif self.map[y][x] == -3:
                    lav = gameCanvas.create_rectangle(x * self.game['cellSize'], y * self.game['cellSize'], (x + 1) * self.game['cellSize'], (y + 1) * self.game['cellSize'], fill='red')
                    gameCanvas.tag_lower(lav)

        # Players
        for i in range(len(self.players)):
            self.players[i]['icon'] = gameCanvas.create_oval(self.players[i]['x'] * self.game['cellSize'],
                                                             self.players[i]['y'] * self.game['cellSize'],
                                                             (self.players[i]['x'] + 1) * self.game['cellSize'],
                                                             (self.players[i]['y'] + 1) * self.game['cellSize'],
                                                             fill=self.players[i]['color'])
            self.players[i]['hpBar'] = [gameCanvas.create_rectangle(self.players[i]['x'] * self.game['cellSize'],
                                                                    (self.players[i]['y'] - 0.15) * self.game['cellSize'],
                                                                    (self.players[i]['x'] + 1) * self.game['cellSize'],
                                                                    self.players[i]['y'] * self.game['cellSize'],
                                                                    fill='red'),
                                        gameCanvas.create_rectangle(self.players[i]['x'] * self.game['cellSize'],
                                                                    (self.players[i]['y'] - 0.15) * self.game['cellSize'],
                                                                    ((self.players[i]['x'] + 1) * self.game['cellSize']) * (self.players[i]['hp'] / self.players[i]['maxHp']),
                                                                    self.players[i]['y'] * self.game['cellSize'],
                                                                    fill='green')]
            self.players[i]['pseudoLabel'] = gameCanvas.create_text(
                (self.players[i]['x'] + 0.5) * self.game['cellSize'],
                (self.players[i]['y'] + 0.5) * self.game['cellSize'],
                text=self.players[i]['pseudo'][:5],
                anchor='center',
                fill='white')
            self.players[i]['gui'] = {'pseudo': gui[i][0], 'canvas': gui[i][1], 'hpLabel': gui[i][2],
                                      'weaponLabel': gui[i][3]}
            self.players[i]['gui']['pseudo'].config(text=self.players[i]['pseudo'])
            self.players[i]['gui']['canvas'].create_oval(10, 10, 40, 40, fill=self.players[i]['color'])
            self.players[i]['gui']['hpLabel'].config(
                text='HP : ' + str(self.players[i]['maxHp']) + '/' + str(self.players[i]['maxHp']))
            self.players[i]['gui']['weaponLabel'].config(text='Arme actuelle : None')

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

                    self.players[self.game['whoPlays']]['x'] = x
                    self.players[self.game['whoPlays']]['y'] = y
                    gameCanvas.coords(self.players[self.game['whoPlays']]['icon'],
                                      self.players[self.game['whoPlays']]['x'] * self.game['cellSize'],
                                      self.players[self.game['whoPlays']]['y'] * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['x'] + 1) * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] + 1) * self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][0],
                                      self.players[self.game['whoPlays']]['x'] * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] - 0.15) * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['x'] + 1) * self.game['cellSize'],
                                      self.players[self.game['whoPlays']]['y'] * self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][1],
                                      self.players[self.game['whoPlays']]['x'] * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] - 0.15) * self.game['cellSize'],
                                      ((self.players[self.game['whoPlays']]['x'] + (self.players[self.game['whoPlays']]['hp'] / self.players[self.game['whoPlays']]['maxHp'])) * self.game['cellSize']),
                                      self.players[self.game['whoPlays']]['y'] * self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['pseudoLabel'],
                                      (self.players[self.game['whoPlays']]['x'] + 0.5) * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] + 0.5) * self.game['cellSize'])

                    root.update()
                    time.sleep(0.12)

                elif action[0] == '[MARK]':
                    cellsToMark = json.loads(''.join(action[1:-1]))
                    color = action[-1]
                    for cell in cellsToMark:
                        x = int(cell[0])
                        y = int(cell[1])
                        marks.append(gameCanvas.create_rectangle(x * self.game['cellSize'], y * self.game['cellSize'], (x + 1) * self.game['cellSize'], (y + 1) * self.game['cellSize'], fill=color, stipple='gray50'))
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
                        self.players[target]['gui']['hpLabel'].config(text='HP : ' + str(self.players[target]['hp']) + '/' + str(self.players[target]['maxHp']))
                        gameCanvas.coords(self.players[target]['hpBar'][0],
                                          self.players[target]['x'] * self.game['cellSize'],
                                          (self.players[target]['y'] - 0.15) * self.game['cellSize'],
                                          (self.players[target]['x'] + 1) * self.game['cellSize'],
                                          self.players[target]['y'] * self.game['cellSize'])
                        gameCanvas.coords(self.players[target]['hpBar'][1],
                                          self.players[target]['x'] * self.game['cellSize'],
                                          (self.players[target]['y'] - 0.15) * self.game['cellSize'], ((self.players[target]['x'] + (self.players[target]['hp'] / self.players[target]['maxHp'])) * self.game['cellSize']),
                                          self.players[target]['y'] * self.game['cellSize'])

                    # Animate
                    for i in range(5):
                        spark = gameCanvas.create_line((self.players[self.game['whoPlays']]['x'] + 0.5) * self.game['cellSize'],
                                                       (self.players[self.game['whoPlays']]['y'] + 0.5) * self.game['cellSize'],
                                                       (x + 0.5) * self.game['cellSize'],
                                                       (y + 0.5) * self.game['cellSize'],
                                                       width=8,
                                                       fill='yellow')
                        root.update()
                        time.sleep(0.02)
                        gameCanvas.delete(spark)
                        root.update()
                        time.sleep(0.02)

                elif action[0] == '[WHOPLAYS]':
                    root.update()
                    time.sleep(0.25)  # wait before erasing marks

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
                    self.players[self.game['whoPlays']]['gui']['weaponLabel'].config(text='Arme actuelle : ' + action[2])
                    root.update()

                elif action[0] == '[HEAL]':
                    self.players[self.game['whoPlays']]['hp'] = min(self.players[self.game['whoPlays']]['hp'] + 5, self.players[self.game['whoPlays']]['maxHp'])
                    self.fightLog.append(self.players[self.game['whoPlays']]['pseudo'] + ' remonte à ' + str(self.players[self.game['whoPlays']]['hp']) + 'HP')
                    self.players[self.game['whoPlays']]['gui']['hpLabel'].config(text='HP : ' + str(self.players[self.game['whoPlays']]['hp']) + '/' + str(self.players[self.game['whoPlays']]['maxHp']))
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][0],
                                      self.players[self.game['whoPlays']]['x'] * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] - 0.15) * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['x'] + 1) * self.game['cellSize'],
                                      self.players[self.game['whoPlays']]['y'] * self.game['cellSize'])
                    gameCanvas.coords(self.players[self.game['whoPlays']]['hpBar'][1],
                                      self.players[self.game['whoPlays']]['x'] * self.game['cellSize'],
                                      (self.players[self.game['whoPlays']]['y'] - 0.15) * self.game['cellSize'], ((self.players[self.game['whoPlays']]['x'] + (self.players[self.game['whoPlays']]['hp'] / self.players[self.game['whoPlays']]['maxHp'])) * self.game['cellSize']),
                                      self.players[self.game['whoPlays']]['y'] * self.game['cellSize'])

                    # Animate
                    heal = gameCanvas.create_oval((self.players[self.game['whoPlays']]['x'] + 0.5) * self.game['cellSize'],
                                                  (self.players[self.game['whoPlays']]['y'] + 0.5) * self.game['cellSize'],
                                                  (self.players[self.game['whoPlays']]['x'] + 0.5) * self.game['cellSize'],
                                                  (self.players[self.game['whoPlays']]['y'] + 0.5) * self.game['cellSize'],
                                                  width=3, fill='', outline='chartreuse3')
                    for i in [x * 0.1 for x in range(0, 10)]:
                        gameCanvas.coords(heal,
                                    (self.players[self.game['whoPlays']]['x'] + 0.5 - 0.5 * i) * self.game['cellSize'],
                                    (self.players[self.game['whoPlays']]['y'] + 0.5 - 0.5 * i) * self.game['cellSize'],
                                    (self.players[self.game['whoPlays']]['x'] + 0.5 + 0.5 * i) * self.game['cellSize'],
                                    (self.players[self.game['whoPlays']]['y'] + 0.5 + 0.5 * i) * self.game['cellSize'])

                        root.update()
                        time.sleep(0.1-(i/10))

                    time.sleep(0.2)
                    gameCanvas.delete(heal)
                    root.update()

                elif action[0] == '[DEATH]':
                    self.fightLog.append(self.players[int(action[1])]['pseudo'] + ' est mort.')

                elif action[0] == '[END]':
                    self.fightLog.append('Fin de la partie.')

                if len(self.fightLog) > (self.game['height'] * self.game['cellSize']) / 20:
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
    # turn = pickTurnScale.get()


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
gameCanvas.grid(row=0, column=1)

# gui Frame

guiFrame = Frame(root)
guiFrame.grid(row=0, column=0)

gui = []

# gui Player 1
guiFramePlayer1 = Frame(guiFrame)
guiFramePlayer1.grid(row=0, column=0)
guiPseudoPlayer1 = Label(guiFramePlayer1, text='----')
guiPseudoPlayer1.grid(row=0, column=0)
guiCanvasPlayer1 = Canvas(guiFramePlayer1, width=50, height=50)
guiCanvasPlayer1.grid(row=1, column=0)
guiLabelPlayer1HP = Label(guiFramePlayer1, text='HP : --')
guiLabelPlayer1HP.grid(row=2, column=0)
guiLabelPlayer1Weapon = Label(guiFramePlayer1, text='Arme actuelle : --')
guiLabelPlayer1Weapon.grid(row=3, column=0)

gui.append([guiPseudoPlayer1, guiCanvasPlayer1, guiLabelPlayer1HP, guiLabelPlayer1Weapon])

# gui Player 2
guiFramePlayer2 = Frame(guiFrame)
guiFramePlayer2.grid(row=0, column=1)
guiPseudoPlayer2 = Label(guiFramePlayer2, text='----')
guiPseudoPlayer2.grid(row=0, column=0)
guiCanvasPlayer2 = Canvas(guiFramePlayer2, width=50, height=50)
guiCanvasPlayer2.grid(row=1, column=0)
guiLabelPlayer2HP = Label(guiFramePlayer2, text='HP : --')
guiLabelPlayer2HP.grid(row=2, column=0)
guiLabelPlayer2Weapon = Label(guiFramePlayer2, text='Arme actuelle : --')
guiLabelPlayer2Weapon.grid(row=3, column=0)

gui.append([guiPseudoPlayer2, guiCanvasPlayer2, guiLabelPlayer2HP, guiLabelPlayer2Weapon])

# Player frame
playerFrame = Frame(root)
playerFrame.grid(row=1, column=1)
pickTurnScale = Scale(playerFrame, from_=0, to=16, tickinterval=1, length=600, orient=HORIZONTAL, command=pickTurnUpdate)
pickTurnScale.grid(row=0, column=0)
togglePlayingButton = Button(playerFrame, text='Play', command=lambda: togglePlaying())
togglePlayingButton.grid(row=1, column=0)

# Infos frame
infosFrame = Frame(root, width=20)
infosFrame.grid(row=0, column=2)
logLabel = Label(infosFrame, text='Information Frame here', anchor="nw", justify=LEFT, width=20, font=("Helvetica", 10, "normal"))
logLabel.grid(row=0, column=0)

# Fight Thread
fightThread = replayThread(path)
fightThread.start()

root.mainloop()
fightThread.join()
