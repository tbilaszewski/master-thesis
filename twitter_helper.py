#
import json
import tweepy
import re
import textblob as tb
import pandas as pd
#

class TweetTimeLineHelper:
  def __init__(self, name='elonmusk', items=5):
    config_file = '.config.json'
    with open(config_file) as fh:
        config = json.load(fh)

    auth = tweepy.AppAuthHandler(
        config['consumer_key'], config['consumer_secret']
    )
    self.twitter_api = tweepy.API(auth)
    self.timeLineName = name
    self.items = items
    self.tweets = {
      'created_at': [],
      'text': [],
      'retweet_count': [],
      'favorite_count': [],
      'retweeted': [],
    }
      
  def saveToCsv(self, fileName='tweets.csv'):
    self.forEach(self.__appendTweet)
    pd.DataFrame.from_dict(self.tweets).to_csv(fileName, mode='w+')
    
  def __appendTweet(self, status):
    self.tweets['created_at'].append(status.created_at)
    self.tweets['text'].append(status.text)
    self.tweets['retweet_count'].append(status.retweet_count)
    self.tweets['favorite_count'].append(status.favorite_count)
    self.tweets['retweeted'].append(status.retweeted)

  def forEach(self, func=print, clean=True):
      for status in tweepy.Cursor(
        self.twitter_api.user_timeline,
        screen_name=self.timeLineName,
      ).items(self.items):
        func(status)


def cleanTweet(input):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z])|(\w+:\/\/\S+)", " ", input).split())

def analyze(input_text, analyzer=tb.en.sentiments.NaiveBayesAnalyzer()):
  sentiment = tb.TextBlob(input_text, analyzer=analyzer).sentiment
  return [sentiment.classification, getattr(sentiment,'p_{}'.format(sentiment.classification))]