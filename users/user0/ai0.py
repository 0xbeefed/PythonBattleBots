import sys
sys.path.append(sys.path[0] + '/users/')
import lib
import time

def minimax(grid, depth):
    moves = grid.availableMoves()
    best_move = moves[0]
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    random_moves = []
    pos = grid.players[grid.whoPlay]['position']
    for move in moves[::-1]:
        grid.execute(move)
        score = min_play(grid, depth - 1, alpha, beta)
        print('MINIMAX', move, score, file = sys.stderr)
        grid.undo(move, pos)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

def min_play(grid, depth, alpha, beta):
    if depth < 0 or grid.gameOver():
        return grid.evaluate()
    moves = grid.availableMoves()
    best_score = float('inf')
    pos = grid.players[grid.whoPlay]['position']
    for move in moves:
        grid.execute(move)
        best_score = min(best_score, max_play(grid, depth - 1, alpha, beta))
        grid.undo(move, pos)
        if alpha >= best_score:
            return best_score
        beta = min(beta, best_score)
    return best_score


def max_play(grid, depth, alpha, beta):
    if depth < 0 or grid.gameOver():
        return grid.evaluate()
    moves = grid.availableMoves()
    best_score = float('-inf')
    pos = grid.players[grid.whoPlay]['position']
    for move in moves:
        grid.execute(move)
        best_score = max(best_score, min_play(grid, depth - 1, alpha, beta))
        grid.undo(move, pos)
        if best_score >= beta:
            return best_score
        alpha = max(alpha, best_score)
    return best_score

