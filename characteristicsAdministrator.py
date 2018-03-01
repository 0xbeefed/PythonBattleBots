from tkinter import *
from tkinter import filedialog
import json
import os

filename = ''
data = {'hp' : '-', 'mp' : '-', 'tp' : '-', 'cp' : '-', 'pseudo' : '-'}
values = {'hp' : 20, 'mp' : 1, 'tp' : 1}

def refresh():
    global data
    cpLabel.config(text = 'cp : ' + str(data['cp']))
    hpLabel.config(text = 'hp : ' + str(data['hp']))
    mpLabel.config(text = 'mp : ' + str(data['mp']))
    tpLabel.config(text = 'tp : ' + str(data['tp']))
    root.update()
    
def disableButtons():
    moreHpButton.config(state = DISABLED)
    lessHpButton.config(state = DISABLED)
    moreMpButton.config(state = DISABLED)
    lessMpButton.config(state = DISABLED)
    moreTpButton.config(state = DISABLED)
    lessTpButton.config(state = DISABLED)

def activateButtons():
    moreHpButton.config(state = NORMAL)
    lessHpButton.config(state = NORMAL)
    moreMpButton.config(state = NORMAL)
    lessMpButton.config(state = NORMAL)
    moreTpButton.config(state = NORMAL)
    lessTpButton.config(state = NORMAL)

def loadFile():
    global filename, data
    try:
        filename = filedialog.askopenfilename(parent = root)
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        pseudoEntry.delete(0,END)
        pseudoEntry.insert(0, data['pseudo'])
        activateButtons()
        refresh()
    except:
        pass
   
def updateStat(stat, value):
    global data
    if data['cp'] - value//values[stat] >= 0 and data[stat] + value > 0:
        data[stat] += value
        data['cp'] -= value//values[stat]
        refresh()
        
def save():
    global filename, data
    data['pseudo'] = pseudoEntry.get()
    with open(filename, 'w') as file:
        file.write(json.dumps(data))
    data = {'hp' : '-', 'mp' : '-', 'tp' : '-', 'cp' : '-', 'pseudo' : '-'}
    pseudoEntry.delete(0,END)
    pseudoEntry.insert(0, data['pseudo'])
    refresh()
    disableButtons()

def createProfil():
    global filename, data
    with open('globals.dat', 'r') as file:
        var = json.loads(file.read())
    data = {'hp' : 100, 'mp' : 3, 'tp' : 6, 'cp' : 0, 'pseudo' : 'user' + str(var['usersCount'])}
    filename = 'users/user' + str(var['usersCount']) + '/'
    os.makedirs(filename)
    filename += 'stat.dat'
    with open(filename, 'w+') as file:
        file.write(json.dumps(data))
    var['usersCount'] += 1  
    with open('globals.dat', 'w+') as file:
            file.write(json.dumps(var))
    updateStat('hp', 0)
    pseudoEntry.delete(0,END)
    pseudoEntry.insert(0, data['pseudo'])
    activateButtons()
    refresh()
    
root = Tk()
root.title('characteristicMaker')

statsLabel = Label(root)
statsLabel.grid(row = 0, column = 0)

saveLabel = Label(root)
saveLabel.grid(row = 1, column = 0)
saveButton = Button(saveLabel, text = 'save characteristic', command = save)
saveButton.grid(row = 0, column = 0)
loadButton = Button(saveLabel, text = 'load stat', command = loadFile)
loadButton.grid(row = 0, column = 1)
createButton = Button(saveLabel, text = 'create profil', command = createProfil)
createButton.grid(row = 0, column = 2)

pseudoLabel = Label(statsLabel, text = 'pseudo : ')
pseudoLabel.grid(row = 0, column = 0)
pseudoEntry = Entry(statsLabel, text = 'pseudo')
pseudoEntry.grid(row = 0, column = 1)
pseudoEntry.insert(0,data['pseudo'])

cpLabel = Label(statsLabel, text = 'cp : ' + str(data['cp']))
cpLabel.grid(row = 1, column = 0)

hpLabel = Label(statsLabel, text = 'hp : ' + str(data['hp']))
hpLabel.grid(row = 2, column = 0)
moreHpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('hp', values['hp']))
moreHpButton.grid(row = 2, column = 1)
lessHpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('hp', -values['hp']))
lessHpButton.grid(row = 2, column = 2)

mpLabel = Label(statsLabel, text = 'mp : ' + str(data['mp']))
mpLabel.grid(row = 3, column = 0)
moreMpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('mp', values['mp']))
moreMpButton.grid(row = 3, column = 1)
lessMpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('mp', -values['mp']))
lessMpButton.grid(row = 3, column = 2)

tpLabel = Label(statsLabel, text = 'tp : ' + str(data['tp']))
tpLabel.grid(row = 4, column = 0)
moreTpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('tp', values['tp']))
moreTpButton.grid(row = 4, column = 1)
lessTpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('tp', -values['tp']))
lessTpButton.grid(row = 4, column = 2)

root.mainloop()
