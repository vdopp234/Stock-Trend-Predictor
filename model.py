#Preprocessing Imports
import data_collection as dc
import data_processing as dp
import numpy as np
#NN imports
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

def model(x, y):

    model = Sequential()
    model.add(LSTM(128, input_shape = (3, 8), return_sequences = True))
    model.add(LSTM(64, return_sequences = False))
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(1, activation = 'relu'))

    model.compile(loss = 'mse', optimizer = 'rmsprop', metrics = ['accuracy'])
    model.fit(x, y, batch_size = 1, epochs = 10)
    return model

def create_sequence(stock, start_date, window_size):
    curr_date = start_date
    curr_sequence = dp.f_vec(stock, curr_date)
    for _ in len(range(window_size - 1)):
        next_day = int(start_date[2:4]) + 1
        next_month = str(int(start_date[:2]))
        if next_day == 32 or (next_day == 31 and (next_month == 4 or next_month == 6 or next_month == 9 or next_month == 11)):
            next_month = str(int(next_month) + 1)
            next_day = 0
        if next_day < 10:
            next_day = '0' + next_day
        else:
            next_day = str(next_day)
        curr_date = curr_date[:2] + next_day + start_date[4:]
        new_vec = dp.f_vec(curr_date)
        curr_sequence = np.vstack((curr_sequence, new_vec.T))
    next_day = int(start_date[2:4]) + window_size
    next_month = str(int(start_date[:2]))
    #Change month if necessary
    if next_day == 32 or (next_day == 31 and (next_month == 4 or next_month == 6 or next_month == 9 or next_month == 11)):
        next_month = str(int(next_month) + 1)
        next_day = 0
    if next_day < 10:
        next_day = '0' + next_day
    else:
        next_day = str(next_day)
    curr_date = curr_date[:2] + next_day + start_date[4:]
    open, close = dc.get_hist_data(stock, curr_date)
    return curr_sequence, close

def get_x_y(stock, start_date):
    x = []
    y = []
    window_length = 3
    for _ in range(5):
        hold = create_sequence(stock, start_date, window_length)
        x.append(hold[0])
        y.append(hold[1])
    return x, y
