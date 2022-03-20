import cv2 as cv
import mediapipe as mp
from math import hypot


class HandDetector():
    fingerTips = {4, 8, 12, 16, 20}

    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        self.__mode = mode
        self.__maxHands = maxHands
        self.__detectionConfidence = detectionConfidence
        self.__trackConfidence = trackConfidence
        self.__mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.__hands = self.__mpHands.Hands(
            self.__mode, self.__maxHands, 1, self.__detectionConfidence, self.__trackConfidence)
        self.__mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

    def findFingerPositions(self, img, fingerPoints=fingerTips,
                            handNo=-1, draw=True, color=(255, 0, 0),
                            drawFinterTips=False):
        self.__results = self.__hands.process(
            cv.cvtColor(img, cv.COLOR_BGR2RGB))

        positionalLandmark = []

        if self.__results.multi_hand_landmarks:
            handLms = self.__results.multi_hand_landmarks
            for hNo, handLm in enumerate(handLms):
                if(handNo != -1 and handNo != hNo):
                    continue
                if draw:
                    self.__mpDraw.draw_landmarks(img, handLm,
                                                 self.__mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(handLm.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    positionalLandmark.append([hNo, [id, cx, cy]])
                    if drawFinterTips and (id in fingerPoints):
                        cv.circle(img, (cx, cy), 10, color, cv.FILLED)
            return positionalLandmark, handLms

        return None, None

    def getRaisedFingersList(self, posLms, handNo=-1):
        raisedFingers = []
        fingerTips = [4, 8, 12, 16, 20]
        x = len(posLms)//21
        for hNo in range(x):
            # 0 - Right Hand, 1 - Left Hand
            if(handNo != -1 and handNo != hNo):
                continue
            thisHand = self.detectLeftOrRightHand(posLms, hNo)
            for pos in fingerTips:
                if(pos == 4):
                    point4 = self.getPosOfPoints(posLms, hNo, 4)
                    point5 = self.getPosOfPoints(posLms, hNo, 5)
                    if(point4[0] >= point5[0]):
                        raisedFingers.append(thisHand)
                    else:
                        raisedFingers.append(thisHand ^ 1)
                else:
                    x = self.getPosOfPoints(posLms, hNo, pos)
                    y = self.getPosOfPoints(posLms, hNo, pos-2)
                    if(x[1] >= y[1]):
                        raisedFingers.append(0)
                    else:
                        raisedFingers.append(1)
        return raisedFingers

    def getPosOfPoints(self, posLms, hNo, lmNo):
        if lmNo > 20 or lmNo < 0:
            raise ValueError()
        for n, lm in posLms:
            if n != hNo or lm[0] != lmNo:
                continue
            return lm[1], lm[2]

#   0 - Right Hand, 1 - Left Hand
    def detectLeftOrRightHand(self, posLms, hNo):
        thisHand = 0
        point0 = self.getPosOfPoints(posLms, hNo, 0)
        point5 = self.getPosOfPoints(posLms, hNo, 5)
        point17 = self.getPosOfPoints(posLms, hNo, 17)

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

    def getDistanceToTwoPoints(self, posLms, hNo1=0, lmNo1=0, hNo2=0, lmNo2=0):
        point1 = self.getPosOfPoints(posLms, hNo1, lmNo1)
        point2 = self.getPosOfPoints(posLms, hNo2, lmNo2)

        return hypot(point1[0]-point2[0], point1[1]-point2[1])


if __name__ == '__main__':
    mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
    mpHands = mp.solutions.mediapipe.python.solutions.hands
    hdm = HandDetector()
    video = cv.VideoCapture(0)
    while True:
        b, img = video.read()
        _, lmList = hdm.findFingerPositions(img, draw=False)
        if lmList is not None:
            for lm in lmList:
                mpDraw.draw_landmarks(img, lm, mpHands.HAND_CONNECTIONS)
        cv.imshow('Video', img)
        # if(len(lmList) > 0):
        #     print(lmList[4])
        if cv.waitKey(1) == ord('d'):
            break
