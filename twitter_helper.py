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


# +
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer 

_stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
_lematizer = WordNetLemmatizer()

def processTweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = word_tokenize(tweet)
    tweet = [_lematizer.lemmatize(word) for word in tweet]
    tweet_words = [word for word in tweet if word not in _stopwords]
    return ' '.join(map(str, tweet_words))
