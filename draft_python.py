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
import json, tweepy
import re 

config_file = '.config.json'
with open(config_file) as fh:
    config = json.load(fh)

auth = tweepy.AppAuthHandler(
    config['consumer_key'], config['consumer_secret']
)

api = tweepy.API(auth)


# +
all_tweets = api.user_timeline(screen_name='SpaceX', 
                           # 200 is the maximum allowed count
                           count=10,
                           include_rts = True,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                          )
print_info(all_tweets)

def print_info(tweets):
    for info in tweets:
         print("ID: {}".format(info.id))
         print(info.created_at)
         dir(info.retweets)
         print(info.text),
         print(clean_tweet(info.text))
         print("\n")
                        
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
# +

list = [1,23,3]

# -


