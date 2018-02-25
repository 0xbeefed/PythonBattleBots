from tkinter import *


game = {'width': 16, 'height': 16, 'cellSize': 20}
turn = 1
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

def move(action):
    global turn
    
    if action == 'up':
        dx, dy = 0, -1
    elif action == 'down':
        dx, dy = 0, 1
    elif action == 'left':
        dx, dy = -1, 0
    elif action == 'right':
        dx, dy = 1, 0

    player = players[turn%2].copy()
    
    player['x'] += dx
    player['y'] += dy
    if 0 <= player['x'] <= game['width'] and 0 <= player['y'] <= game['height']:
        gameCanvas.coords(player['icon'],player['x']*game['cellSize'],player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'])
        players[turn%2] = player
        if turn%2: # Player Red Turn
            turnLabel.configure(text = '-----Player Blue Turn-----')
        else: # Player Blue Turn
            turnLabel.configure(text = '-----Player Red Turn-----')  
        turn += 1    
    root.update()
        


upButton = Button(controlPanel, text = 'Up', command = lambda : move('up'))
upButton.grid(row = 0, column = 1)
downButton = Button(controlPanel, text = 'Down', command = lambda : move('down'))
downButton.grid(row = 2, column = 1)
leftButton = Button(controlPanel, text = 'Left', command = lambda : move('left'))
leftButton.grid(row = 1, column = 0)
rightButton = Button(controlPanel, text = 'Right', command = lambda : move('right'))
rightButton.grid(row = 1, column = 2)


# Grid
for x in range(game['width']):
    gameCanvas.create_line(x*game['cellSize'], 0, x*game['cellSize'], game['height']*game['cellSize'], width=1, fill='black')
for y in range(game['height']):
    gameCanvas.create_line(0, y*game['cellSize'], game['width']*game['cellSize'], y*game['cellSize'], width=1, fill='black')
# Players
for player in players:
    player['icon'] = gameCanvas.create_oval(player['x']*game['cellSize'], player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'], fill=player['color'])

root.mainloop()
