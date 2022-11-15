import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
from functions import *




#########################################
############## DATA PREP ################
#########################################

# Load the data
df = pd.read_csv("ETH_hist.csv")

# Prepare the dataframe
for column in df:
    df.columns = ['Date', 'Open','High','Low','Close','Volume','Market Cap']
for i in df.columns[1:7]:
    df[i] = df[i].str.replace(',','')
    df[i] = df[i].str.replace('$','', regex=True)
    df[i] = df[i].astype(float)
df['Volume'] = df['Volume'].astype(np.int64)
df['Market Cap'] = df['Market Cap'].astype(np.int64)

df = df.set_index('Date')

SMA(df)
EMA(df)
RSIs(df)

df=df.drop(['pos','neg','Log Return','diff','Open','High','Low'], axis=1)

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
model = KNeighborsRegressor(n_neighbors=3)
model.fit(X_train, y_validation)

#Report training set score
train_score = model.score(X_train, y_train)*100
#Report test set score
test_score = model.score(X_validation, y_validation)*100

#Write evaluation to file
with open("metrics.txt", 'w') as outfile:
    outfile.write("Training variance explained: %2.1f%%\n"%train_score)
    outfile.write("Test variance explained: %2.1f%%\n"%test_score)

#########################################
######## PLOT FEATURE IMPORTANCE ########
#########################################

importances = model.feature_importances_
labels = df.columns
feature_df = pd.DataFrame(list(zip(labels, importances)), columns = ["feature","importance"])
feature_df = feature_df.sort_values(by='importance', ascending=False)

#image formatting
axis_fs = 18
title_fs = 22
sns.set(style="whitegrid")

ax = sns.barplot(x="importance", y="feature", data = feature_df)
ax.set_xlabel('Importance"', fontsize=axis_fs)
ax.set_ylabel('Feature', fontsize=axis_fs)
ax.set_title('Residuals', fontsize=title_fs)

#square aspect ratio
ax.plot([1,10], [1,10], 'black', linewidth=1)
plt.ylim((2.5, 8.5))
plt.xlim((2.5, 8.5))
plt.tight_layout()
plt.savefig("images/residuals.png", dpi=120)