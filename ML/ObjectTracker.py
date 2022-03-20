import cv2 as cv


video = cv.VideoCapture(0)
# tracker = cv.legacy.TrackerMOSSE_create()
tracker = cv.legacy.TrackerCSRT_create()


s, img = video.read()
img = cv.flip(img, 1)
bbox = cv.selectROI("Tracking", img, False)
tracker.init(img, bbox)

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    # cv.putText(img, "Tracking", (75, 75), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3, 1)

def main():
    while True:
        timer = cv.getTickCount()
        success, img = video.read()
        if not success:
            print("Some Error Occured !!🤖🤖🤖")
            break
        img = cv.flip(img, 1)

        s, bbox = tracker.update(img)
        
        if s:
            drawBox(img,bbox)
            cv.putText(img, "Target Locked", (10, 20),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, color=(0, 255, 0), thickness=2)
        else:
            cv.putText(img, "Target Lost", (10, 20),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, color=(0, 0, 255), thickness=2)


        # Adding FPS Counter
        fps = cv.getTickFrequency()/(cv.getTickCount()-timer)
        cv.putText(img, str(int(fps))+" FPS", (10, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, color=(0, 0, 255), thickness=2)
        
        cv.imshow("Tracking", img)
        if(cv.waitKey(1) == ord('d')):
            break


if __name__ == "__main__":
    main()
