import random

for i in range(8):
    ran = random.randrange(-8, 8, 1)
    print(ran if ran < 0 else ' ' + str(ran), end='')
    print(',' if i != 7 else '', end='')