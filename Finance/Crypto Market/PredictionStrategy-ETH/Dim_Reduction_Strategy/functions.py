import numpy as np
import pandas as pd


def signals(df):
    df['short_mavg'] = df['Close'].rolling(window=10, min_periods=1, center=False).mean()
    df['long_mavg'] = df['Close'].rolling(window=60, min_periods=1, center=False).mean()
    df['signal'] = np.where(df['short_mavg'] > df['long_mavg'], 1.0, 0.0)

def SMA(df): #Short Moving Average
    df['SMA_21days'] = df.iloc[:,3].rolling(window=21).mean()
    df['SMA_50days'] = df.iloc[:,3].rolling(window=50).mean()
    df['SMA_100days'] = df.iloc[:,3].rolling(window=100).mean()
    df['SMA_150days'] = df.iloc[:,3].rolling(window=150).mean()

def EMA(df): #Exponential Moving Average
    df['EMA_21days'] = df['Close'].ewm(span=21,adjust=False).mean()
    df['EMA_50days'] = df['Close'].ewm(span=50,adjust=False).mean()
    df['EMA_100days'] = df['Close'].ewm(span=100,adjust=False).mean()
    df['EMA_150days'] = df['Close'].ewm(span=150,adjust=False).mean()

def RSIs(df,n): #Relative Strength Index
    df['diff'] = df.Close.diff()
    df['pos'] = df['diff'].clip(lower=0)
    df['neg'] = -1*df['diff'].clip(upper=0)
    ema_pos = df['pos'].ewm(com=(n-1), adjust=False).mean()
    ema_neg = df['neg'].ewm(com=(n-1), adjust=False).mean()
    relative_str = ema_pos / ema_neg
    df['RSI'+str(n)] = 100-(100/(1+relative_str))
    df['Stochastic_RSI'+str(n)] = (df['RSI'+str(n)]-df['RSI'+str(n)].rolling(n).min())/(df['RSI'+str(n)].rolling(n).max()-(df['RSI'+str(n)].rolling(n).min()))

def ROC(df, n): #Rate of Change
    M = df.diff(n-1)
    N = df.shift(n-1)
    ROC = pd.Series(((M/N)*100),name='Roc_'+str(n))
    return ROC

def MOM(df,n): #Momentum
    MOM = pd.Series(df.diff(n), name='Momentum_' + str(n))
    return MOM

def MACD(df): # Moving Average Convergence Divergence... default is 12-26-9
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1-exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

def Stochastic(df,n): #Stochastic Oscillator
    high = df['High'].rolling(n).max()
    low = df['Low'].rolling(n).min()
    df['%K'+str(n)] = (df['Close']-low)*100/(high-low) #current price in relation to the asset's recent price change...
    df['%D'+str(n)] = df['%K'+str(n)].rolling(3).mean() #3 period average of %K