class Grid:
    def __init__(self, myId, opponentId):
        
        self.whoPlay = myId
        self.myId = myId
        self.opponentId = opponentId
        self.players = [{'position': lib.getCell(0), 'currentWeapon': -1, 'mp': lib.getMp(0), 'tp': lib.getTp(0), 'hp': lib.getHp(0), 'maxHp': lib.getMaxHp(0)},
                        {'position': lib.getCell(1), 'currentWeapon': -1, 'mp': lib.getMp(1), 'tp': lib.getTp(1), 'hp': lib.getHp(1), 'maxHp': lib.getMaxHp(1)}]
        
        self.weapons = [lib.getWeaponEffects(lib.WEAPON_SIMPLE_GUN), lib.getWeaponEffects(lib.WEAPON_SWORD)]
        
        self.players[self.myId]['currentWeapon'] = lib.WEAPON_SIMPLE_GUN
        self.players[self.opponentId]['currentWeapon'] = lib.WEAPON_SIMPLE_GUN
        #self.availableMoves()

    def evaluate(self):
        #print(self.players[self.myId]['position'], self.myId, self.whoPlay)
        return self.players[self.myId]['hp']-self.players[self.opponentId]['hp']
        if self.players[self.myId]['hp']//self.players[self.myId]['maxHp'] < 0.5:
            return (self.players[self.myId]['hp'] - self.players[self.opponentId]['hp'])*1000 + lib.getDistance(self.players[self.myId]['position'], self.players[self.opponentId]['position'])
        else:
            return (self.players[self.myId]['hp'] - self.players[self.opponentId]['hp'])*1000 - lib.getDistance(self.players[self.myId]['position'], [8, 8])
        
    def execute(self, move):
        self.players[self.whoPlay]['position'] = [move[0], move[1]]
        if move[2] == '[ATTACK]':
            self.players[1 - self.whoPlay]['hp'] = max(0, self.players[1 - self.whoPlay]['hp'] - move[3]['damage'])
        elif move[2] == '[FLEE]':
            self.players[self.whoPlay]['hp'] = min(self.players[self.whoPlay]['hp'] + 5, self.players[self.whoPlay]['maxHp'])
        self.whoPlay = 1 - self.whoPlay
        
    def undo(self, move, lastPos):
        self.whoPlay = 1 - self.whoPlay
        self.players[self.whoPlay]['position'] = list(lastPos)
        if move[2] == '[ATTACK]':
            self.players[1 - self.whoPlay]['hp'] = min(self.players[self.whoPlay]['maxHp'], self.players[1 - self.whoPlay]['hp'] + self.weapons[self.players[self.whoPlay]['currentWeapon']]['damage'])
        elif move[2] == '[FLEE]':
            self.players[self.whoPlay]['hp'] = max(self.players[self.whoPlay]['hp'] - 5, 0)

    def availableMoves(self):
        mp = self.players[self.whoPlay]['mp']
        x, y = self.players[self.whoPlay]['position']
        #print('X/Y', x, y)
        path = lib.getPath(list(self.players[self.whoPlay]['position']), list(self.players[1 - self.whoPlay]['position']))
        if path != -1:
            moves = [path[0]]
            moves[0].append('[FLEE]')
            """if len(path) <= 4:
                print('path', path[2])
                moves.append[path[max(0, len(path) - 2)]]
                moves[1].append('[ATTACK]', self.weapons[lib.WEAPON_SWORD])"""
        else:
            moves = [list(self.players[self.whoPlay]['position'])]
            moves[0].append('[FLEE]')
        if self.whoPlay == self.myId:    
            for weapon in self.weapons:
                accessibleCells = [[x, y]]
                enemyPos = lib.getCell(1-self.whoPlay)
                weaponRange = weapon['maxRange']
                
                last = [[x, y]]
                while mp >= 0:
                    tmp = []
                    for cell in last:
                        if lib.getLineOfSight(cell, enemyPos) and lib.getDistance(cell, enemyPos) <= weaponRange:
                            moves.append(tuple(cell) + tuple(['[ATTACK]', weapon]))
                            mp = 0
                        else:
                            for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                                if lib.getCellContent((cell[0] + dx, cell[1] + dy)) == lib.CELL_EMPTY and not [cell[0] + dx, cell[1] + dy] in accessibleCells:
                                    tmp.append([cell[0] + dx, cell[1] + dy])
                                    accessibleCells.append([cell[0] + dx, cell[1] + dy])
                    mp -= 1
                    last = tmp.copy()
        else:
            accessibleCells = [[x, y]]
            enemyPos = lib.getCell(1-self.whoPlay)
            weaponRange = self.weapons[self.players[self.whoPlay]['currentWeapon']]['maxRange']
                
            last = [[x, y]]
            while mp >= 0:
                tmp = []
                for cell in last:
                    if lib.getLineOfSight(cell, enemyPos) and lib.getDistance(cell, enemyPos) <= weaponRange:
                        moves.append(tuple(cell) + tuple(['[ATTACK]', self.weapons[self.players[self.whoPlay]['currentWeapon']]]))
                        mp = 0
                    else:
                        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                            if lib.getCellContent((cell[0] + dx, cell[1] + dy)) == lib.CELL_EMPTY and not [cell[0] + dx, cell[1] + dy] in accessibleCells:
                                tmp.append([cell[0] + dx, cell[1] + dy])
                                accessibleCells.append([cell[0] + dx, cell[1] + dy])
                mp -= 1
                last = tmp.copy()
                
        # Defensive moves
        mp = self.players[self.whoPlay]['mp']
        last = [[x, y]]
        accessibleCells = [[x, y]]
        defMoves = []
        while mp > 0:
            tmp = []
            h = False
            if defMoves:
                h = True
            for cell in last:
                for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                    if (lib.getCellContent((cell[0] + dx, cell[1] + dy)) == lib.CELL_EMPTY) and not [cell[0] + dx, cell[1] + dy] in accessibleCells:
                        tmp.append([cell[0] + dx, cell[1] + dy])
                        accessibleCells.append([cell[0] + dx, cell[1] + dy])
                        if not lib.getLineOfSight([cell[0] + dx, cell[1] + dy], enemyPos):
                            if h:
                                defMoves = []
                                h = False
                            defMoves.append((cell[0] + dx, cell[1] + dy, '[FLEE]'))
                        
                            
            mp -= 1
            last = tmp.copy()
            
        for move in defMoves:
            moves.append(move)
            
        return moves

    def gameOver(self):
        if self.players[0]['hp'] <= 0 or self.players[1]['hp'] <= 0:
            return 1
        return 0   

def main():
    # Variables
    path = lib.getPath(lib.getCell(lib.getMyId()), lib.getCell(lib.getEnemyId()))
    if path != -1:
        lib.mark(path, 'blue')
    start = time.time()
    lib.setWeapon(lib.WEAPON_SWORD)
    grid = Grid(lib.getMyId(), lib.getEnemyId())
    best_move = minimax(grid, 3)
    path = lib.getPath(lib.getCell(lib.getMyId()), [best_move[0], best_move[1]])
    print(best_move, path, file=sys.stderr)
    if path != -1:
        for cell in path:
            lib.moveOn(cell)
    if best_move[2] == '[FLEE]':
        lib.useHeal([best_move[0], best_move[1]])
    elif best_move[2] == '[ATTACK]':
        if best_move[3]['name'] == 'SimpleGun':
            lib.setWeapon(lib.WEAPON_SIMPLE_GUN)
        elif best_move[3]['name'] == 'Sword':
            lib.setWeapon(lib.WEAPON_SWORD)
        lib.attackOn(lib.getCell(lib.getEnemyId()))
        for cell in lib.getPath(lib.getCell(lib.getMyId()), lib.getCell(lib.getEnemyId())):
            lib.moveOn(cell)
    print(time.time()-start, file=sys.stderr)


    
