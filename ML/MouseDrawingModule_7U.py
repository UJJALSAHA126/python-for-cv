from threading import Thread
import cv2 as cv
import numpy as np
from tkinter import *
from tkinter import colorchooser


class DrawUsingMouse:

    def __init__(self, penSize=7, penColor=(0, 0, 0)):
        self.__bHeight = 40
        self.__cHeight, self.__cWidth = 28*20, 28*20
        self.__cColor = (255, 255, 255)

        self.penSize = penSize
        self.penColor = penColor

        self.hexColor = self.__bgrToHex__(self.penColor)

        self.__startX, self.__startY = 0, 0
        self.__pressed = False
        self.__continueLoop = True

    def __bgrToHex__(self, bgr):
        return f'#{int(bgr[2]):02x}{int(bgr[1]):02x}{int(bgr[0]):02x}'

    def __mouseEvent__(self, event, x, y, _, __):
        if(event == cv.EVENT_LBUTTONDOWN):

            if(35 <= x <= 123 and self.__cHeight <= y <= self.__cHeight+self.__bHeight):
                self.canvas[:, :, :] = (255, 255, 255)
                return
            elif(445 <= x <= 530 and self.__cHeight <= y <= self.__cHeight+self.__bHeight):
                self.__continueLoop = False
                return

            self.__startX, self.__startY = x, y
            self.__pressed = True

        elif event == cv.EVENT_MOUSEMOVE and self.__pressed:
            cv.line(self.canvas, (self.__startX, self.__startY),
                    (x, y), self.penColor, self.penSize)
            self.__startX, self.__startY = x, y

        elif event == cv.EVENT_LBUTTONUP:
            self.__pressed = False

    def __startCanvas__(self, dimensions):
        self.canvas = np.full(
            (self.__cHeight, self.__cWidth, 3), self.__cColor, np.uint8)
        bottom = np.full((self.__bHeight, self.__cWidth, 3),
                         (255, 0, 0), np.uint8)
        img = np.full((self.__cHeight+self.__bHeight, self.__cWidth, 3),
                      self.__cColor, np.uint8)

        cv.rectangle
        cv.rectangle(bottom, (35, 0), (123, self.__bHeight), (0, 0, 0), -1)
        cv.rectangle(bottom, (445, 0), (530, self.__bHeight), (0, 0, 0), -1)

        cv.putText(bottom, "Clear", (40, self.__bHeight-10),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv.putText(bottom, "Done", (450, self.__bHeight-10),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        img[:self.__cHeight, :self.__cWidth] = self.canvas
        img[self.__cHeight:] = bottom
        cv.imshow("Canvas", img)

        cv.setMouseCallback("Canvas", self.__mouseEvent__)

        while True and self.__continueLoop:
            img[:self.__cHeight, :self.__cWidth] = self.canvas
            img[self.__cHeight:] = bottom
            cv.imshow("Canvas", img)
            k = cv.waitKey(1)
            if k == ord('d'):
                break

        cv.destroyAllWindows()
        canvas = cv.resize(self.canvas, dimensions,
                           interpolation=cv.INTER_AREA)
        return canvas

    def __chooseColor__(self, event):
        color = colorchooser.askcolor()
        self.penColor = (color[0][2], color[0][1], color[0][0])
        try:
            self.penSize = int(self.x.get())
        except:
            self.x.set(self.penSize)
        self.hexColor = color[1]
        self.colorLabel.config(bg=self.hexColor)

    def __executeParallel__(self):
        self.window = Tk()
        self.window.title("Change Drawing Style")
        self.window.geometry('300x120')
        self.window.config(bg='yellow')
        self.window.resizable(False, False)
        self.__configureAndAddItems__(self.window)
        self.window.mainloop()

    def __doneClicked__(self):
        try:
            self.penSize = int(self.x.get())
        except:
            self.x.set(self.penSize)

    def __closeClicked__(self):
        self.window.destroy()

    def __configureAndAddItems__(self, window):
        label1 = Label(window, text='Pen Color', bg='red', font='arial 15')
        label1.grid(row=0, column=0, pady=5, sticky='w')

        label2 = Label(window, text='Pen Size  ', bg='red', font='arial 15')
        label2.grid(row=1, column=0, sticky='w')

        self.colorLabel = Label(window, text=" ", bg=self.hexColor,
                                font='arial 15', width=100)
        self.colorLabel.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.x = IntVar(value=self.penSize)
        penSizeEntry = Entry(window, textvariable=self.x,
                             width=100, font='arial 15')
        penSizeEntry.grid(row=1, column=1, sticky='w', padx=10)

        doneBtn = Button(window, text="Apply",
                         font="Arial 15 bold", fg='green', bg='gray', command=self.__doneClicked__)
        doneBtn.grid(row=2, column=0,
                     pady=5, padx=10, sticky='e')
        closeBtn = Button(window, text="Close",
                          font="Arial 15 bold", fg='green', bg='gray', command=self.__closeClicked__)
        closeBtn.grid(row=2, column=1,
                      pady=5, padx=10, sticky='w')

        self.colorLabel.bind("<Button-1>", self.__chooseColor__)

    def getDrawing(self, dimensions=(280, 280)):
        # self.window = Tk()
        self.__t1 = Thread(name="Tkinter_Thread",
                           target=self.__executeParallel__)
        self.__t1.start()
        # self.executeParallel()
        return self.__startCanvas__(dimensions)


def main():
    drawer = DrawUsingMouse(penColor=(0, 0, 255))
    canvas = drawer.getDrawing()
    cv.imshow("Drawing", canvas)
    cv.waitKey(0)


if __name__ == '__main__':
    main()
