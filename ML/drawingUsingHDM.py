import cv2 as cv
import numpy as np
import mediapipe as mp
from handDetectionModule import HandDetector
from countFingers import getRaisedFingersList, getPosOfPoints
from resizeImage import rescaleFrame
from os import system, listdir

frameWidth = 1080
frameHeight = 600
imgList = []
penColor = (0, 0, 255)
penThickness = 20
eraserThickness = 35
lastX, lastY = 0, 0

imgCanvas = np.zeros((frameHeight, frameWidth, 3), np.uint8)


def getAllImages():
    folderPath = 'HandDrawing'
    imgURIList = listdir(folderPath)

    for imgURI in imgURIList:
        img = cv.imread(f'{folderPath}/{imgURI}')
        imgList.append(img)


def fingersListFound(raisedList):
    index, middle = raisedList[1:3]
    if index and middle and raisedList[1:].count(1) < 3:
        return selectMode
    elif index and not middle:
        return drawMode
    return None


def selectMode(posLms, img):
    global penColor, lastX, lastY
    lastX, lastY = 0, 0
    point8 = getPosOfPoints(posLms, 0, 8)
    point12 = getPosOfPoints(posLms, 0, 12)
    if (point8[1] not in range(-50, 125)) or (point12[1] not in range(-50, 125)):
        return
    if(point8[0] < 350) or (point12[0] < 350):
        # print('Red')
        penColor = (0, 0, 255)

        return imgList[0]
    elif (point8[0] < 500) or (point12[0] < 500):
        penColor = (255, 0, 0)
        # print('Blue')

        return imgList[1]
    elif (point8[0] < 800) or (point12[0] < 800):
        penColor = (0, 255, 255)
        # print('Yellow')

        return imgList[2]
    elif (point8[0] < 1080) or (point12[0] < 1080):
        penColor = (0, 0, 0)
        # print('Eraser')

        return imgList[3]


def drawMode(posLms, img):
    global lastX, lastY
    point8 = getPosOfPoints(posLms, 0, 8)
    if lastX == 0:
        lastX = point8[0]
    if lastY == 0:
        lastY = point8[1]
    t = penThickness
    if(penColor == (0, 0, 0)):
        t = eraserThickness
    cv.circle(img, point8, t//2, penColor, -1)
    cv.line(imgCanvas, (lastX, lastY), point8, penColor, t)
    lastX, lastY = point8
    return None


def main():
    global lastX, lastY
    system('cls')
    maskImg = imgList[0]
    while True:
        b, img = video.read()
        if not b:
            break
        img = cv.flip(img, 1)
        img = rescaleFrame(img, dWidth=frameWidth, dHeight=frameHeight)
        posLms, _ = detector.findFingerPositions(img, handNo=0)
        if posLms:
            raisedList = getRaisedFingersList(posLms, 0)
            command = fingersListFound(raisedList)
            if command:
                value = command(posLms, img)
                if value is not None:
                    maskImg = value
                else:
                    lastX, lastY = 0, 0
        else:
            lastX, lastY = 0, 0
        img[0:125, 0: 1080] = maskImg
        # drawing = cv.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
        drawing = addTwoImages(img, imgCanvas)
        cv.imshow('Drawing', drawing)
        # cv.imshow('Canvas', imgCanvas)
        if cv.waitKey(1) == ord('d'):
            break
    video.release()
    cv.destroyAllWindows()


def addTwoImages(img, imgCanvas):
    imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 0, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, imgCanvas)
    return img


if __name__ == '__main__':
    video = cv.VideoCapture(0)
    detector = HandDetector(maxHands=1,
                            detectionConfidence=0.75, trackConfidence=0.8)
    getAllImages()
    main()
