import pyautogui
from PIL import Image, ImageGrab
import time
from numpy import asarray

dinoColor = 0
totalScreenShots = 0
start = 0
end = 0


def hit(key):
    pyautogui.keyDown(key)


def getDinoColor(data):
    global dinoColor
    for i in range(95, 105):
        for j in range(450, 460):
            if dinoColor != data[i, j]:
                dinoColor = data[i, j]


def draw():
    image = takeScreenSot()
    data = image.load()
    for i in range(250, 275):
        for j in range(450, 470):
            data[i, j] = 0
    image.show()


def isTreeNearby(data):
    for i in range(280, 300):
        for j in range(450, 470):
            if (data[i, j] == dinoColor) or data[i, j] == 0:
                return True

    return False


def takeScreenSot() -> Image:
    global totalScreenShots
    try:
        image = ImageGrab.grab().convert('L')
        totalScreenShots += 1
    except:
        exit()
    return image


def main():
    print('Please Start Your Game !!')
    time.sleep(2)
    # draw()
    # exit()
    global start
    start = time.time()
    image = takeScreenSot()
    data = image.load()
    getDinoColor(data)
    time.sleep(.5)
    hit('up')
    while(True):
        image = takeScreenSot()
        data = image.load()
        if isTreeNearby(data):
            hit('up')


if __name__ == '__main__':
    try:
        main()
    except:
        end = time.time()
        print('Total ScreenShots Taken =', totalScreenShots)
        print('Speed =', (totalScreenShots//(end-start)))
        exit()
