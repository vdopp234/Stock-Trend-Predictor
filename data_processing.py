#Data Analysis Imports
import numpy as np
import sentiment_analysis as sa
import data_collection as dc
import pandas as pd
#ML Imports
import sentiment_analysis as sa

def get_next_date(curr_date):
    thirtyone = ['1', '3', '5', '7', '8', '10', '12']
    thirty = [str(i) for i in range(1, 13) if str(i) not in thirtyone and i != 2]
    other = ['2']
    date = curr_date.split('-')
    if (date[0] in thirtyone and date[1] == '31') or (date[0] in thirty and date[1] == '30') or (date[0] in other and date[1] == '28'):
        return str(int(date[0]) + 1)+'-1-18'
    else:
        return date[0]+'-'+str(int(date[1]) + 1)+'-18'

def get_prev_date(curr_date):
    num_of_days = {1: 31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    date = curr_date.split('-')
    if date[1] == '1':
        return str(int(date[0]) - 1) + '-' + str(num_of_days[int(date[0]) - 1]) + '-18'
    else:
        return date[0] + '-' + str(int(date[1]) - 1) + '-18'

def get_sma(start_date, stock, num_of_days = 10):
    path = 'data/HistoricalStockData/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['Date']
    start_index = 0
    for i in range(len(dates)):
        d = dates[i]
        a = d.split('-')
        d = str(int(a[1])) + '-' + str(int(a[2])) + '-18'
        if d == start_date:
            start_index = i
            break
    print(start_index)
    print(i)
    close_prices = data['Close']
    return sum(close_prices[(start_index - num_of_days + 1):start_index+1])/num_of_days

def get_ema(start_date, stock, past_emas = {}, num_of_days = 10):
    path = 'data/HistoricalStockData/'+stock+'.csv'
    data = pd.read_csv(path)
    dates = data['Date']
    start_index = 0
    for i in range(len(dates)):
        d = dates[i]
        a = d.split('-')
        d = str(int(a[1])) + '-' + str(int(a[2])) + '-18'
        if d == start_date:
            start_index = i
            break
    close_prices = data['Close']
    multiplier = 2/(num_of_days + 1)
    if not past_emas:
        sma = get_sma(get_prev_date(start_date), stock, num_of_days = num_of_days)
        next = (close_prices[start_index] - sma)*multiplier + sma
        print(next)
        past_emas = {0:next}
        return next, past_emas
    else:
        past_day = max(past_emas.keys())
        past = past_emas[past_day]
        print(past)
        next = (close_prices[start_index] - past)*multiplier + past
        print(close_prices[start_index])
        past_emas[past_day+1] = next
        return next, past_emas

def f_vec(stock, date, past_emas = None):
    print(date)
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
