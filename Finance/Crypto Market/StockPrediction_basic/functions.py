import numpy as np
import pandas as pd

def SMA(df):
    df['SMA_21days'] = df.iloc[:,4].rolling(window=21).mean()
    df['SMA_50days'] = df.iloc[:,4].rolling(window=50).mean()
    df['SMA_100days'] = df.iloc[:,4].rolling(window=100).mean()

def EMA(df):
    df['EMA_21days'] = df['Close'].ewm(span=21,adjust=False).mean()
    df['EMA_50days'] = df['Close'].ewm(span=50,adjust=False).mean()
    df['EMA_100days'] = df['Close'].ewm(span=100,adjust=False).mean()

def RSIs(df):
    df['diff'] = df.Close.diff()
    df['pos'] = df['diff'].clip(lower=0)
    df['neg'] = -1*df['diff'].clip(upper=0)
    ema_pos = df['pos'].ewm(com=13, adjust=False).mean()
    ema_neg = df['neg'].ewm(com=13, adjust=False).mean()
    relative_str = ema_pos / ema_neg
    df['RSI'] = 100-(100/(1+relative_str))
    df['Stochastic_RSI'] = (df['RSI']-df['RSI'].rolling(14).min())/(df['RSI'].rolling(14).max()-(df['RSI'].rolling(14).min()))

