#Data Analysis Imports
import numpy as np
import sentiment_analysis as sa
import data_collection as dc
import pandas as pd
#ML Imports
import sentiment_analysis as sa



def get_sma(start_date, stock, num_of_days = 10):
    path = 'data/HistoricalStockData/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['date']
    start_index = 0
    # print(len(dates))
    for i in range(len(dates)):
        d = dates[i]
        a = d.split('/')
        d = str(int(a[1])) + '-' + str(int(a[2])) + '-' + str(a[0][2:])
        if d == start_date:
            start_index = i
            break
    # print(start_index)
    close_prices = data['close']
    out = sum(close_prices[(start_index - num_of_days + 1):start_index+1])/num_of_days
    if int(out) == 0:
        return get_sma(dc.get_prev_date(start_date), 'googl')
    return out

def get_ema(start_date, stock, past_emas = {}, num_of_days = 10):
    path = 'data/HistoricalStockData/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['date']
    start_index = 0
    for i in range(len(dates)):
        d = dates[i]
        # print(d)
        a = d.split('/')
        d = str(int(a[1])) + '-' + str(int(a[2])) + '-18'
        if d == start_date:
            start_index = i
            break
    close_prices = data['close']
    multiplier = 2/(num_of_days + 1)
    if not past_emas:
        sma = get_sma(dc.get_prev_date(start_date), stock, num_of_days = num_of_days)
        next = (close_prices[start_index] - sma)*multiplier + sma
        # print(next)
        past_emas = {0:next}
        return next, past_emas
    else:
        past_day = max(past_emas.keys())
        past = past_emas[past_day]
        # print(past)
        next = (close_prices[start_index] - past)*multiplier + past
        # print(close_prices[start_index])
        past_emas[past_day+1] = next
        return next, past_emas

def f_vec(stock, date, past_emas = None):
    # print(date)
    tweets = dc.get_tweets(stock, date)
    sentiment_model, tok = sa.load_model()
    volume = len(tweets)
    sent = np.array([[0 ,0]], dtype = np.float64)
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
    return np.hstack([np.array([[close/1000, retweets, sma/1000, ema[0]/1000]]), sent]).T
