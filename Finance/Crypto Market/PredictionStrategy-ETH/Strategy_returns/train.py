import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from functions import *

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Loading the data
df = pd.read_csv('ETH-USD.csv')

# Load the Feature Engineered functions from functions.py
signals(df)
SMA(df)
RSIs(df, 21)
RSIs(df, 50)
RSIs(df, 100)
RSIs(df, 150)
df['ROC21'] = ROC(df['Close'],21)
df['ROC50'] = ROC(df['Close'],50)
df['ROC100'] = ROC(df['Close'],100)
df['ROC150'] = ROC(df['Close'],150)
df['MOM21'] = MOM(df['Close'], 21)
df['MOM50'] = MOM(df['Close'], 50)
df['MOM100'] = MOM(df['Close'], 100)
df['MOM150'] = MOM(df['Close'], 150)
MACD(df)
Stochastic(df,21)
Stochastic(df,50)
Stochastic(df,100)
Stochastic(df,150)

#Drop unnecessary features
df = df.drop(['Open','Date','High','Low', 'short_mavg','long_mavg'],axis=1)

# Create train and validation set
val_size = 0.2
seed = 42
val = int(df.shape[0]*0.8)
subset = df.iloc[-val:]
X = subset.loc[:, df.columns != 'signal']
y = subset['signal']

X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=val_size, random_state=seed)

# We use the Random Forest Classifier that has already been fine-tuned with GridSearch CV. Check the ETH_predictor notebook.
model = RandomForestClassifier(criterion='gini', max_depth=10, n_estimators=20)
model.fit(X_train, y_train)

#Report training set score
train_score = model.score(X_train, y_train)*100
#Report test set score
test_score = model.score(X_val, y_val)*100

#Write evaluation to file
with open("metrics.txt", 'w') as outfile:
    outfile.write("Training variance explained: %2.1f%%\n"%train_score)
    outfile.write("Test variance explained: %2.1f%%\n"%test_score)