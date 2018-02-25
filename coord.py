import json
import os
import subprocess
import shutil
from threading import Thread
import time

fightInProgress = False

class Steward(Thread):

    def __init__(self, path):
        Thread.__init__(self)
        self.path = path

    def run(self):
        global fightInProgress
        print('[STEWARD]: started')
        while fightInProgress:
            try: # actionO = require treatment | actionX = allFine
                with open(self.path + 'actionO.dat', 'r+') as file:
                    print('[STEWARD]: command -> ' + file.read())
                    file.seek(0)
                    file.write('message from steward')
                os.rename(self.path + 'actionO.dat', self.path + 'actionX.dat')
            except:
                continue
                
        print('[STEWARD]: end')
            
            

class Coordinator():

    def __init__(self):
        # VARIABLES #
        self.game = {'id': -1, 'ias': ['1.py', '2.py'], 'maxTurns': 4, 'turn': 1, 'path':''}
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
        with open(self.game['path'] + 'game.dat', 'w') as file:
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

    def updateGame(self):
        with open(self.game['path'] + 'game.dat', 'w+') as file:
            file.write(json.dumps(self.game))

    def processGame(self):
        global fightInProgress
        fightInProgress = True
        self.steward.start()
        for turn in range(self.game['maxTurns']):
            self.turn = turn
            for ia in self.game['ias']:
                # Launch IA
                result = subprocess.run(['python', 'C:/Users/arthc/Desktop/ProG2/IAs/' + ia, self.game['path']], stdout=subprocess.PIPE)
                with open(self.game['path'] + ia + '.dat', 'a') as file:
                    file.write('\nTurn ' + str(turn) + ': ' + str(result.stdout))
                    
                # Update
                self.updateGame()
        fightInProgress = False
        self.steward.join()

Coordinator()
