import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data_from_path(filepath):
    df = pd.read_csv(filepath)
    return df

def load_raw_data():
    input_path = "data/Account_Sales.csv"
    df = pd.read_csv(input_path)
    return df

def save_processed_data(df: pd.DataFrame):
    output_path = "data/Processed_Account_Sales.csv"
    df.to_csv(output_path, index=False)
    return

def load_processed_data():
    input_path = "data/Processed_Account_Sales.csv"
    df = load_data_from_path(input_path)
    return df

def save_train_test_data(X_train, y_train,X_test, y_test):
    pd.DataFrame(X_train).to_csv("data/train_model_data/train_data.csv", index=False)
    pd.DataFrame(y_train).to_csv("data/train_model_data/train_data_result.csv", index=False)
    pd.DataFrame(X_test).to_csv("data/test_model_data/test_data.csv", index=False)
    pd.DataFrame(y_test).to_csv("data/test_model_data/test_data_result.csv", index=False)
    return

def split_train_test_data():
    df = load_processed_data()
    X = df.drop('Total Revenue',axis=1)
    y = df['Total Revenue'].values
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=2)
    save_train_test_data(X_train, y_train, X_test, y_test)
    return X_train, y_train, X_test, y_test