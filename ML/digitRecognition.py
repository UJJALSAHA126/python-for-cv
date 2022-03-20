from statistics import mode
import cv2 as cv
import numpy as np
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.engine import Sequential
from keras.layers import Conv2D, MaxPooling2D,Dropout,Dense,Flatten
from keras.optimizers import Adam
import keras


# ******************************************************************

path = "myData"
noOfClasses = 0
images = []
classNo = []
myList = []
test_ratio = 0.2
val_ratio = 0.2
imageDimensions = (32, 32, 3)

# ******************************************************************


def preProcessing(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.equalizeHist(img)
    img = img/255
    return img


def myModel():
    noOfFilters = 60
    sizeOfFilter1 = (5, 5)
    sizeOfFilter2 = (3, 3)
    sizeOfPool = (2, 2)
    noOfNodes = 500

    model = Sequential()
    model.add(Conv2D(noOfFilters, sizeOfFilter1, input_shape=(
        imageDimensions[0], imageDimensions[1], 1),activation='relu'))

    model.add(Conv2D(noOfFilters, sizeOfFilter1, activation='relu'))

    model.add(MaxPooling2D(pool_size=sizeOfPool))
    
    model.add(Conv2D(noOfFilters//2, sizeOfFilter2, activation='relu'))
    model.add(Conv2D(noOfFilters//2, sizeOfFilter2, activation='relu'))
    
    model.add(MaxPooling2D(pool_size=sizeOfPool))
    model.add(Dropout(0.5))
    
    model.add(Flatten())
    model.add(Dense(noOfNodes,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(0.5))
    model.add(Dense(noOfClasses,activation='softmax'))
    model.compile(Adam(lr=0.001),loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
    

def main():
    global myList, images, classNo, noOfClasses

    myList = os.listdir(path)
    noOfClasses = len(myList)
    print("Total Data Sets Detected =", len(myList))
    print("Importing Image Data ......")
    for l in myList:
        imgList = os.listdir(path+"/"+l)
        for img in imgList:
            image = cv.imread(path+"/"+l+"/"+img)
            image = cv.resize(image, (32, 32))
            images.append(image)
            classNo.append(int(l))
        print(l, end=" ")

    print("")
    images = np.array(images)
    classNo = np.array(classNo)

    x_train, x_test, y_train, y_test = train_test_split(
        images, classNo, test_size=test_ratio)

    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train, y_train, test_size=val_ratio)

    noOfSamples = []
    for x in range(0, noOfClasses):
        noOfSamples.append(len(np.where(y_train == 0)[0]))

    print(noOfSamples)

    # plt.figure(figsize=(10,5))
    # plt.bar(range(0,noOfClasses),noOfSamples)
    # plt.title("No of images of each class")
    # plt.xlabel("Class ID")
    # plt.ylabel("Number of Images")
    # plt.show()

    # img = preProcessing(x_train[30])
    # img = cv.resize(img, (300, 300))
    # cv.imshow("PreProcessed Image", img)
    # cv.waitKey(0)

    x_train = np.array(list(map(preProcessing, x_train)))
    x_test = np.array(list(map(preProcessing, x_test)))
    x_validation = np.array(list(map(preProcessing, x_validation)))

    x_train = x_train.reshape(
        x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
    x_test = x_test.reshape(
        x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
    x_validation = x_validation.reshape(
        x_validation.shape[0], x_validation.shape[1], x_validation.shape[2], 1)

    data_generator = ImageDataGenerator(width_shift_range=0.1,
                                        height_shift_range=0.1,
                                        zoom_range=0.2,
                                        shear_range=0.1,
                                        rotation_range=10)

    data_generator.fit(x_train)
    y_train = to_categorical(y_train, noOfClasses)
    y_test = to_categorical(y_test, noOfClasses)
    y_validation = to_categorical(y_validation, noOfClasses)

    model = myModel()
    print(model.summary())

if __name__ == '__main__':
    # l="0"
    # print(int(l) +1)
    os.system('cls')
    main()
