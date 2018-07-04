from twitter import *
import pandas as pd
import json

#Info for personal twitter app. Delete before every commit

class Tweet:
    def __init__(self, text, retweets):
        self.retweets = retweets
        self.text = text

def get_json(stock):
    from tweepy import OAuthHandler
    from tweepy import StreamListener
    from tweepy import Stream

    consumer_key = 'YOUR--KEY--HERE'
    consumer_secret = 'YOUR--SECRET--HERE'
    access_token = 'YOUR--TOKEN--HERE'
    access_secret = 'YOUR--SECRET--HERE'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    class MyListener(StreamListener):
        def on_data(self, data):
            with open(str(stock)+'_7-4-18.json', 'a') as f:
                try:
                    f.write(data)
                except BaseException:
                    print('sorry')

    st = Stream(auth = auth, listener = MyListener())
    st.filter(track = ['$'+str(stock).upper()])

def get_str(lst):
    out_str = ''
    for str in lst:
        out_str += str
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
                if 'extended_tweet' in tweet['retweeted_status'].keys():
                    tot_text = tweet['retweeted_status']['extended_tweet']['full_text']
                else:
                    tot_text = tweet['retweeted_status']['text']
            else:
                if 'extended_tweet' in tweet.keys():
                    tot_text = tweet['extended_tweet']['full_text']
                else:
                    tot_text = tweet['text']
            retweet_count = tweet['retweet_count']

            #Basic 'spam' classifier and string modifier. If 'FREE' is in the tweet, chances are the tweet is a
            #commercial promotion rather than a tweet about the stock's information
            contains_free = False
            for i in range(len(tot_text.split())):
                word = tot_text.split()[i]
                if word == 'FREE':
                    contains_false = True
                if word.lower() == 'bullish':
                    tot_text = get_str(tot_text.split()[:i]) + 'amazing' + get_str(tot_text.split()[i+1:])
                if word.lower() == 'bearish':
                    tot_text = get_str(tot_text.split()[:i]) + 'awful' + get_str(tot_text.split()[i+1:])
            a = Tweet(tot_text, retweet_count)
            if not contains_free:
                out_lst.append(a)
        return out_lst

def get_hist_data(stock, date):
    data = pd.read_csv('data/' + str(stock) + '.csv')
    ind = 0
    for d in data['date']:
        if d == date:
            break
        ind += 1
    open = data['open'][ind]
    close = data['close'][ind]
    return open, close
