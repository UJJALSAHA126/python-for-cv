import cv2 as cv
import handDetectionModule as hdmodule
import math
import SystemVolumeModule as svm

frameWidth = 620
frameHeight = 480

hdm = hdmodule.HandDetector()
video = cv.VideoCapture(0)
video.set(3, frameWidth)
video.set(4, frameHeight)

sysVolMod = svm.SystemVolumeSetter()


def landMarkFound(lmList, drawnImg):
    if(len(lmList) > 0):
        cx, cy = 0, 0
        for lm in lmList:
            if(lm[0] != 0):
                return
            if(lm[1][0] in {4, 8}):
                cx, cy = lm[1][1:]
                cv.circle(drawnImg, (cx, cy), 10,
                          (0, 0, 255), cv.FILLED)
                if(lm[1][0] == 4):
                    thumbX, thumbY = cx, cy
                else:
                    indexX, indexY = cx, cy
        midColor = (0, 255, 0)
        midX, midY = int((thumbX+indexX)/2), int((thumbY+indexY)/2)

        length = float(math.hypot(thumbX-indexX, thumbY-indexY))
        sysVolMod.setSystemVolume(length, volumeRange=[30, 160])

        if(length >= 160):
            midColor = (0, 0, 255)
        elif(length >= 80):
            midColor = (0, 255, 255)
        elif (length <= 30):
            midColor = (255, 0, 0)

        cv.line(drawnImg, (thumbX, thumbY), (indexX, indexY), (0, 255, 0), 3)
        cv.circle(drawnImg, (midX, midY), 10, midColor, -1)


def main():
    while True:
        b, img = video.read()
        cv.cvtColor(img, cv.COLOR_BGR2RGB)
        lmList, _ = hdm.findFingerPositions(img, fingerPoints={
            4, 8}, draw=True, handNo=0, color=(0, 0, 255))

        # thumbX, thumbY, indexX, indexY = 0, 0, 0, 0
        if lmList:
            landMarkFound(lmList, img)
        cv.imshow('Video', img)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
