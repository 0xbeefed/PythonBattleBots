from tkinter import *
from tkinter import filedialog
import json
import os

path = ''
data = {'maxHp': '-', 'maxMp': '-', 'maxTp': '-', 'cp': '-', 'pseudo': '-'}
values = {'maxHp': 20, 'maxMp': 1, 'maxTp': 1}


def refresh():
    global data
    cpLabel.config(text='cp : ' + str(data['cp']))
    hpLabel.config(text='hp : ' + str(data['maxHp']))
    mpLabel.config(text='mp : ' + str(data['maxMp']))
    tpLabel.config(text='tp : ' + str(data['maxTp']))
    root.update()


def disableButtons():
    moreHpButton.config(state=DISABLED)
    lessHpButton.config(state=DISABLED)
    moreMpButton.config(state=DISABLED)
    lessMpButton.config(state=DISABLED)
    moreTpButton.config(state=DISABLED)
    lessTpButton.config(state=DISABLED)


def activateButtons():
    moreHpButton.config(state=NORMAL)
    lessHpButton.config(state=NORMAL)
    moreMpButton.config(state=NORMAL)
    lessMpButton.config(state=NORMAL)
    moreTpButton.config(state=NORMAL)
    lessTpButton.config(state=NORMAL)


def loadFile():
    global path, data
    try:
        path = filedialog.askopenfilename(parent=root)
        with open(path, 'r') as file:
            data = json.loads(file.read())
        pseudoEntry.delete(0, END)
        pseudoEntry.insert(0, data['pseudo'])
        activateButtons()
        refresh()
    except:
        pass


def updateStat(stat, value):
    global data
    if data['cp'] - value // values[stat] >= 0 and data[stat] + value > 0:
        data[stat] += value
        data['cp'] -= value // values[stat]
        refresh()


def save():
    global path, data
    data['pseudo'] = pseudoEntry.get()
    with open(path, 'w') as file:
        file.write(json.dumps(data))
    data = {'maxHp': '-', 'maxMp': '-', 'maxTp': '-', 'cp': '-', 'pseudo': '-'}
    pseudoEntry.delete(0, END)
    pseudoEntry.insert(0, data['pseudo'])
    refresh()
    disableButtons()


def createProfil():
    global path, data
    userId = 0
    while os.path.isfile('users/user' + str(userId) + '/stat.dat'):
        userId += 1
    data = {'maxHp': 100, 'maxMp': 3, 'maxTp': 6, 'cp': 0, 'pseudo': 'user' + str(userId)}
    path = 'users/user' + str(userId) + '/'
    os.makedirs(path)

    with open(path + 'stat.dat', 'w+') as file:
        file.write(json.dumps(data))
    with open(path + 'ai' + str(userId) + '.py', 'w+') as file:
        file.write('\n'.join(['import sys', 'sys.path.append(sys.path[0] + "/users/")', 'import lib', '', 'def main():', '   # Write your code for a turn here', '   pass']))

    updateStat('maxHp', 0)
    pseudoEntry.delete(0, END)
    pseudoEntry.insert(0, data['pseudo'])
    activateButtons()
    refresh()


root = Tk()
root.title('Character Administrator')

statsFrame = Frame(root)
statsFrame.grid(row=0, column=0)

saveFrame = Frame(root)
saveFrame.grid(row=1, column=0)
saveButton = Button(saveFrame, text='save characteristic', command=save)
saveButton.grid(row=0, column=0)
loadButton = Button(saveFrame, text='load stat', command=loadFile)
loadButton.grid(row=0, column=1)
createButton = Button(saveFrame, text='create profil', command=createProfil)
createButton.grid(row=0, column=2)

pseudoLabel = Label(statsFrame, text='pseudo : ')
pseudoLabel.grid(row=0, column=0)
pseudoEntry = Entry(statsFrame, text='pseudo')
pseudoEntry.grid(row=0, column=1)
pseudoEntry.insert(0, data['pseudo'])

cpLabel = Label(statsFrame, text='cp : ' + str(data['cp']))
cpLabel.grid(row=1, column=0)

hpLabel = Label(statsFrame, text='hp : ' + str(data['maxHp']))
hpLabel.grid(row=2, column=0)
moreHpButton = Button(statsFrame, text='+', state=DISABLED, command=lambda: updateStat('maxHp', values['maxHp']))
moreHpButton.grid(row=2, column=1)
lessHpButton = Button(statsFrame, text='-', state=DISABLED, command=lambda: updateStat('maxHp', -values['maxHp']))
lessHpButton.grid(row=2, column=2)

mpLabel = Label(statsFrame, text='mp : ' + str(data['maxMp']))
mpLabel.grid(row=3, column=0)
moreMpButton = Button(statsFrame, text='+', state=DISABLED, command=lambda: updateStat('maxMp', values['maxMp']))
moreMpButton.grid(row=3, column=1)
lessMpButton = Button(statsFrame, text='-', state=DISABLED, command=lambda: updateStat('maxMp', -values['maxMp']))
lessMpButton.grid(row=3, column=2)

tpLabel = Label(statsFrame, text='tp : ' + str(data['maxTp']))
tpLabel.grid(row=4, column=0)
moreTpButton = Button(statsFrame, text='+', state=DISABLED, command=lambda: updateStat('maxTp', values['maxTp']))
moreTpButton.grid(row=4, column=1)
lessTpButton = Button(statsFrame, text='-', state=DISABLED, command=lambda: updateStat('maxTp', -values['maxTp']))
lessTpButton.grid(row=4, column=2)

root.mainloop()
