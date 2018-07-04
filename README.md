# Stock-Trend-Predictor

This repository contains the code for a Neural Network which predicts Stock Market Prices using deep learning techniques. My model does so by monitoring the activity of a stock using the Stream API of both Twitter and StockTwits and by monitoring the activity of the stock itself by gathering relevant data from the stock's historical data. 

The features I gathered are as follows

1) The average number of retweets per tweet in a given day
2) The average sentiment of each tweet in a given day
    a) I calculated the sentiment of the text by using an LSTM recurrent network, which I trained using an IMDB Movie Review Dataset cited below. 
3) The 10-day simple moving average of the stock on a given day
4) The 10-day exponential moving average of the stock on a given day
5) The price a stock opened at on a given day
6) The price a stock closed at on a given day

The network itself is an LSTM recurrent network, similar to the model I used to predict the sentiment of the tweets. Window size, etc. are all given in the code

Note: This repo does NOT contain the data (GloVe Embeddings, IMDB Movie Reviews, etc.) I used to train my entire network, as it would take a very long time to push them to this repo. 

Citations: 
IMDB Movie Dataset -- http://ai.stanford.edu/~amaas/data/sentiment/
Glove Embeddings -- https://nlp.stanford.edu/projects/glove/
