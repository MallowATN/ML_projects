import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
from functions import *
from sklearn.model_selection import train_test_split

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
df = df.dropna(axis=0)

# Split data into train/test split
X = df.drop('Close',axis=1)
Y = df['Close'].values

X_train, X_validation, Y_train, Y_validation = train_test_split(X,Y, test_size=0.2, random_state=42)


#########################################
################# MODEL #################
#########################################

# Fit model on train
model = KNeighborsRegressor(n_neighbors=3)
model.fit(X_train, Y_train)

#Report training set score
train_score = model.score(X_train, Y_train)*100
#Report test set score
test_score = model.score(X_validation, Y_validation)*100

#Write evaluation to file
with open("metrics.txt", 'w') as outfile:
    outfile.write("Training variance explained: %2.1f%%\n"%train_score)
    outfile.write("Test variance explained: %2.1f%%\n"%test_score)