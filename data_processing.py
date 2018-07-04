#Data Analysis Imports
import numpy as np
import sentiment_analysis as sa
import data_collection as dc
import pandas as pd
#ML Imports
import sentiment_analysis as sa


def get_sma(start_date, stock, num_of_days = 10):
    path = 'data/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['Date']
    start_index = 0
    for i in range(len(dates)):
        if dates[i] == start_date:
            start_index = i
            break
    close_prices = data['Close']
    return sum(close_prices[(i - num_of_days + 1):i+1])/num_of_days

def get_ema(start_date, stock, past_emas = {}):
    num_of_days = 10
    path = 'data/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['Date']
    start_index = 0
    for i in range(len(dates)):
        if dates[i] == start_date:
            start_index = i
            break
    close_prices = data['Close']

    multiplier = 2/(num_of_days + 1)
    if not past_emas:
        sma = get_sma(start_date, stock, num_of_days = num_of_days)
        past_emas[0] = sma
        return sma, past_emas
    else:
        past_day = max(past_emas.keys())
        past = past_emas[past_day]
        next = (close_prices[start_index] - past)*multiplier + past
        past_emas[past_day+1] = next
        return next, past_emas

def f_vec(stock, date, past_emas = None):
    tweets = dc.get_tweets(stock, date)
    sentiment_model, tok = sa.load_model()
    volume = len(tweets)
    sent = np.array([[0],[0]])
    retweets = 0
    for tweet in tweets:
        retweets += tweet.retweets
        txt = tweet.text
        sent += sa.predict(txt, sentiment_model, tok)
    retweets /= volume
    sent /= volume
    open, close = dc.get_hist_data(stock, date)

    sma = get_sma(date, stock)
    ema = get_ema(date, stock, past_emas)
    #Measurement of tweet volume wasn't great, consider getting rid of this as a feature
    return np.hstack([np.array([[open, close, retweets, sma, ema]]), sent]).T
