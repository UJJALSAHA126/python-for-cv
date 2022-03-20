import cv2 as cv
import numpy as np

bHeight = 40

cHeight, cWidth = 28*20, 28*20
cColor = (255, 255, 255)

penSize = 10
penColor = (0, 0, 0)

startX, startY = 0, 0
pressed = False
continueLoop = True

# Handles The Mouse Click Enents #


def __mouseEvent__(event, x, y, _, __):
    global startX, startY, pressed, continueLoop
    if(event == cv.EVENT_LBUTTONDOWN):
        # print("Down", x, y)

        if(35 <= x <= 123 and cHeight <= y <= cHeight+bHeight):
            # print('Clear Clicked')
            canvas[:, :, :] = (255, 255, 255)
            return
        elif(445 <= x <= 530 and cHeight <= y <= cHeight+bHeight):
            continueLoop = False
            # print('Done Clicked')
            return

        startX, startY = x, y
        pressed = True

    elif event == cv.EVENT_MOUSEMOVE and pressed:
        # print(x, y)
        cv.line(canvas, (startX, startY), (x, y), penColor, penSize)
        startX, startY = x, y

    elif event == cv.EVENT_LBUTTONUP:
        # print("Up")
        pressed = False


def getDrawing(dimensions=(280, 280)):
    global canvas
    canvas = np.full((cHeight, cWidth, 3), cColor, np.uint8)
    bottom = np.full((bHeight, cWidth, 3), (255, 0, 0), np.uint8)
    img = np.full((cHeight+bHeight, cWidth, 3), cColor, np.uint8)

    cv.rectangle
    cv.rectangle(bottom, (35, 0), (123, bHeight), (0, 0, 0), -1)
    cv.rectangle(bottom, (445, 0), (530, bHeight), (0, 0, 0), -1)

    cv.putText(bottom, "Clear", (40, bHeight-10),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv.putText(bottom, "Done", (450, bHeight-10),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    img[:cHeight, :cWidth] = canvas
    img[cHeight:] = bottom
    cv.imshow("Canvas", img)

    cv.setMouseCallback("Canvas", __mouseEvent__)

    while True and continueLoop:
        img[:cHeight, :cWidth] = canvas
        img[cHeight:] = bottom
        cv.imshow("Canvas", img)

        if cv.waitKey(1) == ord('d'):
            break

    cv.destroyAllWindows()
    canvas = cv.resize(canvas, dimensions, interpolation=cv.INTER_AREA)
    return canvas


def main():
    canvas = getDrawing()
    cv.imshow("Drawing", canvas)
    cv.waitKey(0)


if __name__ == '__main__':
    main()
