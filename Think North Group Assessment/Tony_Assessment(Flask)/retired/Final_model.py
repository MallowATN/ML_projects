import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

# Create the dataset
df = pd.read_csv(r'c:\Users\antho\Desktop\Tony_Assessment\retired\Account_Sales.csv')

# Dropped these features in our 'Final_TR_model.ipynb' file. Check for the feature selection tab.
df = df.drop(['Days Since Most Recent Deal Close','Employees','Billing Country','Industry',
                'Owner ID','Annual Revenue','Account Type','Average Age','Account Source',
                'Top Product Family','Days Since First Deal Close','Account ID', 'Account Name',
                'Created Date','Billing State/Province','Customer Priority','First Deal Date',
                'Number of Locations','Top Product Name'
                ],axis=1)

# Split the dataset with train test split
X = df.drop(columns='Total Revenue', axis=1)
y = df['Total Revenue']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=2)

pipe = Pipeline([('std_scaler', StandardScaler()),
                 ('GBR',GradientBoostingRegressor(n_estimators=150))])
pipe.fit(X_train, y_train)

# print(pipe.predict(X))

# Saving and loading model
import pickle
pickle.dump(pipe, open('Total_Rev.pkl','wb'))

with open('Total_Rev.pkl','rb') as f:
    model = pickle.load(f)