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

#
import json
import tweepy
import re
import textblob as tb
import numpy as np
import yfinance as yf
#
# +
#
config_file = '.config.json'
with open(config_file) as fh:
    config = json.load(fh)

auth = tweepy.AppAuthHandler(
    config['consumer_key'], config['consumer_secret']
)
twitter_api = tweepy.API(auth)

# +


def analyze(input_text, _analyzer=tb.en.sentiments.NaiveBayesAnalyzer()):
    blob = tb.TextBlob(input_text, analyzer=_analyzer)
    for sentence in blob.sentences:
        sentiment = sentence.sentiment
        print(sentence)
        print(sentiment)


def prepare_input(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z])|(\w+:\/\/\S+)", " ", tweet).split())


# -
for status in tweepy.Cursor(
    twitter_api.user_timeline,
    screen_name='elonmusk',
).items(5):

    text = status._json['text']
    print(status.created_at)
    print(text)
    text = prepare_input(text)
    analyze(text)


# +
# TODO: train data
