import numpy as np
import cv2 as cv
from MouseDrawingModule_7U import DrawUsingMouse
import os
import joblib

modelNameToSave = "Digit_Recognizer_Model"


def restoreModel():
    model = None
    try:
        model = joblib.load(modelNameToSave)
    except:
        return model, False
    return model, True


def main():
    model, status = restoreModel()
    if not status:
        print("Cannot Find The Model In Local Storage 😥😥😥")
        exit()

    print("Model Successfully Restored 😀😎😍")
    drawer = DrawUsingMouse(penSize=45, penColor=(0, 0, 0))

    digitImg = drawer.getDrawing(dimensions=(8, 8))
    digitImg = cv.cvtColor(digitImg, cv.COLOR_BGR2GRAY)
    digitImg = 255-digitImg
    digitImg //= 10
    digitImg = np.reshape(digitImg, (1, 64))

    print("\nCaptured Image Value --------------------------")
    print(digitImg)
    print("\nCaptured Image Value --------------------------\n")

    pred = model.predict(digitImg)
    print("Predicted Digit is ", pred[0])


if __name__ == "__main__":
    os.system("cls")
    main()
