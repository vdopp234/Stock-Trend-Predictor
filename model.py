#Preprocessing Imports
import data_collection as dc
import data_processing as dp
import numpy as np
#NN imports
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM, Dropout, Flatten



def create_sequence(stock, start_date, window_size):
    curr_date = start_date
    curr_sequence = ''
    try:
        curr_sequence = dp.f_vec(stock, curr_date).T
    except KeyError:
        try:
            curr_date = dc.get_next_date(curr_date)
            curr_sequence = dp.f_vec(stock, curr_date).T
        except KeyError:
            curr_date = dc.get_next_date(curr_date)
            curr_sequence = dp.f_vec(stock, curr_date).T
    for _ in range(window_size - 1):
        #print(curr_date)
        curr_date = dc.get_next_date(curr_date)
        print(curr_date)
        try:
            new_vec = dp.f_vec(stock, curr_date).T
        except KeyError:
            try:
                curr_date = dc.get_next_date(curr_date)
                print(curr_date)
                new_vec = dp.f_vec(stock, curr_date).T
            except KeyError:
                curr_date = dc.get_next_date(curr_date)
                print(curr_date)
                new_vec = dp.f_vec(stock, curr_date).T
        curr_sequence = np.vstack((curr_sequence, new_vec))
    curr_date = dc.get_next_date(curr_date)
    #print(curr_date)
    open, close = dc.get_hist_data(stock, curr_date)
    return curr_sequence, close/1000

def get_x_y(stock, start_date):
    x = []
    y = []
    window_length = 3
    num_of_training_examples = 10
    curr_date = start_date
    for _ in range(num_of_training_examples):
        hold = create_sequence(stock, curr_date, window_length)
        x.append(hold[0])
        y.append(hold[1])
        curr_date = dc.get_next_date(curr_date)
    return x, y

def get_model(x, y):
    model = Sequential()
    model.add(LSTM(16, input_shape = (3, 6), return_sequences = True))
    model.add(LSTM(8, return_sequences = True))
    model.add(Flatten())
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(1, activation = 'relu')) #NOT sigmoid or softmax because this is a linear regression problem

    model.compile(loss = 'mse', optimizer = 'adam', metrics = ['accuracy'])
    model.fit(x, y, batch_size = 1, epochs = 10)

    model_json = model.to_json()
    with open('saved_models/main_model.json', 'w') as f:
        f.write(model_json)
    model.save_weights('saved_models/main_model.h5')
    return model

def load_model():
    model = open('saved_models/main_model.json')
    loaded_model = model.read()
    model.close()
    loaded_model = model_from_json(loaded_model)
    loaded_model.load_weights('saved_models/main_model.h5')
    return loaded_model
