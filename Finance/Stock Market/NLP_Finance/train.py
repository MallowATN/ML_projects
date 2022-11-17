############################################## IMPORT LIBRARIES ##############################################
import numpy as np
import pandas as pd
from functions import *
import zipfile

#Preprocessing headlines libraries
import json
from os import listdir

#NLP
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

#Sklearn
from sklearn.model_selection import train_test_split
#Keras/TF
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.layers import Embedding
#If you haven't downloaded en_core_web_sm, you can download it from terminal
# !python -m spacy download en_core_web_lg
import en_core_web_lg

from os.path import isfile, join
from pandas.tseries.offsets import BDay
from scipy.stats.mstats import winsorize

import warnings
warnings.filterwarnings('ignore')

############################################## LOADING THE DATA ##############################################
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
data_df_news = pd.concat(data_df_news)
#Dataframe 2... We want to capture event return of R (t-1 & t+1) since reports that affects market often happens late, but
# we want to capture the whole entirety of the event with a slightly wider window. (the day before and the day aftter)
df_ticker_return = pd.read_csv(r'data\returnData.csv')
add_features(df_ticker_return)

#Merge all dataframe together and drop NaN
merge_df = pd.merge(data_df_news, df_ticker_return, how='left',left_on = ['date','ticker'], right_on=['date','ticker'])
merge_df = merge_df[merge_df['ticker'].isin(tickers)]
df = merge_df[['ticker','headline','date','eventRet','Close']]
df.dropna().to_csv(r'data\NewsAndReturnData.csv', sep='|', index=False) #this is our News arnd Return data

#Read in the data again and separate by "|"
df = pd.read_csv(r'data\NewsAndReturnData.csv', sep='|')
df = df.dropna()

### Model Evaluation with TextBlob ############################################################################
sentiments_data = pd.read_csv(r'data\LabelledNewsData.csv',encoding = "ISO-8859-1")
df['sentiment_textblob'] = [TextBlob(s).sentiment.polarity for s in df['headline']]

### Model evaluation LSTM (Supervised Learning) ###############################################################

#Tokenizer on sentiments data
vocabulary_size = 30000
tokenizer = Tokenizer(num_words=vocabulary_size)
tokenizer.fit_on_texts(sentiments_data['headline'])
sequences = tokenizer.texts_to_sequences(sentiments_data['headline'])

#Pad sequence of 50
X_LSTM = pad_sequences(sequences, maxlen=50)
y_LSTM = sentiments_data["sentiment"]
#Train test split
X_train_LSTM, X_test_LSTM, Y_train_LSTM, Y_test_LSTM = train_test_split(X_LSTM, \
                       y_LSTM, test_size=0.4, random_state=42)

#Create the model
def create_model(input_length=50):
    model = Sequential()
    model.add(Embedding(20000, 300, input_length=50))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])    
    return model    

LSTM_model = KerasClassifier(build_fn=create_model, epochs=3, verbose=1, validation_split=0.4)
LSTM_model.fit(X_train_LSTM, Y_train_LSTM)

#Tokenizer on the df headlines
sequences_LSTM = tokenizer.texts_to_sequences(df['headline'])
X_LSTM = pad_sequences(sequences_LSTM, maxlen=50)
df['sentiment_LSTM'] = Y_LSTM = LSTM_model.predict(X_LSTM)


### Model Evaluiation with Financial Lexicon (Unsupervised Learning) ###########################################
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

#Save the data for test phase.
df.to_csv(r'data\DataWithSentiments.csv', sep='|', index=False)