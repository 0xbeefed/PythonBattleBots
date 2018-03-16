import importlib

NUMBER_OF_TURN = 4

user1 = importlib.import_module('ia1')
user2 = importlib.import_module('ia2')

fight = []

print('coord', user1.libtoast.actions)

def checkAction(action): #
    return True

for turn in range(NUMBER_OF_TURN):
    turnInProgress = []
    turnInProgress = [['Turn', turn]]
    turnInProgress.append(['user : user1'])
    user1.main()
    #print('coord', user1.libtoast.actions)
    for action in user1.libtoast.actions:
        if checkAction(action):
            turnInProgress.append(action)
        else:
            print('error in this action')

    user1.libtoast.actions = []
    turnInProgress.append(['user : user2'])
    user2.main()
    #print('coord', user1.libtoast.actions)
    for action in user2.libtoast.actions:
        if checkAction(action):
            turnInProgress.append(action)
        else:
            print('error in this action')
            
    fight.append(turnInProgress)
    user2.libtoast.actions = []
    

print('Complete fight :')
for turn in fight:
    print(turn)
