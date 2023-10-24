#


# 1. Gather data  https://www.javatpoint.com/how-to-get-datasets-for-machine-learning
#   Create a dataset:

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score  
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as pyp
from sklearn import metrics



dataSet = pd.read_csv("archive/Housing.csv")

def toNumericalValue():
    toNumVal = ("mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "prefarea")
    for i in toNumVal:
        dataSet[i] = dataSet[i].map({"yes": 1, "no": 0})
    workedData = pd.get_dummies(data=dataSet, columns=["furnishingstatus"], prefix=["furnish"])

    catToNum = ("furnish_furnished", "furnish_semi-furnished", "furnish_unfurnished")
    for i in catToNum:
        workedData[i] = workedData[i].map({True:1, False:0})
    finalData = workedData

    return finalData


processed_Data = toNumericalValue()

# Dependent variable 
depen_Variable = "furnish_furnished"

X = processed_Data
X = np.reshape(X, (np.size(X,0), np.size(X,1)))
X = np.delete(X, [12,13,14] ,axis=1)
y = processed_Data[depen_Variable]

scale = StandardScaler()
scaleX = scale.fit_transform(X)


# How to use predict/accuracy values to be sure the model is working properly
# Deploy app with machine learning
train_X, test_X, train_y, test_y = train_test_split(scaleX,y, test_size=0.20, random_state=2)

regr = LinearRegression()
regr.fit(train_X, train_y)

cross_score = np.mean(-cross_val_score(regr,train_X, train_y, cv=10))


# model
def testLinReg(price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwater, aircon, parking, prefarea):
    scaled = scale.transform([[price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwater, aircon, parking, prefarea]])
    pred = regr.predict(scaled)
    val = pred.item() * 100
    val = str(round(val, 2))
    print("Furnished percentage: " + val + "%")

def main():
    print(cross_score)
    #testLinReg(9240000,3500,4,2,2,1,0,0,1,0,2,0)

if __name__ == "__main__":
    main()