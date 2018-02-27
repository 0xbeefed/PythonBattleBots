from tkinter import *
import time
import sys
import json

if (len(sys.argv) > 1):
    path = sys.argv[1]
else:
    path = 'replay.dat'
replay = open(path, 'r')
replay = replay.read().split('\n')
Map = json.loads(replay[0])
replay = replay[1:]

game = {'width': len(Map), 'height': len(Map[0]), 'cellSize': 25}
players = []
players.append({'hp': 100, 'x': 1, 'y': 1, 'color': 'blue'})
players.append({'hp': 100, 'x': game['width']-2, 'y': game['height']-2, 'color': 'red'})
root = Tk()

gameCanvas = Canvas(root, width=game['width']*game['cellSize'], height=game['height']*game['cellSize'])
gameCanvas.grid(row = 0, column = 0)

informationPanel = Label(root)
informationPanel.grid(row = 0, column = 1)
turnLabel = Label(informationPanel, text = '-----Replay-----')
turnLabel.grid(row = 0, column = 0)
controlPanel = Label(informationPanel)
controlPanel.grid(row = 1, column = 0)

def watchReplay(replay):
    global VERBOSE, players
    player = 0
    turn = 0
    marks = []
    for action in replay:
        action = action.split(' ')
        delay = 0

        if action[0] == '[MOVE]':
            x = int(action[1])
            y = int(action[2])

            players[player]['x'] = x
            players[player]['y'] = y
            gameCanvas.coords(players[player]['icon'], players[player]['x']*game['cellSize'],players[player]['y']*game['cellSize'], (players[player]['x']+1)*game['cellSize'], (players[player]['y']+1)*game['cellSize'])
            root.update()
            time.sleep(0.12)

        if action[0] == '[MARK]':
            x = int(action[1])
            y = int(action[2])
            color = action[3]
            marks.append(gameCanvas.create_rectangle(x*game['cellSize'],y*game['cellSize'], (x+1)*game['cellSize'], (y+1)*game['cellSize'], fill=color, stipple='gray50'))
            root.update()
            time.sleep(0.02)
        
        elif action[0] == '[WHOPLAYS]':
            player = int(action[1])
            time.sleep(0.15) # wait before erasing marks
            for mark in marks:
                gameCanvas.delete(mark)
            marks = []
            root.update()
            
            
        elif action[0] == '[TURN]':
            turn = int(action[1])
            time.sleep(0.15)
 
startButton = Button(informationPanel, text = 'Play', command = lambda : watchReplay(replay))
startButton.grid(row = 2, column = 0)
   
# Grid
for x in range(game['width']):
    gameCanvas.create_line(x*game['cellSize'], 0, x*game['cellSize'], game['height']*game['cellSize'], width=1, fill='black')
for y in range(game['height']):
    gameCanvas.create_line(0, y*game['cellSize'], game['width']*game['cellSize'], y*game['cellSize'], width=1, fill='black')

# Numerotation
for x in range(game['width']):
    for y in range(game['height']):
        gameCanvas.create_text((x+0.5)*game['cellSize'], (y+0.5)*game['cellSize'], text='[{0}, {1}]'.format(x, y), justify='center', font=("Arial", 5))

# Obstacles
for y in range(len(Map)):
    for x in range(len(Map[y])):
        if Map[y][x] == -2:
            gameCanvas.create_rectangle(x*game['cellSize'],y*game['cellSize'], (x+1)*game['cellSize'], (y+1)*game['cellSize'], fill='black')

# Players
for player in players:
    player['icon'] = gameCanvas.create_oval(player['x']*game['cellSize'], player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'], fill=player['color'])

root.mainloop()
