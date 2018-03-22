action = "[MARK] [[0, 0], [1, 1]] yellow".split()

print(action) #['[MARK]', '[[0,', '0]]', 'yellow']

if action[0] == '[MARK]':
    color = action[-1]
    exec('tmp = ' + ''.join(action[1:-1]))
    print(color)
    print(tmp)
    print(type(tmp))

for cell in tmp:
    x = int(cell[0])
    y = int(cell[1])
    print(x,y)
