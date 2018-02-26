import json
import os
import subprocess
import shutil
from threading import Thread
import time
from random import randint

fightInProgress = False
turn = 1
whoPlays = -1

class Coordinator():

    def __init__(self):
        # VARIABLES #
        self.game = {'id': -1, 'ias': ['1.py', '2.py'], 'maxTurns': 10, 'path':'', 'turn': 1, 'whoPlays': -1, 'width': 16, 'height': 16}
        self.players = [
            {'x': 1, 'y': 1, 'maxMp': 3, 'mp': 3, 'id': 0},
            {'x': self.game['width']-2, 'y': self.game['height']-2, 'maxMp': 3, 'mp': 3, 'id': 1}
            ]
        self.globals = {}
        with open('globals.dat', 'r') as file:
            self.globals = json.loads(file.read())
        self.history = []

        # GAME TREE #
        self.game['id'] = self.globals['gamesCount']
        self.game['path'] = 'Fights/' + str(self.game['id']) + '/'
        os.makedirs(self.game['path'])

        # DAT #
        with open(self.game['path'] + 'actionX.dat', 'w') as file:
            file.write('')
        self.globals['gamesCount'] += 1
        with open('globals.dat', 'w+') as file:
            file.write(json.dumps(self.globals))
        print('Created game id ' + str(self.game['id']))

        # GENERATING MAP #
        self.map = [[-1 for i in range(self.game['width'])] for o in range(self.game['height'])]
        for player in self.players:
            self.map[player['y']][player['x']] = player['id']
        placedObstacles = 0
        obstaclesToPlace = 15
        while placedObstacles < obstaclesToPlace:
            y = randint(0, len(self.map)-1)
            x = randint(0, len(self.map[y])-1)
            if (self.map[y][x] == -1):
                placedObstacles += 1
                self.map[y][x] = -2
        self.history.append(json.dumps(self.map))

        # LAUNCH GAME #
        print('Generating turns')
        self.processGame()
        
    def processGame(self):
        for t in range(self.game['maxTurns']):
            self.game['turn'] = t
            self.history.append('[TURN] ' + str(self.game['turn']))
            
            for i in range(len(self.game['ias'])):
                self.game['whoPlays'] = i
                self.history.append('[WHOPLAYS] ' + str(self.game['whoPlays']))
                ia = self.game['ias'][self.game['whoPlays']]

                # Stats
                self.players[self.game['whoPlays']]['mp'] = self.players[self.game['whoPlays']]['maxMp']

                # UPDATE CHANGES
                with open(self.game['path'] + 'players.dat', 'w') as file:
                    file.write(json.dumps(self.players))
                with open(self.game['path'] + 'map.dat', 'w') as file:
                    file.write(json.dumps(self.map))
                with open(self.game['path'] + 'game.dat', 'w') as file:
                    file.write(json.dumps(self.game)) 
                
                # LAUNCH
                result = str(subprocess.run(['python', 'IAs/' + ia, self.game['path']], stdout=subprocess.PIPE).stdout.decode('utf-8'))
                with open(self.game['path'] + ia + '.dat', 'a') as file: # Debug
                    file.write('\nTurn ' + str(self.game['turn']) + ': ' + result)
                for action in result.split('\r\n'):
                    action = action.split(' ')

                    if len(action) and action[0] == '[MOVE]':
                        x = int(action[1])
                        y = int(action[2])

                        
                        if (abs(self.players[self.game['whoPlays']]['y'] - y) + abs(self.players[self.game['whoPlays']]['x'] - x) == 1
                            and x >= 0 and y >= 0 and y < len(self.map) and x < len(self.map[y])
                            and self.map[y][x] == -1
                            and self.players[self.game['whoPlays']]['mp'] >= 1):
                            
                            self.map[self.players[self.game['whoPlays']]['y']][self.players[self.game['whoPlays']]['x']] = 0
                            self.players[self.game['whoPlays']]['x'] = x
                            self.players[self.game['whoPlays']]['y'] = y
                            self.map[y][x] = self.game['whoPlays']
                            self.players[self.game['whoPlays']]['mp'] -= 1
                            self.history.append(' '.join(action))
                            

                        
                    elif len(action) and action[0] == '[ATTACK]':
                        x = action[1]
                        y = action[2]
                        item = action[3]


        # Save replay:
        with open(self.game['path'] + 'replay.dat', 'w') as file:
            file.write('\n'.join(self.history))
        subprocess.run(['python', 'player.py', self.game['path'] + 'replay.dat'], stdout=subprocess.PIPE)# Play replay
                

Coordinator()
