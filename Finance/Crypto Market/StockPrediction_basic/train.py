import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from functions import *


#########################################
############## DATA PREP ################
#########################################

# Load the data
df = pd.read_csv("ETH-USD.csv")

# Prepare the dataframe
df = df.set_index('Date')

SMA(df)
EMA(df)
RSIs(df)

df=df.drop(['pos','neg','diff','Open','High','Low'], axis=1)
#Drop the nan rows bc we had to use rolling method to obtain the MA & RSI
df = df.dropna(axis=0)

# Split data into train/test split
X = df.drop('Close',axis=1)
Y = df['Close']

validation_size = 0.3
train_size = int(len(X) * (1-validation_size))
X_train, X_validation = X[0:train_size], X[train_size:len(X)]
y_train, y_validation = Y[0:train_size], Y[train_size:len(X)]

#########################################
################# MODEL #################
#########################################

# Fit model on train
model = RandomForestRegressor()
model.fit(X_train, y_train)

#Report training set score
train_score = model.score(X_train, y_train)*100
#Report test set score
test_score = model.score(X_validation, y_validation)*100

#Write evaluation to file
with open("metrics.txt", 'w') as outfile:
    outfile.write("Training variance explained: %2.1f%%\n"%train_score)
    outfile.write("Test variance explained: %2.1f%%\n"%test_score)