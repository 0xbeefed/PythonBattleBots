from tkinter import *
from tkinter import filedialog
import json
import os

filename = ''
data = {'maxHp' : '-', 'maxMp' : '-', 'maxTp' : '-', 'cp' : '-', 'pseudo' : '-'}
values = {'maxHp' : 20, 'maxMp' : 1, 'maxTp' : 1}

def refresh():
    global data
    cpLabel.config(text = 'cp : ' + str(data['cp']))
    hpLabel.config(text = 'hp : ' + str(data['maxHp']))
    mpLabel.config(text = 'mp : ' + str(data['maxMp']))
    tpLabel.config(text = 'tp : ' + str(data['maxTp']))
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
    data = {'maxHp' : '-', 'maxMp' : '-', 'maxTp' : '-', 'cp' : '-', 'pseudo' : '-'}
    pseudoEntry.delete(0,END)
    pseudoEntry.insert(0, data['pseudo'])
    refresh()
    disableButtons()

def createProfil():
    global filename, data
    with open('globals.dat', 'r') as file:
        var = json.loads(file.read())
    data = {'maxHp' : 100, 'maxMp' : 3, 'maxTp' : 6, 'cp' : 0, 'pseudo' : 'user' + str(var['usersCount'])}
    filename = 'users/' + str(var['usersCount']) + '/'
    os.makedirs(filename)
    filename += 'stat.dat'
    with open(filename, 'w+') as file:
        file.write(json.dumps(data))
    var['usersCount'] += 1  
    with open('globals.dat', 'w+') as file:
            file.write(json.dumps(var))
    updateStat('maxHp', 0)
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

hpLabel = Label(statsLabel, text = 'hp : ' + str(data['maxHp']))
hpLabel.grid(row = 2, column = 0)
moreHpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('maxHp', values['maxHp']))
moreHpButton.grid(row = 2, column = 1)
lessHpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('maxHp', -values['maxHp']))
lessHpButton.grid(row = 2, column = 2)

mpLabel = Label(statsLabel, text = 'mp : ' + str(data['maxMp']))
mpLabel.grid(row = 3, column = 0)
moreMpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('maxMp', values['maxMp']))
moreMpButton.grid(row = 3, column = 1)
lessMpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('maxMp', -values['maxMp']))
lessMpButton.grid(row = 3, column = 2)

tpLabel = Label(statsLabel, text = 'tp : ' + str(data['maxTp']))
tpLabel.grid(row = 4, column = 0)
moreTpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('maxTp', values['maxTp']))
moreTpButton.grid(row = 4, column = 1)
lessTpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('maxTp', -values['maxTp']))
lessTpButton.grid(row = 4, column = 2)

root.mainloop()
