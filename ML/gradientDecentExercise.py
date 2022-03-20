import math
import os
import numpy as np
import pandas as pd
from sklearn import linear_model

actualM = 0
actualB = 0


def gradient_decent(x, y):
    m_curr = b_curr = 0
    iteration = 0
    n = len(x)
    learningRate = 0.00001
    print("Running..........")
    pcost = None
    while True:
        iteration += 1
        y_predicted = m_curr * x + b_curr
        cost = (1/n) * sum([val**2 for val in (y-y_predicted)])
        if(pcost):
            if(math.isclose(pcost, cost, rel_tol=1e-5)):
                break
        # if(pcost):
        #     if(math.isclose(pcost, cost, rel_tol=1e-5)):
        #         if(math.isclose(actualM, m_curr, rel_tol=1e-2) and math.isclose(actualB, b_curr, rel_tol=1e-2)):
        #             break
        print("*",end="")
        pcost = cost
        md = -(2/n)*sum(x*(y-y_predicted))
        bd = -(2/n)*sum(y-y_predicted)

        m_curr = m_curr - learningRate * md
        b_curr = b_curr - learningRate * bd

    print("\nM = {}, B = {}".format(actualM, actualB))
    print("*****M = {}, B = {}".format(m_curr, b_curr))
    print("Iterations = {}, Learning Rate = {}".format(iteration, learningRate))


def liner_reg(x, y):
    global actualM, actualB
    model = linear_model.LinearRegression()
    model.fit(x, y)
    actualM = model.coef_
    actualB = model.intercept_

    print("M = {}, B = {}".format(actualM, actualB))


def main():
    global data, x, y
    data = pd.read_csv("test_scores.csv", sep=",")
    x = np.array(data['math'])
    x1 = x.reshape((10, 1))
    y = np.array(data['cs'])
    print(x.shape, y.shape)
    liner_reg(x1, y)
    gradient_decent(x, y)


if __name__ == "__main__":
    main()
