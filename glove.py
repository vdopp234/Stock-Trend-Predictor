from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

def training_data(captions_lst):
    tok = Tokenizer()
    #captions_lst = list(captions.values())
    tok.fit_on_texts(captions_lst)
    return tok

#Word to embedding array. Will be very slow, but okay because it is a one time cost
def load_glove_embeddings(tweets):
    caption_tok = training_data(tweets)
    embeddings_index = {}
    count = 0
    with open('data/glove.6B/glove.6B.100d.txt') as f:
        try:
            while True:
                try:
                    line = next(f)
                    values = line.split(' ')
                    word = values[0]
                    coefs = np.asarray(values[1:], dtype='float32')
                    embeddings_index[word] = coefs
                except UnicodeDecodeError:
                    intellect = 1
        except StopIteration:
            #print(len(caption_tok.word_index.items()))
            max = 0
            embedding_matrix = np.zeros((700000, 100)) #100 because we are importing 100d glove
            for word, i in caption_tok.word_index.items():
                embedding_vector = embeddings_index.get(word)
                if embedding_vector is not None and len(embedding_vector) == 100:
                    embedding_matrix[i] = embedding_vector
                    if i > max:
                        max = i
                else:
                    asdf = 'adf'
            print(max)
            return embedding_matrix, caption_tok

    #Matrix of embeddings for each word in captions
