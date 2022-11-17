import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from copy import copy
from datetime import date
import yfinance as yf

import zipfile

#NLP
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

#If you haven't downloaded en_core_web_sm, you can download it from terminal
# !python -m spacy download en_core_web_lg
import en_core_web_lg

#Preprocessing headlines libraries
from lxml import etree
import json
from io import StringIO
from os import listdir

from os.path import isfile, join
from pandas.tseries.offsets import BDay
from scipy.stats.mstats import winsorize

#Keras/TF
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM
from tensorflow.keras.layers import Embedding

from functions import *

#Classification
from keras.wrappers.scikit_learn import KerasClassifier

import warnings
warnings.filterwarnings('ignore')

nlp = en_core_web_lg.load()
get_tick_data()

# We can't use json format for NLP algorithm...
# Need to parse the news from json files and Regex is crucial, as it finds pattern in raw messy text and perform parsing action
z = zipfile.ZipFile("Data/Raw Headline Data.zip", "r")
testFile=z.namelist()[10]
fileData= z.open(testFile).read() 
jsonParser(json.loads(fileData))[1][1]

#JSON
jsonextractor()

#Dataframe 1... We will merge the all later
# data_df_news = pd.concat(data_df_news)
#Dataframe 2... We want to capture event return of R (t-1 & t+1) since reports that affects market often happens late, but
# we want to capture the whole entirety of the event with a slightly wider window. (the day before and the day aftter)
df_ticker_return = pd.read_csv('data/returnData.csv')
add_features(df_ticker_return)

#Merge all dataframe together and drop NaN
merge_df = pd.merge(data_df_news, df_ticker_return, how='left',left_on = ['date','ticker'], right_on=['date','ticker'])
merge_df = merge_df[merge_df['ticker'].isin(tickers)]
df = merge_df[['ticker','headline','date','eventRet','Close']]
df = df.dropna()
df.to_csv(r'data\NewsAndReturnData.csv', sep='|', index=False) #this is our News arnd Return data

#Read in the data again and separate by "|"
df = pd.read_csv('data/NewsAndReturnData.csv', sep='|')

#Model Evaluiation with Financial Lexicon (Unsupervised Learning)
sia = SentimentIntensityAnalyzer()
stock_lex = pd.read_csv('data\LexiconData.csv')
stock_lex['sentiment'] = (stock_lex['Aff_Score'] + stock_lex['Neg_Score'])/2
stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
stock_lex = {k:v for k,v in stock_lex.items() if len(k.split(' '))==1}
stock_lex_scaled = {}
for k, v in stock_lex.items():
    if v > 0:
        stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
    else:
        stock_lex_scaled[k] = v / min(stock_lex.values()) * -4

final_lex = {}
final_lex.update(stock_lex_scaled)
final_lex.update(sia.lexicon)
sia.lexicon = final_lex

#Extract sentiment for entire dataset and add to df
vader_sentiments = pd.np.array([sia.polarity_scores(s)['compound'] for s in df['headline']])
df['sentiment_lex'] = vader_sentiments
