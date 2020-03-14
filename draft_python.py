# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import json
import tweepy
import re
from textblob import TextBlob
import numpy as np
import yfinance as yf
import requests
import json
# +
config_file = '.config.json'
with open(config_file) as fh:
    config = json.load(fh)

auth = tweepy.AppAuthHandler(
    config['consumer_key'], config['consumer_secret']
)
twitter_api = tweepy.API(auth)
# +
def analyze(input_text):
    text = clean_input(input_text)
    print(text)
    blob = TextBlob(text)
    print(blob.noun_phrases)
    polarityList = []
    for sentence in blob.sentences:
        polarity = sentence.sentiment.polarity
        polarityList.append(polarity)
        if len(blob.sentences) > 1:
            print("sentence_{} polarity={}".format(len(polarityList),polarity))
    print("sentence polarity_sum={}".format(np.average(polarityList)))



def print_info(tweets):
    for info in tweets:
        print("ID: {}".format(info.id))
        print(info.created_at)
        print(info.text)
        analyze(info.text)
        print("\n")

def get_stock_data():
    return

def clean_input(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z])|(\w+:\/\/\S+)", " ", tweet).split())


# -
all_tweets = twitter_api.user_timeline(screen_name='elonmusk',
                               # 200 is the maximum allowed count
                               count=10,
                               include_rts=True,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               )
# print_info(all_tweets)
# print(get_stock_data())


from alpha_vantage.timeseries import TimeSeries
import datetime

ts = TimeSeries(key=config['alpha_vantage_token'], output_format='pandas')


intraday_data, data_info = ts.get_intraday('TSLA', outputsize='full', interval='1min')
# Print the information of the data

refreshed_date = data_info['3. Last Refreshed']

print(intraday_data.to_csv("stocks_{}.csv".format(refreshed_date)))


