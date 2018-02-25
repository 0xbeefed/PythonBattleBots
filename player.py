from tkinter import *


game = {'width': 10, 'height': 10, 'cellSize': 30}
players = []
players.append({'hp': 100, 'x': 1, 'y': 1, 'color': 'blue'})
players.append({'hp': 100, 'x': game['width']-2, 'y': game['height']-2, 'color': 'red'})


root = Tk()
gameCanvas = Canvas(root, width=game['width']*game['cellSize'], height=game['height']*game['cellSize'])
gameCanvas.pack()

# Grid
for x in range(game['width']):
    gameCanvas.create_line(x*game['cellSize'], 0, x*game['cellSize'], game['height']*game['cellSize'], width=1, fill='black')
for y in range(game['height']):
    gameCanvas.create_line(0, y*game['cellSize'], game['width']*game['cellSize'], y*game['cellSize'], width=1, fill='black')
# Players
for player in players:
    gameCanvas.create_oval(player['x']*game['cellSize'], player['y']*game['cellSize'], (player['x']+1)*game['cellSize'], (player['y']+1)*game['cellSize'], fill=player['color'])

root.mainloop()
