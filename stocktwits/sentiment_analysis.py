from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.models import Sequential

def m(xtrain, ytrain):
    max_tweet_length = 50 #Approximation for words given max char length is 140
    glove_embeddings = get_embeddings(stock)


    model = Sequential()
    model.add(Embedding(vocab_size, output_dim = 150, input_length = max_tweet_length, weights = [glove_embeddings], trainable = False)
    model.add(Flatten())
    model.add(Dense(100, activation = 'relu'))
    model.add(Dense(50, activation = 'relu'))
    model.add(Dense(25, activation = 'relu'))
    model.add(Dense(3, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    #Mess with epochs/batch_size as necessary
    model.fit(xtrain, ytrain, epochs = 10, batch_size = 1, verbose = 1)
    return model
