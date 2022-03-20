import cv2 as cv


def rescaleFrame(frame, scale=0.75, dWidth=None, dHeight=None):
    if(dWidth is None):
        width = int(frame.shape[1]*scale)
    else:
        width = dWidth
    if(dHeight is None):
        height = int(frame.shape[0]*scale)
    else:
        height = dHeight
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def changeRes(capture, width, height):
    # For Live Videos
    capture.set(3, width)
    capture.set(4, height)


def main():
    #  Reading Image Data
    img = cv.imread('Photos/cat_large.jpg')
    img_resize = rescaleFrame(img, 0.2)
    cv.imshow('Cat', img_resize)
    cv.waitKey(0)

    #  Reading Video Data
    # capture=cv.VideoCapture('Videos/dog.mp4')
    # while True:
    #     isTrue,frame= capture.read()
    #     if not isTrue:
    #         break
    #     frame_resized=rescaleFrame(frame)
    #     cv.imshow('Video',frame)
    #     cv.imshow('Resized Video',frame_resized)
    #     if cv.waitKey(20) & 0xFF==ord('d'):
    #         break
    # capture.release()
    # cv.destroyAllWindows()
    pass


if __name__ == '__main__':
    main()
