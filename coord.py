import json
import os
import subprocess
import shutil
from threading import Thread
import time
from random import randint
import math

fightInProgress = False
turn = 1
whoPlays = -1

class Coordinator():

    def __init__(self, pId1, pId2):
        # VARIABLES #
        with open('users/' + str(pId1) + '/stat.dat') as file:
            user1Stat = json.loads(file.read())
        with open('users/' + str(pId2) + '/stat.dat') as file:
            user2Stat = json.loads(file.read())
            
        self.game = {'id': -1, 'maxTurns': 16, 'path':'', 'turn': 1, 'whoPlays': -1, 'width': 16, 'height': 16}
        self.players = [
            {'pseudo': user1Stat['pseudo'], 'color': 'blue', 'x': 1, 'y': 1, 'ia': 'users/' + str(pId1) + '/ai.py', 'maxMp': user1Stat['maxMp'], 'mp': user1Stat['maxMp'], 'id': 0, 'maxTp': user1Stat['maxTp'], 'tp': user1Stat['maxTp'], 'hp': user1Stat['maxHp'], 'maxHp': user1Stat['maxHp']},
            {'pseudo': user2Stat['pseudo'], 'color': 'red', 'x': self.game['width']-2, 'y': self.game['height']-2, 'ia': 'users/' + str(pId2) + '/ai.py', 'maxMp': user2Stat['maxMp'], 'mp': user2Stat['maxMp'], 'id': 1, 'maxTp': user2Stat['maxTp'], 'tp': user2Stat['maxTp'], 'hp': user2Stat['maxHp'], 'maxHp': user2Stat['maxHp']}
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
        self.globals['gamesCount'] += 1
        with open('globals.dat', 'w+') as file:
            file.write(json.dumps(self.globals))
        print('Created game id ' + str(self.game['id']))

        # GENERATING MAP #
        self.map = [[-1 for i in range(self.game['width'])] for o in range(self.game['height'])]
        for player in self.players:
            self.map[player['y']][player['x']] = player['id']
        placedObstacles = 0
        obstaclesToPlace = 40
        while placedObstacles < obstaclesToPlace:
            y = randint(0, len(self.map)-1)
            x = randint(0, len(self.map[y])-1)
            if (self.map[y][x] == -1):
                placedObstacles += 1
                self.map[y][x] = -2
        self.history.append(json.dumps(self.players))
        self.history.append(json.dumps(self.map))

        # LAUNCH GAME #
        print('Generating turns')
        self.processGame()
        
    def processGame(self):
        for t in range(self.game['maxTurns']):
            self.game['turn'] = t
            print('Generating turn ' + str(self.game['turn']) + ' / ' + str(self.game['maxTurns']-1))
            self.history.append('[TURN] ' + str(self.game['turn']))
            
            for i in range(len(self.players)):
                self.game['whoPlays'] = i
                self.history.append('[WHOPLAYS] ' + str(self.game['whoPlays']))
                ia = self.players[self.game['whoPlays']]['ia']

                # Stats
                self.players[self.game['whoPlays']]['mp'] = self.players[self.game['whoPlays']]['maxMp']
                self.players[self.game['whoPlays']]['tp'] = self.players[self.game['whoPlays']]['maxTp']

                # UPDATE CHANGES
                with open(self.game['path'] + 'players.dat', 'w') as file:
                    file.write(json.dumps(self.players))
                with open(self.game['path'] + 'map.dat', 'w') as file:
                    file.write(json.dumps(self.map))
                with open(self.game['path'] + 'game.dat', 'w') as file:
                    file.write(json.dumps(self.game)) 
                
                # LAUNCH
                result = str(subprocess.run(['python', ia, self.game['path']], stdout=subprocess.PIPE).stdout.decode('utf-8'))
                with open(self.game['path'] + self.players[self.game['whoPlays']]['pseudo'] + '.dat', 'a') as file: # Debug
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
                            
                            self.map[self.players[self.game['whoPlays']]['y']][self.players[self.game['whoPlays']]['x']] = -1
                            self.players[self.game['whoPlays']]['x'] = x
                            self.players[self.game['whoPlays']]['y'] = y
                            self.map[y][x] = self.game['whoPlays']
                            self.players[self.game['whoPlays']]['mp'] -= 1
                            self.history.append(' '.join(action))

                    elif len(action) and action[0] == '[MARK]':
                        self.history.append(' '.join(action))

                        
                    elif len(action) and action[0] == '[ATTACK]':
                        x = int(action[1])
                        y = int(action[2])
                        distance = math.sqrt((self.players[self.game['whoPlays']]['x'] - x)**2 + (self.players[self.game['whoPlays']]['y'] - y)**2)
                        
                        if distance <= 5 and self.players[self.game['whoPlays']]['tp'] >= 4: # 5 is max range of the weapon, 4 is the cost of attack
                            # CHECK LOS
                            obstacles = []
                            for y1 in range(len(self.map)):
                                for x1 in range(len(self.map[0])):
                                    if self.map[y1][x1] != -1:
                                        obstacles.append([x1, y1])

                            los = 1
                            pos = [self.players[self.game['whoPlays']]['x'], self.players[self.game['whoPlays']]['y']]
                            pos2 = [x, y]
                            for obstacle in obstacles:
                                u = 0
                                d = 0
                                if (obstacle[0] > pos[0]) == (pos2[0] > pos[0]) and (obstacle[1] > pos[1]) == (pos2[1] > pos[1]) and abs(obstacle[0]-pos[0])+abs(obstacle[1]-pos[1]) < abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1]) and obstacle != pos:
                                    for a, b in [[0,0], [0,1], [1,0], [1,1]]: # Check that the 4 corners of the obstacle are below or above the line between pos and [x,y]
                                        if obstacle[1]+b > ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                                            u += 1
                                        if obstacle[1]+b < ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                                            d += 1
                                        if obstacle[1]+b == ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                                            u += 1
                                            d += 1
                                    if d != 4 and u != 4:
                                        los = 0
                            if los:
                                for i in range(len(self.players)):
                                    if self.players[i]['x'] == x and self.players[i]['y'] == y:
                                        self.players[i]['hp'] -= 10
                                        self.players[self.game['whoPlays']]['tp'] -= 4
                                        self.history.append(' '.join(action))
                                        if (self.players[i]['hp'] <= 0):
                                            self.history.append('[DEATH] ' + str(self.players[i]['id']))


        # Save replay:
        with open(self.game['path'] + 'replay.dat', 'w') as file:
            file.write('\n'.join(self.history))
        subprocess.run(['python', 'player.py', self.game['path'] + 'replay.dat'], stdout=subprocess.PIPE)# Play replay
                

Coordinator(0, 1)
