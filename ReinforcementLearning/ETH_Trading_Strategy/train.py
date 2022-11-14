from agent import *
from helper_functions import *
import pandas as pd

#Grab the crypto historical data
crypto = 'ETH-USD'
get_crypto_data(crypto, '01/01/2020')

#Read in the data frame and data wrangle
df = pd.read_csv('data/'+crypto+'.csv', index_col=0) 
df = df.fillna(method='ffill')

#Create your train and test set.. (80% train, 20% test) 
# Validation set should always be the last few months from current day for crypto prediction
X = list(df['Close'])
val_size = 0.2
train_size = int(len(X)*(1-val_size))
X_train, X_test = X[0:train_size], X[train_size:len(X)]

#Training phase
window_size = 1
agent = Agent(window_size)
data = X_train
l = len(data)-1
batch_size = 64
episode_count = 360

for e in range(episode_count+1):
    print("Running episode "+str(e)+"/"+str(episode_count))
    state = get_state(data, 0, window_size+1)
    total_profit = 0
    agent.inventory=[]
    buy_states = []
    sell_states = []

    for t in range(l):
        action = agent.actions(state)
        next_state = get_state(data, t+1, window_size+1)
        reward = 0
        if action == 1: # BUY ACTION AND ADD TO INVENTORY
            agent.inventory.append(data[t])
            buy_states.append(t)
#             print("Buy: " + formatPrice(data[t]))

        elif action == 2 and len(agent.inventory) > 0: # SELL ACTION IF YOU OWN ETH 
            bought_price = agent.inventory.pop(0)
            reward = max(data[t]-bought_price,0) 
            total_profit += data[t]-bought_price #Profit difference
            sell_states.append(t)
#             print("Sell: " + formatPrice(data[t]) + " | Profit: "+formatPrice(data[t]-bought_price))

        done = True if t == (l-1) else False
        #append the state action information in memory for exp_replay...
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state

        if done:
            print('--------------------------------')
            print('Total Profit: ' + formatPrice(total_profit))
            print('--------------------------------')
            
            plot_behavior(data, buy_states, sell_states, total_profit,'Episode_'+str(e))
        if len(agent.memory) > batch_size:
            agent.exp_replay(batch_size)
    if e % 10 == 0:
        agent.model.save('models/model_ep'+str(e))