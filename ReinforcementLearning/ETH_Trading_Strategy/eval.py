from agent import *
from helper_functions import *

import pandas as pd
from keras.models import load_model

crypto = 'ETH-USD'
df = pd.read_csv('data/'+crypto+'.csv', index_col=0) 
df = df.fillna(method='ffill')

X = list(df['Close'])
val_size = 0.2
train_size = int(len(X)*(1-val_size))
X_train, X_test = X[0:train_size], X[train_size:len(X)]

model_name = 'model_ep40.h5'
model = load_model('models/'+model_name)

#### IN PROGRESS ####