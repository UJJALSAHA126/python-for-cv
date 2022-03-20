#  CREATING A TIC-TAC-TOE GAME
from os import system
from random import randint
# from ChangeColors import ColorClass as cc

points = [[" ", " ", " "],
          [" ", " ", " "],
          [" ", " ", " "]]

values = ['X', '0']
players = ['X', '0']


def printPlayers(value):
    if(value == values[0]):
        print(f'\033[1;{31}m', end='')
        # cc.changeColorAfter(31)
    elif(value == values[1]):
        print(f'\033[1;{36}m', end='')
        # cc.changeColorAfter(36)
    else:
        print(f'\033[1;{30}m', end='')
        # cc.changeColorAfter(30)
    print(value, end='')
    print(f'\033[1;{33}m', end='')
    # cc.changeColorAfter(33)


def printPoints():
    # system('COLOR 9')
    print('')
    printPlayers(points[0][0])
    print(' | ', end='')
    printPlayers(points[0][1])
    print(' | ', end='')
    printPlayers(points[0][2])
    print('\n--+---+--')

    printPlayers(points[1][0])
    print(' | ', end='')
    printPlayers(points[1][1])
    print(' | ', end='')
    printPlayers(points[1][2])
    print('\n--+---+--')

    printPlayers(points[2][0])
    print(' | ', end='')
    printPlayers(points[2][1])
    print(' | ', end='')
    printPlayers(points[2][2])
    print('')

    # print(f'\n{printPlayers(0,0)} | {points[0][1]} | {points[0][2]}')
    # print('--+---+--')
    # print(f'{points[1][0]} | {points[1][1]} | {points[1][2]}')
    # print('--+---+--')
    # print(f'{points[2][0]} | {points[2][1]} | {points[2][2]}')


def isFinished():
    for val in points:
        if val[0] != ' ' and val[0] == val[1] and val[1] == val[2]:
            return True, val[0]

    for i in range(0, 3):
        if(points[0][i] != ' ' and points[0][i] == points[1][i] and points[1][i] == points[2][i]):
            return True, points[0][i]

    if(points[0][0] != ' ' and points[0][0] == points[1][1] and points[1][1] == points[2][2]):
        return True, points[0][0]

    if(points[0][2] != ' ' and points[0][2] == points[1][1] and points[1][1] == points[2][0]):
        return True, points[0][2]

    for val in points:
        for v in val:
            if v.isnumeric() and int(v) > 0:
                return False, 'Free'

    return False, 'Filled'


def putValue(num, p):
    for i, val in enumerate(points):
        for j, v in enumerate(val):
            if str(v) == str(num):
                points[i][j] = p
                return True
    return False


def startGame():
    p = randint(0, 1)
    while True:
        printPoints()
        r, v = isFinished()
        if(r):
            system('cls')
            printPoints()
            printPlayers(v)
            print(' Has Won The Game 🎇✨🎉🎊🎈🎆')
            if(input('Enter "S" To Restart :: ').upper() == 'S'):
                main()
                return
            return
        if(v == 'Filled'):
            system('cls')
            printPoints()
            print('\nThe Game Is Finished. Please Restart The Game. 😊😊😊')
            if(input('Enter "S" To Restart :: ').upper() == 'S'):
                main()
                return
            return

        print('\n'+players[p]+'\'s Turn :')
        while True:
            _p = str(input('Enter The Position :: '))
            if(not _p.isnumeric()):
                try:
                    if(int(_p) == -1):
                        return
                except:
                    pass
                print('Please Choose A Value Between 0 to 9 !!! 👿👿👿')
                continue
            if(int(_p) >= 0 and int(_p) <= 9):
                if(putValue(_p, players[p])):
                    p = p ^ 1
                    break
                elif(int(_p) == -1):
                    exit(0)
                else:
                    print('This Place Is Not Avilable 🤐🤐😐😐😑😑')
            else:
                print('Please Choose A Value Between 0 to 9 !!! 😒😒😒')


def main():
    system('cls')
    num = 1
    for i in range(0, 3):
        for j in range(0, 3):
            points[i][j] = str(num)
            num += 1
    startGame()


if __name__ == '__main__':
    main()


# print('X | 0 | X')
# print('--+---+--')
# print('0 | 0 | X')
# print('--+---+--')
# print('X | 0 | X')
