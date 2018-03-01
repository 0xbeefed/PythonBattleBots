from tkinter import *
from tkinter import filedialog

filename = ''
data = {'hp' : '-', 'mp' : '-', 'tp' : '-', 'cp' : '-'}
values = {'hp' : 20, 'mp' : 1, 'tp' : 1}

def loadFile():
    global filename, data
    filename = filedialog.askopenfilename(parent = root)
    file = open(filename, 'r')
    data = eval(file.read())
    file.close()

    moreHpButton.config(state = NORMAL)
    lessHpButton.config(state = NORMAL)
    
    moreMpButton.config(state = NORMAL)
    lessMpButton.config(state = NORMAL)
    
    moreTpButton.config(state = NORMAL)
    lessTpButton.config(state = NORMAL)

    cpLabel.config(text = 'cp : ' + str(data['cp']))
    hpLabel.config(text = 'hp : ' + str(data['hp']))
    mpLabel.config(text = 'mp : ' + str(data['mp']))
    tpLabel.config(text = 'tp : ' + str(data['tp']))

def updateStat(stat, value):
    global data
    if data['cp'] - value//values[stat] >= 0 and data[stat] + value > 0:
        data[stat] += value
        data['cp'] -= value//values[stat]
        cpLabel.config(text = 'cp : ' + str(data['cp']))
        hpLabel.config(text = 'hp : ' + str(data['hp']))
        mpLabel.config(text = 'mp : ' + str(data['mp']))
        tpLabel.config(text = 'tp : ' + str(data['tp']))
        
def save():
    global filename, data
    file = open(filename, 'w')
    file.write(str(data))
    file.close()
    data = {'hp' : '-', 'mp' : '-', 'tp' : '-', 'cp' : '-'}
    cpLabel.config(text = 'cp : ' + str(data['cp']))
    hpLabel.config(text = 'hp : ' + str(data['hp']))
    mpLabel.config(text = 'mp : ' + str(data['mp']))
    tpLabel.config(text = 'tp : ' + str(data['tp']))
    
    moreHpButton.config(state = DISABLED)
    lessHpButton.config(state = DISABLED)
    
    moreMpButton.config(state = DISABLED)
    lessMpButton.config(state = DISABLED)
    
    moreTpButton.config(state = DISABLED)
    lessTpButton.config(state = DISABLED)
    
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

cpLabel = Label(statsLabel, text = 'cp : ' + str(data['cp']))
cpLabel.grid(row = 0, column = 0)

hpLabel = Label(statsLabel, text = 'hp : ' + str(data['hp']))
hpLabel.grid(row = 1, column = 0)
moreHpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('hp', values['hp']))
moreHpButton.grid(row = 1, column = 1)
lessHpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('hp', -values['hp']))
lessHpButton.grid(row = 1, column = 2)

mpLabel = Label(statsLabel, text = 'mp : ' + str(data['mp']))
mpLabel.grid(row = 2, column = 0)
moreMpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('mp', values['mp']))
moreMpButton.grid(row = 2, column = 1)
lessMpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('mp', -values['mp']))
lessMpButton.grid(row = 2, column = 2)

tpLabel = Label(statsLabel, text = 'tp : ' + str(data['tp']))
tpLabel.grid(row = 3, column = 0)
moreTpButton = Button(statsLabel, text = '+', state = DISABLED, command = lambda : updateStat('tp', values['tp']))
moreTpButton.grid(row = 3, column = 1)
lessTpButton = Button(statsLabel, text = '-', state = DISABLED, command = lambda : updateStat('tp', -values['tp']))
lessTpButton.grid(row = 3, column = 2)

root.mainloop()
