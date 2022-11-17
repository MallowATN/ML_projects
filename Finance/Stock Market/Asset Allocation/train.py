import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions import *

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

# Load in the data
df = pd.read_csv('data/dow_adjcloses.csv', index_col=0)

# Preprocessing
# Drop NaN values... These securities occured much later, was missing a lot of values... 92% missing in DWPD, 43% missing in V
df = df.drop(['DWDP','V'],axis=1)
df = df.fillna(method='ffill')

df_return = df.pct_change(1) #daily linear return
df_return= df_return[df_return.apply(lambda x :(x-x.mean()).abs()<(3*x.std())).all(1)] #Remove outliers beyond 3 std.

#Standard Scaling
scaler = StandardScaler().fit(df_return)
rs_df = pd.DataFrame(scaler.fit_transform(df_return),columns = df_return.columns, index = df_return.index)

# Split the dataset
percentage=int(rs_df.shape[0]*0.8)
X_train, X_test = rs_df[:percentage], rs_df[percentage:]
X_train_clean, X_test_clean = df_return[:percentage], df_return[percentage:]
stock_ticks = rs_df.columns.values

# Weight params
weights = pcWeights(X_train)
n_tickers = stock_ticks.shape[0]

#Specify portfolio you want to view: range = 0|28 I believe, but remember... choose the one with the highest Sharpe ratio (AKA 0)
eigen=weights[0]

#Evaluate model - Apply PCA
pcomp = pca.fit(X_train)
final_port(rs_df,X_train_clean)
Backtest(eigen, X_test_clean, X_test, stock_ticks)
