#preprocessing Imports
import os
import csv
import glove
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
#NN Imports
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Embedding, Dropout, Conv1D, Flatten, LSTM


def get_num(str):
    for char in str:
        try:
            a = int(char)
            return a
        except Exception:
            continue

def get_str(str_lst):
    start = ''
    for str in str_lst:
        start += (str + ' ')
    return start[1:len(start) - 1]

def get_data():
    x = []
    y = []
    p = 'data/aclImdb/train/pos'
    files = os.listdir(path = p)
    for file in files:
        try:
            with open(p+'/' + file) as f:
                x_init = f.read().split('<br /><br />')
                x.append(get_str(x_init))
                y.append(1)
        except UnicodeDecodeError:
            continue
    p = 'data/aclImdb/train/neg'
    files = os.listdir(path = p)
    for file in files:
        try:
            with open(p+'/' + file) as f:
                x_init = f.read().split('<br /><br />')
                x.append(get_str(x_init))
                y.append(0)
        except UnicodeDecodeError:
            continue
    p = 'data/aclImdb/test/pos'
    files = os.listdir(path = p)
    for file in files:
        try:
            with open(p+'/' + file) as f:
                x_init = f.read().split('<br /><br />')
                x.append(get_str(x_init))
                y.append(1)
        except UnicodeDecodeError:
            continue
    p = 'data/aclImdb/test/neg'
    files = os.listdir(path = p)
    for file in files:
        try:
            with open(p+'/' + file) as f:
                x_init = f.read().split('<br /><br />')
                x.append(get_str(x_init))
                y.append(0)
        except UnicodeDecodeError:
            continue

    p = 'data/sentiment labelled sentences'
    files = [file for file in os.listdir(path = p) if file != 'readme.txt']
    for file in files:
        with open(p+'/'+file) as f:
            for line in f.readlines():
                b = line.split('\t')
                c = b[1].split('\n')
                a = int(c[0])
                if a == 0:
                    x.append(b[0])
                    y.append(int(c[0]))
                elif a == 1:
                    x.append(b[0])
                    y.append(1)
    return x, y

def tokenize(x, y, tok):
    max_len = 100
    #print(x)
    new_x = tok.texts_to_sequences(x)
    #print(new_x)
    new_x = pad_sequences(new_x, max_len, padding = 'post')
    #print(new_x)
    new_y = pd.get_dummies(y)
    return new_x, np.array(new_y)

def tokenize_x(x, tok):
    max_len = 100
    new_x = tok.texts_to_sequences(x)
    new_x = pad_sequences(new_x, max_len, padding = 'post')
    return new_x

def get_model():
    vocab_size = 700000
    sentence_length = 100
    x, y = get_data()
    # types = []
    # for a in y:
    #     if a not in types:
    #         types.append(a)
    #
    # print(types)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)
    embeddings, tok = glove.load_glove_embeddings(x)
    print("Loaded GloVe embeddings")
    x_train, y_train = tokenize(x_train, y_train, tok)
    x_test, y_test = tokenize(x_test, y_test, tok)

    #Use convolution because studies have shown it to be an effective technique for sentiment analysis.
    model = Sequential()
    model.add(Embedding(vocab_size, output_dim = 100, input_length = sentence_length, weights = [embeddings], trainable = False))
    model.add(LSTM(64, return_sequences = True))
    model.add(LSTM(16, return_sequences = True))
    model.add(Flatten())
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(2, activation = 'sigmoid'))

    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    model.fit(x = x_train, y = y_train, batch_size = 10, epochs = 2)

    p = model.evaluate(x = x_test, y = y_test, batch_size = 1)
    print(model.metrics_names)
    print(p)
    # x = model.predict(tokenize_x(['great gains while avoiding the drop things are so good for use I could not be any happier'], tok))
    # print(x)
    model_json = model.to_json()
    with open('saved_models/sentiment.json', 'w') as f:
        f.write(model_json)
    model.save_weights('saved_models/sentiment.h5')

    with open('saved_models/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tok, handle, protocol = pickle.HIGHEST_PROTOCOL)

    return model, tok

def load_model():
    model = open('saved_models/sentiment.json')
    loaded_model = model.read()
    model.close()
    loaded_model = model_from_json(loaded_model)
    loaded_model.load_weights('saved_models/sentiment.h5')

    tokenizer = None
    with open('saved_models/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return loaded_model, tokenizer

def predict(text, model, tok):
    return model.predict(tokenize_x([text], tok))
