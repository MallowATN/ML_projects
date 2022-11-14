import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import os

PROJECT_ROOT_DIR = "."
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
os.makedirs(IMAGES_PATH, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

def formatPrice(n):
    return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

#Sigmoid Function
def sigmoid(x):
    return 1/(1+np.exp(-x))

#get state history
def get_state(data, t, n):
    d = t-n+1
    block = data[d:t+1] if d>=0 else -d*[data[0]]+data[0:t+1]
    res = []

    for i in range(n-1):
        res.append(sigmoid(block[i+1]-block[i]))
        return np.array([res])

#plot the charts
def plot_behavior(df_input, buy_states, sell_states, gains, name):
    fig = plt.figure(figsize=(20,8))
    plt.plot(df_input, color='b')
    plt.plot(df_input, 'v', color='r', label='Sell Signal', markevery=sell_states, markersize=8)
    plt.plot(df_input, '^', color='g', label='Buy Signal', markevery=buy_states, markersize=8)
    plt.legend()
    plt.title(name+' Total profits: %f'%(gains))
    save_fig(name, tight_layout=True)
    # plt.show() Toggle on or off if you want to view while running, else just look in the folder

def get_crypto_data(crypto, date): 
    # i.e: ETH-USD, BTC-USD, etc. must be available to locate on YF
    # date in mm/dd/yyyy in strings
    df = pdr.DataReader(crypto, 'yahoo', date)
    df.sort_index(inplace=True)
    df.to_csv('data/'+crypto+'.csv')
    return df

