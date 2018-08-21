import pandas as pd
import json

#Basic Wrapper Class
class Tweet:
    def __init__(self, text, retweets, stocktwits = False, sent = None):
        self.retweets = retweets
        self.text = text
        self.stocktwits = True
        self.sentiment = None

def get_json(stock):
    from tweepy import OAuthHandler
    from tweepy import StreamListener
    from tweepy import Stream

    #Delete before every commit.
    consumer_key =  'YOUR-KEY-HERE'
    consumer_secret = 'YOUR-SECRET-HERE'
    access_token = 'YOUR-TOKEN-HERE'
    access_secret = 'YOUR-SECRET-HERE'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    class MyListener(StreamListener):
        def on_data(self, data):
            with open(str(stock)+'_7-7-18.json', 'a') as f:
                try:
                    f.write(data)
                except BaseException:
                    print('sorry')

    st = Stream(auth = auth, listener = MyListener())
    st.filter(track = ['$'+str(stock).upper()])

def get_str(lst):
    out_str = ''
    for str in lst:
        out_str += str + ' '
    return out_str

def get_tweets(stock, date):
    with open('data/tweets_json/' +str(stock)+'_'+str(date)+'.json') as f:
        #Things to keep track of:
            #If the tweet is a retweet. If so, concatenate text with text of retweeted tweet
            #Retweet count of tweet
        tweet_lst = f.readlines()
        out_lst = []
        for t in tweet_lst:
            try:
                tweet = json.loads(t)
            except Exception:
                continue
            small_text = tweet['text']
            tot_text = ''
            if small_text[:2] == 'RT':
                try:
                    if 'extended_tweet' in tweet['retweeted_status'].keys():
                        tot_text = tweet['retweeted_status']['extended_tweet']['full_text']
                    else:
                        tot_text = tweet['retweeted_status']['text']
                except KeyError:
                    continue
            else:
                if 'extended_tweet' in tweet.keys():
                    tot_text = tweet['extended_tweet']['full_text']
                else:
                    tot_text = tweet['text']
            retweet_count = tweet['retweet_count']

            #Basic 'spam' classifier and string modifier. If 'FREE' is in the tweet, chances are the tweet is a
            #commercial promotion rather than a tweet about the stock's information
            filter = False

            lst = tot_text.split()
            for i in range(len(lst)):
                word = lst[i]
                #Spam
                if word == 'FREE' or word.lower() == 'trial':
                    filter = True
                    break
                if 'REAL TIME TRADE ALERTS' in tot_text.split():
                    filter = True
                    break
                if 'sign up' in tot_text.lower():
                    filter = True
                    break
                #String modifier. Necessary since the words below have stock-specific meaning
                if word.lower() == 'bullish':
                    lst[i] = 'amazing'
                if word.lower() == 'bearish':
                    lst[i] = 'awful'
                if word.lower() == 'bulls' or word.lower() == 'bull':
                    lst[i] = 'praise' + word.lower()[4:]
                if word.lower() == 'bears' or word.lower() == 'bear':
                    lst[i] = 'negate' + word.lower()[4:]
                if 'https://' in word.lower() or 'http://' in word.lower():
                    lst[i] = ','
            tot_text = get_str(lst)
            a = Tweet(tot_text, retweet_count)
            if not filter:
                out_lst.append(a)
        return out_lst

def get_stocktwits(stock, date):
    twts = []
    with open('data/stocktwits_json/stocktwits_'+date+'.json') as f:
        for obj in f.readlines():
            b = True
            while b:
                try:
                    a = json.loads(obj)
                    twts.append(Tweet(a['body'], 0, stocktwits = True, sent = a['entities']['sentiment']))
                    b = False
                except json.decoder.JSONDecodeError as j:
                    s = str(j)
                    #print(s)
                    i = int(s[len(s) - 5 : len(s) - 1])
                    a = json.loads(obj[:i])
                    #Text Editor
                    tot_text = a['body']
                    lst = tot_text.split()
                    for i1 in range(len(lst)):
                        word = lst[i1]
                        if word.lower() == 'bullish':
                            lst[i1] = 'amazing'
                        if word.lower() == 'bearish':
                            lst[i1] = 'awful'
                        if word.lower() == 'bulls' or word.lower() == 'bull':
                            lst[i1] = 'praise' + word.lower()[4:]
                        if word.lower() == 'bears' or word.lower() == 'bear':
                            lst[i1] = 'negate' + word.lower()[4:]
                    tot_text = get_str(lst)
                    twts.append(Tweet(tot_text, 0, stocktwits = True, sent = a['entities']['sentiment']))
                    obj = obj[i:]
    t = []
    #Basic Spam Filterer
    for twit in twts:
        txt = twit.text
        if not('FREE' in txt or 'trial' in txt.lower() or 'sign up' in txt.lower()):
            t.append(twit)
    return t
    #String modifier. Necessary since the words below have stock-specific meaning


def get_hist_data(stock, date):
    data = pd.read_csv('data/HistoricalStockData/' + str(stock) + '.csv')
    ind = 0
    for d in data['Date']:
        a = d.split('-')
        d = str(int(a[1])) + '-' + str(int(a[2])) + '-18'
        if d == date:
            break
        ind += 1
    open = data['Open'][ind]
    close = data['Close'][ind]
    return open, close
