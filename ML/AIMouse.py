import cv2 as cv
import mediapipe as mp
from handDetectionModule import HandDetector
from resizeImage import rescaleFrame
import numpy as np
import pyautogui
import os
import math

myScreenSize = (1366, 768)
myScreenRatio = (683, 384, 2)

pointStart = [0, 0]
pointEnd = [0, 0]

fWidth = 1080
fHeight = 650


def getRectangleSize():
    pointStart[0] = 80
    pointStart[1] = 10
    pointEnd[0] = fWidth-80

    width = int(pointEnd[0]-pointStart[0])
    height = int(width*myScreenRatio[1]/myScreenRatio[0])

    pointEnd[1] = pointStart[1]+height


def posLmsFound(posLms):
    raisedList = detector.getRaisedFingersList(posLms, 0)
    if raisedList[1] and raisedList[2] and raisedList[3:].count(1) <= 0:
        point8 = detector.getPosOfPoints(posLms, 0, 8)
        point7 = detector.getPosOfPoints(posLms, 0, 7)
        point12 = detector.getPosOfPoints(posLms, 0, 12)
        point11 = detector.getPosOfPoints(posLms, 0, 11)

        dis1 = math.hypot(point8[0]-point12[0], point8[1]-point12[1])
        dis2 = math.hypot(point7[0]-point11[0], point7[1]-point11[1])

        if dis2-5 <= dis1 <= dis2+5:
            # print('click')
            mouseClick()
    elif raisedList[1] and raisedList[2:].count(1) <= 1:

        point = [0, 0]
        point8 = detector.getPosOfPoints(posLms, 0, 8)
        # width = pointEnd[0] - pointStart[0]
        # height = pointEnd[1] - pointStart[1]

        point[0] = np.interp(
            point8[0], (pointStart[0], pointEnd[0]), (0, myScreenSize[0]))
        point[1] = np.interp(
            point8[1], (pointStart[1], pointEnd[1]), (0, myScreenSize[1]))

        moveMouse(point)


def mouseClick():
    pyautogui.click()


def moveMouse(point):
    # print('Moving', point)
    currPos = pyautogui.mouseinfo.position()
    pyautogui.move(point[0] - currPos[0],  point[1]-currPos[1])


def main():
    os.system('cls')
    while True:
        success, img = video.read()
        if not success:
            break
        img = cv.flip(img, 1)
        img = rescaleFrame(img, dWidth=fWidth, dHeight=fHeight)
        posLms, _ = detector.findFingerPositions(
            img, draw=True, handNo=0)
        if posLms:
            posLmsFound(posLms)

        cv.rectangle(img, pointStart, pointEnd, (0,  255, 0), 3)
        cv.imshow('AI Mouse', img)
        if cv.waitKey(1) == ord('d'):
            break
    video.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    getRectangleSize()
    pyautogui.FAILSAFE = False
    video = cv.VideoCapture(0)
    detector = HandDetector(maxHands=1, detectionConfidence=0.3)
    mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
    main()
