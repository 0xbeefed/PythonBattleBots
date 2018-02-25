import sys
import os
import time
PATH = os.getcwd().replace('\\', '/') + '/' + sys.argv[1]

def toast(text):
    global PATH

    # Request info
    with open(PATH + 'actionX.dat', 'r+') as file:
        file.seek(0)
        file.write(text)
    os.rename(PATH + 'actionX.dat', PATH + 'actionO.dat')

    # Wait for response
    while os.path.isfile(PATH + 'actionO.dat'):
        a=0

    # Read info
    data = ''
    while data == '':
        try:
            with open(PATH + 'actionX.dat', 'r+') as file:
                data = file.read()
                file.seek(0)
                file.truncate()
        except:
            continue
        
    return data
