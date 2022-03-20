# --------------------------------------------------------------
# Classifier Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
# --------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
import joblib
import os
import cv2 as cv

modelNameToSave = "Digit_Recognizer_Model"
test_size = 0.21
random_state = 10

labelList = "target"


def mytrainTestSplit(x, y):
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train, y_test


def restoreModel():
    model = None
    try:
        model = joblib.load(modelNameToSave)
    except:
        return model, False
    return model, True


def trainAndSaveModel(x_train, y_train, autosave=True):

    # #Using Random Forest Classifier
    # model = RandomForestClassifier()
    # model = RandomForestClassifier(n_estimators=200)  #96.94%

    # #Usig LogisticRegression
    # model = LogisticRegression(solver='lbfgs', max_iter=100000) #95.28%

    #  #Using Support Vector Machine
    # model = SVC()
    # model = SVC(C=1)
    # model = SVC(gamma=3)
    model = SVC(C=1) #98.33%

    # #Linear Kermal Model
    # model = SVC(kernel="linear")  # 97.5%

    # Training The Model
    model.fit(x_train, y_train)

    try:
        if autosave:
            joblib.dump(model, modelNameToSave)
        return model, True
    except:
        return model, False


def preprocessDf():
    digits = load_digits()
    df = pd.DataFrame(digits.data)
    df["target"] = digits.target

    x = np.array(df.drop(columns=labelList, axis=1))
    y = np.array(df["target"])

    return df, x, y


def main():
    df, x, y = preprocessDf()
    x_train, x_test, y_train, y_test = mytrainTestSplit(x, y)

    model, status = trainAndSaveModel(x_train, y_train)
    if status:
        print("\nModel Trained And Saved Successfully ------>>>>\n")

    score = model.score(x_test, y_test)*100
    print("Model Score =", round(score, 2), "%")

    y_predicted = model.predict(x_test)
    cm = confusion_matrix(y_test, y_predicted)

    # plt.figure(figsize=(7, 5))
    # sb.heatmap(cm, annot=True)
    # plt.xlabel("Predicted")
    # plt.ylabel("Truth")
    # plt.show()


if __name__ == '__main__':
    # os.system("cls")
    main()
