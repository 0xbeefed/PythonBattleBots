global actions

actions = []

def attack(x):
    actions.append(['attack',x])
    return 0

def move(x,y):
    actions.append(['move', x, y])
    return 0
