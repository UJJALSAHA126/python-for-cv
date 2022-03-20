from os import system
from typing import List
import cv2 as cv
import mediapipe as mp
from getIpWebCam import getUrl
from resizeImage import rescaleFrame
from handDetectionModule import HandDetector


class MyFaceDetector():
    def __init__(self, min_detection_confidence=0.5, model_selection=0):
        self.__mim_dect_con = min_detection_confidence
        self.__model_delection = model_selection
        self.__myFaceDect = mp.solutions.mediapipe.python.solutions.face_detection
        self.__faceDetection = self.__myFaceDect.FaceDetection(self.__mim_dect_con,
                                                               self.__model_delection)

    def detectFaces(self, img, draw=True, t=4, rt=1,
                    cColor=(255, 0, 255), rColor=(0, 255, 0),
                    lockTarget=False):
        imgRBG = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        allBboxx = []
        allFacesDetection = []
        results = self.__faceDetection.process(imgRBG)
        if results.detections:
            ih, iw = img.shape[:2]
            for id, face in enumerate(results.detections):
                score = int(face.score[0]*100)
                bboxC = face.location_data.relative_bounding_box
                allFacesDetection.append([id, face])
                bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih),\
                    int((bboxC.width) * iw), int((bboxC.height)*ih)
                allBboxx.append([id, bbox])
                if draw:
                    cv.putText(img, f'Score :{score}%', (bbox[0], bbox[1]-10),
                               cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                    self.__fancyDraw(img, bbox, t, rt, cColor,
                                     rColor, lockTarget)
        return allBboxx, allFacesDetection

    def __fancyDraw(self, img, bbox, t=4, rt=1,
                    cColor=(255, 0, 255), rColor=(0, 255, 0),
                    lockTarget=False):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        l = int(w/5)

        # Locking Target
        if lockTarget:
            cv.line(img, (x, y), (x1, y1), (0, 0, 255), t)
            cv.line(img, (x1, y), (x, y1), (0, 0, 255), t)

        # Total Rectangle
        cv.rectangle(img, bbox, rColor, rt)
        # Top Left
        cv.line(img, (x, y), (x+l, y), cColor, t)
        cv.line(img, (x, y), (x, y+l), cColor, t)
        # Top Right
        cv.line(img, (x1, y), (x1-l, y), cColor, t)
        cv.line(img, (x1, y), (x1, y+l), cColor, t)

        # Bottom Left
        cv.line(img, (x, y1), (x+l, y1), cColor, t)
        cv.line(img, (x, y1), (x, y1-l), cColor, t)
        # Bottom Right
        cv.line(img, (x1, y1), (x1-l, y1), cColor, t)
        cv.line(img, (x1, y1), (x1, y1-l), cColor, t)


def main():
    system('cls')
    detector = MyFaceDetector()
    hDetector = HandDetector()
    while True:
        success, img = video.read()
        if(not success):
            return
        img = cv.flip(img, 1)
        img = rescaleFrame(img, dWidth=900, dHeight=500)
        allBboxs, faceDetections = detector.detectFaces(img, lockTarget=True)
        hDetector.findFingerPositions(img)
        # if(len(faceDetections) > 0):
        # for id, face in faceDetections:
        #     mpDraw.draw_detection(img, face)

        cv.imshow('Face Detection', img)
        key = cv.waitKey(1)
        if(key == ord('d')):
            break
    video.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
    url = getUrl()
    video = cv.VideoCapture(0)
    if(url != ''):
        video.open(url)
    main()
