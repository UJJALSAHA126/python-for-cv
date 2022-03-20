import pandas as pd
from sklearn import model_selection, preprocessing, linear_model
from sklearn.metrics import mean_squared_error
import sklearn
import numpy as np
import os

dataFile = "houses_to_rent.csv"
requiredFeatures = ['city', 'area', 'rooms', 'bathroom',
                    'parking spaces', 'furniture', 'fire insurance',
                    'rent amount', 'total']

dollarList = ['fire insurance', 'rent amount', 'total']

featureEncoderList = ['furniture']

outputLabel = 'rent amount'


def changeConsoleForeGrount(color: int):
    print(f'\033[1;{color}m', end='')


def printSeparation(heading: str, changeColor=False):
    i = 60
    num1, num2 = 36, 37
    if changeColor:
        changeConsoleForeGrount(num1)
    print('\n' + '-'*i + f'\n{heading}\n' + '-'*i)
    if changeColor:
        changeConsoleForeGrount(num2)


def sliceData(data: pd.DataFrame, printHeading=True, changeColor=False):
    if printHeading:
        printSeparation('Slicing The Required Data', changeColor)

    return data[requiredFeatures]


def processAndModifyData(data: pd.DataFrame, printHeading=True, changeColor=False):
    if printHeading:
        printSeparation('Processing Data', changeColor)

    for i in dollarList:
        data[i] = data[i].map(
            lambda i: int(str(i).replace('R$', '').replace(',', '')))

    #  Preprocessing Label Encoder
    le = preprocessing.LabelEncoder()
    for feature in featureEncoderList:
        data[feature] = le.fit_transform(data[feature])

    return data


def main():
    os.system('cls')
    # printSeparation('Loading Data')
    data = pd.read_csv(dataFile, sep=',')
    # print(data.head())

    # If There is a NAN value in the .csv file; .dronna() Drops All the nan values and returns the new dataset
    # print(data.isnull().sum())
    # data = data.dropna()
    # print(data.head())

    data = sliceData(data, False)
    # print(data.head())
    data = processAndModifyData(data, False)
    # print(data.head())

    x = np.array(data.drop(columns=[outputLabel], axis=1))
    y = np.array(data[outputLabel])

    # print('X Shape = ', x.shape, '\nY Shape  = ', y.shape)

    xTrain, xTest, yTrain, yTest = model_selection.train_test_split(
        x, y, test_size=0.2, random_state=10)

    # print('X Train Shape = ', xTrain.shape)
    # print('X Test Shape = ', xTest.shape)
    # print('Y Train Shape = ', yTrain.shape)
    # print('Y Test Shape = ', yTest.shape)

    printSeparation('Model Training')
    model = linear_model.LinearRegression()
    model.fit(xTrain, yTrain)
    accuracy = model.score(xTest, yTest)*100

    print('Co-Efficients = ', model.coef_)
    print('Intercepets = ', model.intercept_)
    print('Accuracy = '+str(round(accuracy, 3))+'%')

    printSeparation('Predecting Values')
    testValues = model.predict(xTest)
    error = 0
    for i, testValue in enumerate(testValues):
        error += pow(yTest[i]-testValue, 2)
    meanSquredError = error/i

    print('My Mean Squared Error      : ', meanSquredError)
    # print(yTest.shape,'\n',testValues.shape)
    print('Sklearn Mean Squared Error : ',
          mean_squared_error(yTest, testValues))


if __name__ == '__main__':
    main()
