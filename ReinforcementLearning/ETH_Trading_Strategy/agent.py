from collections import deque

import numpy as np
from numpy.random import choice
import random

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

class Agent:
    #Constructor
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size #this is the window size, n previous days
        self.action_size = 3 # buy/sell/HODL
        self.memory = deque(maxlen=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval #lets me know if training is ongoing

        #epsilon greedy approach factor... We will try random condition first before optimizing. We add eps-greedy policy 
        #with eps=0.05. THIS IS TO PREVENT OVERFITTING
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.gamma = 0.95 #discount factor...agent prioritize short-term rewards > long-term rewards..lower=shift to long-term

        self.model = load_model(model_name) if is_eval else self._model()
    
    #Now we build the Deep Q-Learn model that returns q-value when inputs are states at t=1,...,t=T
    def _model(self):
        model = Sequential() #from keras
        
        #Input layer
        model.add(Dense(units=64, input_dim=self.state_size, activation='relu'))

        #Hidden layers
        model.add(Dense(units=32, activation='relu'))
        model.add(Dense(units=8, activation='relu'))

        #Final Output Layer
        model.add(Dense(self.action_size, activation='linear')) # output dim = action size = buy/sell/HODL... (3)
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

# We need to return action on value function with:
# - prob (1-eps)... action will be based on highest Q-value
# - prob (eps)... action will be randomly picked

#Basically, there's going to be higher epsilon in the initial phase, but as we train RL, it will later on be less... 
# We need to make an action

    #Action
    def actions(self, state):
        if not self.is_eval and random.random() <= self.epsilon: #If tested & self.eps still high... go random
            return random.randrange(self.action_size) 
        options = self.model.predict(state)
        return np.argmax(options[0]) #So.. choose the corresponding action based on highest q-value func

    #Memory.. so NN is trained based on observed experience.. stores state history/action/reward/next state experienced by agent
    # Takes in minibatch as inputs and updates Deep Q-model weights by minimizing loss function
    def exp_replay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        
        for i in range(l-batch_size+1, l):
            mini_batch.append(self.memory[i])

        #memory during training
        for state, action, reward, next_state, done in mini_batch:
            # At time t... reward
            target=reward
            #update Q table from Q table eq
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            
            #Q-value of current state from table
            target_f = self.model.predict(state)
            #update Q table for output after action given
            target_f[0][action] = target
            #train and fit model when in X state... if Y state, target_f (target is updated)
            self.model.fit(state, target_f, epochs=1, verbose=0)
        
        #Finally implimenting the eps-greedy approach
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay