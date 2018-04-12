import json
import os
import subprocess
from random import randint
import math
import users.lib
import traceback

fightInProgress = False
turn = 1
whoPlays = -1

class Coordinator():

    def __init__(self, pId1, pId2):
        # VARIABLES #
        self.history = []
        with open('users/user' + str(pId1) + '/stat.dat') as file:
            user1Stat = json.loads(file.read())
        with open('users/user' + str(pId2) + '/stat.dat') as file:
            user2Stat = json.loads(file.read())

        self.game = {'id': -1, 'maxTurns': 16, 'path':'', 'turn': 1, 'whoPlays': -1, 'width': 16, 'height': 16}
        self.players = [
            {'pseudo': user1Stat['pseudo'], 'color': 'blue', 'x': 1, 'y': 1, 'currentWeapon' : -1, 'maxMp': user1Stat['maxMp'], 'mp': user1Stat['maxMp'], 'id': 0, 'maxTp': user1Stat['maxTp'], 'tp': user1Stat['maxTp'], 'hp': user1Stat['maxHp'], 'maxHp': user1Stat['maxHp']},
            {'pseudo': user2Stat['pseudo'], 'color': 'red', 'x': self.game['width']-2, 'y': self.game['height']-2, 'currentWeapon' : -1, 'maxMp': user2Stat['maxMp'], 'mp': user2Stat['maxMp'], 'id': 1, 'maxTp': user2Stat['maxTp'], 'tp': user2Stat['maxTp'], 'hp': user2Stat['maxHp'], 'maxHp': user2Stat['maxHp']}]

        self.history.append(json.dumps(self.players))
        exec("from users.user{0} import ai{1} as u1".format(pId1, pId1), globals())
        self.players[0]['ai'] = u1
        exec("from users.user{0} import ai{1} as u2".format(pId2, pId2), globals())
        self.players[1]['ai'] = u2

        self.globals = {}
        with open('globals.dat', 'r') as file:
            self.globals = file.read().split('\n')
        self.history.append(self.globals[1])
        self.spells = json.loads(self.globals[2])
        self.weapons = json.loads(self.globals[1])
        self.globals = json.loads(self.globals[0])

        # GAME TREE #
        i = 0
        while os.path.isfile('Fights/' + str(i) + '.dat'):
            i += 1
        self.game['id'] = i

        # DAT #
        with open('globals.dat', 'w+') as file:
            file.write(json.dumps(self.globals))
            file.write('\n')
            file.write(json.dumps(self.weapons))
            file.write('\n')
            file.write(json.dumps(self.spells))
        print('Created game id ' + str(self.game['id']))

        # GENERATING MAP #
        self.map = [[-1 for i in range(self.game['width'])] for o in range(self.game['height'])]
        for player in self.players:
            self.map[player['y']][player['x']] = player['id']
        placedObstacles = 0
        obstaclesToPlace = 20
        while placedObstacles < obstaclesToPlace:
            y = randint(0, len(self.map)-1)
            x = randint(0, len(self.map[y])-1)
            if (self.map[y][x] == -1):
                placedObstacles += 1
                self.map[y][x] = -2
        placedLavaHole = 0
        lavaHoleToPlace = 20
        while placedLavaHole < lavaHoleToPlace:
            y = randint(0, len(self.map)-1)
            x = randint(0, len(self.map[y])-1)
            if (self.map[y][x] == -1):
                placedLavaHole += 1
                self.map[y][x] = -3

        self.history.append(json.dumps(self.map))

        # LAUNCH GAME #
        self.processGame()

    def processGame(self):
        countAlivePlayers = len(self.players)
        for t in range(self.game['maxTurns']):
            self.game['turn'] = t
            print('\nGenerating turn ' + str(self.game['turn']) + ' / ' + str(self.game['maxTurns']-1))
            self.history.append('[TURN] ' + str(self.game['turn']))

            for i in range(len(self.players)):
                self.game['whoPlays'] = i
                self.history.append('[WHOPLAYS] ' + str(self.game['whoPlays']))

                # Stats
                self.players[self.game['whoPlays']]['mp'] = self.players[self.game['whoPlays']]['maxMp']
                self.players[self.game['whoPlays']]['tp'] = self.players[self.game['whoPlays']]['maxTp']

                # LAUNCH
                users.lib.MAP_DAT = self.map.copy()
                users.lib.GAME_DAT = self.game.copy()
                users.lib.PLAYERS_DAT = self.players.copy()
                self.players[self.game['whoPlays']]['ai'].lib.MAP_DAT = self.map.copy()
                self.players[self.game['whoPlays']]['ai'].lib.GAME_DAT = self.game.copy()
                self.players[self.game['whoPlays']]['ai'].lib.PLAYERS_DAT = self.players.copy()
                self.players[self.game['whoPlays']]['ai'].lib.actions = []
                self.players[self.game['whoPlays']]['ai'].lib.WEAPONS = self.weapons.copy()

                try:
                    self.players[self.game['whoPlays']]['ai'].main()
                except:
                    print(self.players[self.game['whoPlays']]['pseudo'] + ': IA exit with non 0 statement')
                    print(traceback.print_exc())
                result = self.players[self.game['whoPlays']]['ai'].lib.actions

                for action in result:

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
                            self.history.append(' '.join([str(a) for a in action]))
                            users.lib.MAP_DAT = self.map.copy()

                    elif len(action) and action[0] == '[MARK]':
                        self.history.append(' '.join([str(a) for a in action]))

                    elif len(action) and action[0] == '[ATTACK]' and self.players[self.game['whoPlays']]['currentWeapon'] != -1:
                        x = int(action[1])
                        y = int(action[2])
                        currentWeapon = self.players[self.game['whoPlays']]['currentWeapon']

                        distance = math.sqrt((self.players[self.game['whoPlays']]['x'] - x)**2 + (self.players[self.game['whoPlays']]['y'] - y)**2)
                        maxRange = self.weapons[currentWeapon]['maxRange']
                        cost = self.weapons[currentWeapon]['cost']
                        damage = self.weapons[currentWeapon]['damage']


                        if distance <= maxRange and self.players[self.game['whoPlays']]['tp'] >= cost: # 5 is max range of the weapon, 4 is the cost of attack

                            pos = [self.players[self.game['whoPlays']]['x'], self.players[self.game['whoPlays']]['y']]
                            pos2 = [x, y]

                            los = users.lib.getLineOfSight(pos, pos2)
                            if los:
                                for i in range(len(self.players)):
                                    if self.players[i]['x'] == x and self.players[i]['y'] == y:
                                        self.players[i]['hp'] -= damage
                                        self.players[self.game['whoPlays']]['tp'] -= cost
                                        self.history.append(' '.join([str(a) for a in action]))
                                        if (self.players[i]['hp'] <= 0):
                                            self.history.append('[DEATH] ' + str(self.players[i]['id']))
                                            countAlivePlayers -= 1
                                users.lib.PLAYERS_DAT = self.players.copy()

                    elif len(action) and action[0] == '[SET_WEAPON]':
                        if self.players[self.game['whoPlays']]['tp'] >= 1 and self.players[self.game['whoPlays']]['currentWeapon'] != action[1]:
                            self.players[self.game['whoPlays']]['currentWeapon'] = action[1]
                            self.players[self.game['whoPlays']]['tp'] -= 1
                            self.history.append(' '.join([str(a) for a in action]))

                    elif len(action) and action[0] == '[HEAL]':
                        if self.players[self.game['whoPlays']]['tp'] >= 4:
                            self.players[self.game['whoPlays']]['hp'] = min(self.players[self.game['whoPlays']]['hp'] + 5, self.players[self.game['whoPlays']]['maxHp'])
                            self.players[self.game['whoPlays']]['tp'] -= 4
                            self.history.append(' '.join([str(a) for a in action]))

            if countAlivePlayers <= 1:
                break
        print("End of the game")
        self.history.append('[END]')

        # Save replay:
        with open('Fights/' + str(self.game['id']) + '.dat', 'w') as file:
            file.write('\n'.join(self.history))
        subprocess.run(['python', 'player.py', 'Fights/' + str(self.game['id']) + '.dat'], stdout=subprocess.PIPE)# Play replay


Coordinator(0, 1)
