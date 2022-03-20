from os import system
import cv2 as cv
import mediapipe as mp
import handDetectionModule as hdm
from resizeImage import rescaleFrame


def getRaisedFingersList(posLms, handNo=-1):
    raisedFingers = []
    fingerTips = [4, 8, 12, 16, 20]
    x = len(posLms)//21
    for hNo in range(x):
        # 0 - Right Hand, 1 - Left Hand
        if(handNo != -1 and handNo != hNo):
            continue
        thisHand = detectLeftOrRightHand(posLms, hNo)
        for pos in fingerTips:
            if(pos == 4):
                point4 = getPosOfPoints(posLms, hNo, 4)
                point5 = getPosOfPoints(posLms, hNo, 5)
                if(point4[0] >= point5[0]):
                    raisedFingers.append(thisHand)
                else:
                    raisedFingers.append(thisHand ^ 1)
            else:
                x = getPosOfPoints(posLms, hNo, pos)
                y = getPosOfPoints(posLms, hNo, pos-2)
                if(x[1] >= y[1]):
                    raisedFingers.append(0)
                else:
                    raisedFingers.append(1)
    return raisedFingers


def getProperList(posLms):
    x = 0
    cleanList = []
    temp = []
    for hNo, lm in posLms:
        if(hNo == x):
            temp.append(lm)
        else:
            cleanList.append(temp)
            temp.clear()
            temp.append(lm)
            x = hNo
    if len(temp) > 0:
        cleanList.append(temp)
    return cleanList


def detectLeftOrRightHand(posLms, hNo):
    thisHand = 0
    point0 = getPosOfPoints(posLms, hNo, 0)
    point5 = getPosOfPoints(posLms, hNo, 5)
    point17 = getPosOfPoints(posLms, hNo, 17)

    if point5[0] < point17[0]:
        if(point0[1] > point5[1]):
            thisHand = 0
        else:
            thisHand = 1
    else:
        if(point0[1] > point5[1]):
            thisHand = 1
        else:
            thisHand = 0
    return thisHand


def getPosOfPoints(posLms, hNo, lmNo):
    if lmNo > 20 or lmNo < 0:
        raise ValueError()
    for n, lm in posLms:
        if n != hNo or lm[0] != lmNo:
            continue
        return lm[1], lm[2]


def main():
    system('cls')
    while True:
        b, img = video.read()
        if not b:
            break
        img = cv.flip(img, 1)
        img = rescaleFrame(img, dWidth=800, dHeight=500)
        posLms, allLms = detector.findFingerPositions(img)
        if posLms:
            finList = getRaisedFingersList(posLms)
            c = finList.count(1)
            # cv.rectangle(img, (50, 50), (160, 200), (0, 255, 255), -1)
            cv.putText(img, str(c), (50, 200),
                       cv.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 25)
        cv.imshow('Finger Counter', img)
        if(cv.waitKey(1) == ord('d')):
            break
    video.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    video = cv.VideoCapture(0)

    detector = hdm.HandDetector()

    main()
