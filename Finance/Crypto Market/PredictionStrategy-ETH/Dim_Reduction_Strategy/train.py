import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from functions import *

import time

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier

# Loading the data
df = pd.read_csv('data/ETH-USD.csv')

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

# Standard Scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
rs_df = pd.DataFrame(X_scaled, columns = X_train.columns, index=X_train.index)

X_train.dropna(how='any', inplace=True)
rs_df.dropna(how='any', inplace=True)

#Dimensionality Reduction - SVD
ncomps = 10
svd = TruncatedSVD(n_components=ncomps)
svd_fit = svd.fit(rs_df)

# projected Eigenvalues
y_pred = svd.fit_transform(rs_df)
svd_df = pd.DataFrame(y_pred, columns=['c{}'.format(c) for c in range(ncomps)], index=rs_df.index)
compressed_df_cols = [c for c in svd_df.columns if c[0] == 'c']

# We use the Random Forest Classifier and will test the speed of ML algorithm with Dimensionality Reduction and without.
model = RandomForestClassifier(criterion='entropy', max_depth=10, n_estimators=80, n_jobs=-1)
model.fit(X_train, y_train)

scoring = 'accuracy'
#scoring = 'precision'
#scoring = 'recall'
#scoring ='neg_log_loss'
#scoring = 'roc_auc'

kfold = KFold(n_splits=10)
cv_results = cross_val_score(model, X_train, y_train, cv=kfold,scoring=scoring)

# Result - without the Dimensionality Reduction
start_time = time.time()
model = RandomForestClassifier(criterion='entropy', max_depth=10, n_estimators=80, n_jobs=-1)
cv_results_XTrain= cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)

time_no_DR = "Time Without Dimensionality Reduction--- %s seconds --- \n" % (time.time() - start_time)
result_no_DR= "Result without Dimensionality Reduction: %f (%f)\n" % (cv_results_XTrain.mean(), cv_results_XTrain.std())

#Time with the Dimensionality Reduction
start_time = time.time()
X_SVD= svd_df[compressed_df_cols].iloc[:,:10]
cv_results_SVD = cross_val_score(model, X_SVD, y_train, cv=kfold, scoring=scoring)

time_DR = "Time With Dimensionality Reduction--- %s seconds --- \n" % (time.time() - start_time)
result_DR = "Result with Dimensionality Reduction: %f (%f)" % (cv_results_SVD.mean(), cv_results_SVD.std())

#Write evaluation to file
with open("metrics.txt", 'w') as outfile:
    outfile.write(time_no_DR)
    outfile.write(result_no_DR)
    outfile.write(time_DR)
    outfile.write(result_DR)
