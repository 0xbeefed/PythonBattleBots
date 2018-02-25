import json
import os
import subprocess
import shutil
from threading import Thread
import time

fightInProgress = False
turn = 1
whoPlays = -1
history = []

class Steward(Thread):

    def __init__(self, path):
        Thread.__init__(self)
        self.game = {'id': -1, 'ias': ['1.py', '2.py'], 'maxTurns': 4, 'turn': 1, 'path': path, 'width': 16, 'height': 16}
        self.map = [[[-1] for i in range(self.game['width'])] for e in range(self.game['height'])] # -1: void | -2: obstacle | [0-9]*: entity ID
        self.players = []
        self.players.append({'x': 1, 'y': 1, 'id': 0})
        self.players.append({'x': self.game['width']-2, 'y': self.game['height']-2, 'id': 1})
        for who in self.players:
            self.map[who['y']][who['x']] = who['id']

    def run(self):
        global fightInProgress, turn, whoPlays, history
        print('[STEWARD]: started')
        while fightInProgress:
            try: # actionO = require treatment | actionX = allFine
                with open(self.game['path'] + 'actionO.dat', 'r+') as file:
                    response = 0
                    data = file.read().split(' ')
                    if (data[0] == '[MOVE]'):
                        x = int(data[1])
                        y = int(data[2])

                        if (x > 0 and x < self.game['width'] and y > 0 and y < self.game['height'] and self.map[y][x] == -1):
                            response = 1
                            self.map[self.players[whoPlays]['y']][self.players[whoPlays]['x']] = -1
                            self.players[whoPlays]['x'] = x
                            self.players[whoPlays]['y'] = y
                            self.map[y][x] = whoPlays
                            history.append('[MOVE] ' + str(x) + ' ' + str(y))

                    #response
                    file.seek(0)
                    file.write(str(response))
                os.rename(self.game['path'] + 'actionO.dat', self.game['path'] + 'actionX.dat')
            except PermissionError:
                continue
            except FileNotFoundError:
                continue
                
        print('[STEWARD]: end')
            
            

class Coordinator():

    def __init__(self):
        # VARIABLES #
        self.game = {'id': -1, 'ias': ['1.py', '2.py'], 'maxTurns': 4, 'path':''}
        self.globals = {}
        self.getGlobals()

        # GAME TREE #
        self.game['id'] = self.globals['gamesCount']
        self.game['path'] = 'Fights/' + str(self.game['id']) + '/'
        self.steward = Steward(self.game['path'])
        os.makedirs(self.game['path'])

        #dat files
        with open(self.game['path'] + 'replay.dat', 'w') as file:
            file.write('')
        with open(self.game['path'] + 'actionX.dat', 'w') as file:
            file.write('')

        self.globals['gamesCount'] += 1
        self.setGlobals()
        print('Created game id ' + str(self.game['id']))

        # LAUNCH GAME #
        print('Generating turns')
        self.processGame()

    def getGlobals(self):
        with open('globals.dat', 'r') as file:
            self.globals = json.loads(file.read())

    def setGlobals(self):
        with open('globals.dat', 'w+') as file:
            file.write(json.dumps(self.globals))

    def processGame(self):
        global fightInProgress, turn, whoPlays, history
        fightInProgress = True
        self.steward.start()
        for t in range(self.game['maxTurns']):
            turn = t
            history.append('[TURN] ' + str(turn))
            
            for i in range(len(self.game['ias'])):
                whoPlays = i
                history.append('[WHOPLAYS] ' + str(i))
                ia = self.game['ias'][i]
                
                # Launch IA
                result = subprocess.run(['python', 'IAs/' + ia, self.game['path']], stdout=subprocess.PIPE)
                with open(self.game['path'] + ia + '.dat', 'a') as file:
                    file.write('\nTurn ' + str(turn) + ': ' + str(result.stdout))
                    
        fightInProgress = False
        self.steward.join()

        #Save replay:
        with open(self.game['path'] + 'replay.dat', 'w') as file:
            file.write('\n'.join(history))
                

Coordinator()
