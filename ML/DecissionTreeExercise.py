import joblib
import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

csvFilePath = "titanic.csv"
modelNameToSave = "Titanic_Decission_Tree_Model"
test_size = 0.2
random_state = 10

labelToEncode = ["Sex", "Parch", "Ticket", "Cabin", "Embarked"]

featureList = ["PassengerId", "Pclass", "Sex", "Age",
               "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
targetLabel = "Survived"

nanValueFeatures = []


def restoreModel(modelName=modelNameToSave):
    model = None
    try:
        model = joblib.load(modelName)
    except:
        return model, False
    return model, True


def trainAndSaveModel(x_train, y_train, autosave=True, modelName=modelNameToSave):

    # para = [{'max_iter': [1, 10, 100, 100]}]
    # clf = GridSearchCV(LogisticRegression(), param_grid=para, cv=5, scoring='r2')

    # model = DecisionTreeClassifier()
    model = DecisionTreeClassifier()
    model.fit(x_train, y_train)

    if autosave:
        try:
            joblib.dump(model, modelName)
            return model, True
        except:
            return model, False

    return model, None


def encodeTheLables(df, lebelList):
    le = LabelEncoder()
    for l in lebelList:
        df[l] = le.fit_transform(df[l])

    return df


def dealWithNanValues(df: pd.DataFrame, featureList):
    df = df.dropna()
    # # print(df.head())

    # for l in featureList:
    #     print(l)
    #     df[l] = df.groupby(l).mean();
    # df.mean()

    return df


def preProcessData(df: pd.DataFrame):
    # naValuesList = df.isna().sum()
    # print(type(naValuesList))

    df = encodeTheLables(df, labelToEncode)
    # print(df.head())

    naValuesList = df.isna().sum()
    # print("\n------------\n",type(naValuesList))

    for lName, nanSize in naValuesList.items():
        if int(nanSize) > 0:
            # print(lName)
            nanValueFeatures.append(lName)

    df = dealWithNanValues(df, nanValueFeatures)

    x = np.array(df[featureList])
    y = np.array(df[targetLabel])

    return df, x, y


def mytrainTestSplit(x, y):
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train, y_test


def main():
    df = pd.read_csv(csvFilePath)

    df, x, y = preProcessData(df)
    # return
    x_train, x_test, y_train, y_test = mytrainTestSplit(x, y)

    if not os.path.exists(modelNameToSave):
        model, success = trainAndSaveModel(x_train, y_train)
        if success:
            print("Model Saved Successfully ------>>>>\n")
    else:
        model, success = restoreModel()
        if success:
            print("Model Restored Successfully ------>>>>\n")
        else:
            print("Error While Loading The Model From  The Local Storage !!!")

    # Accuracy
    print("Score = ", model.score(x, y))

    y_predict = model.predict(x_test)
    mse = mean_squared_error(y_test, y_predict)
    print("MSE = ", mse)

    # print("Test Data -------------")
    # print(x_test)

    # print("\nTest Data -------------")
    # print(y_test)
    # print(y_predict)

    print("\nComfussion Matrix -------------")
    cm = confusion_matrix(y_test, y_predict)
    print(cm)


if __name__ == "__main__":
    os.system("cls")
    main()
