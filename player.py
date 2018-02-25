from tkinter import *
import time

VERBOSE = False
replay = open('replayFormat2', 'r')
replay = replay.read().split('\n')

game = {'width': 16, 'height': 16, 'cellSize': 20}
players = []
players.append({'hp': 100, 'x': 1, 'y': 1, 'color': 'blue'})
players.append({'hp': 100, 'x': game['width']-2, 'y': game['height']-2, 'color': 'red'})
root = Tk()

gameCanvas = Canvas(root, width=game['width']*game['cellSize'], height=game['height']*game['cellSize'])
gameCanvas.grid(row = 0, column = 0)

informationPanel = Label(root)
informationPanel.grid(row = 0, column = 1)
turnLabel = Label(informationPanel, text = '-----Player Red Turn-----')
turnLabel.grid(row = 0, column = 0)
controlPanel = Label(informationPanel)
controlPanel.grid(row = 1, column = 0)

def move(action, index_player):    
    if action == 'up':
        dx, dy = 0, -1
    elif action == 'down':
        dx, dy = 0, 1
    elif action == 'left':
        dx, dy = -1, 0
    elif action == 'right':
        dx, dy = 1, 0

    player = players[index_player].copy()
    
    player['x'] += dx
    player['y'] += dy
    if 0 <= player['x'] <= game['width'] and 0 <= player['y'] <= game['height']:
        gameCanvas.coords(player['icon'],player['x']*game['cellSize'],player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'])
        players[index_player] = player 
           
    root.update()

def watchReplay(replay):
    global VERBOSE
    player = 0
    turn = 0
    for action in replay:
        if VERBOSE:
            print(action)
        action = action.split(' ')
        if action[0] == '[MOVE]':
            direction = [players[player]['y']-int(action[1]), players[player]['x']-int(action[2])]
            if direction == [0, 1]: move('left', player)
            elif direction == [0 ,-1]: move('right', player)
            elif direction == [1, 0]: move('up', player)
            elif direction == [-1, 0]: move('down', player)
            
        elif action[0] == '[WHOPLAYS]':
            player = int(action[1])
        elif action[0] == '[TURN]':
            turn = int(action[1])
            
        time.sleep(0.025)
 
startButton = Button(informationPanel, text = 'start replay', command = lambda : watchReplay(replay))
startButton.grid(row = 2, column = 0)
   
# Grid
for x in range(game['width']):
    gameCanvas.create_line(x*game['cellSize'], 0, x*game['cellSize'], game['height']*game['cellSize'], width=1, fill='black')
for y in range(game['height']):
    gameCanvas.create_line(0, y*game['cellSize'], game['width']*game['cellSize'], y*game['cellSize'], width=1, fill='black')
# Players
for player in players:
    player['icon'] = gameCanvas.create_oval(player['x']*game['cellSize'], player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'], fill=player['color'])

root.mainloop()
