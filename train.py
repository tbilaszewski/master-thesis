import csv
import pickle

# +
from twitter_helper import processTweet

train_data_tweets = []
train_data_classification = []

sentiment_dict = {
    '0': 'negative',
    '2': 'neutral',
    '4': 'positive'
}

with open('tweets_data.csv', newline='', encoding='latin-1') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csv_reader:
        classification = sentiment_dict[row[0]]
        text = row[5]
        train_data_tweets.append(processTweet(text))
        train_data_classification.append(classification)

# +
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

pipeline = Pipeline([
    ('bow',CountVectorizer()), 
    ('tfidf', TfidfTransformer()), 
    ('classifier', MultinomialNB()),
])

# +
from sklearn.model_selection import train_test_split

tweets_train, tweets_test, sentiments_train, sentiments_test = train_test_split(train_data_tweets, train_data_classification, test_size=0.2)


# +
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

pipeline.fit(tweets_train, sentiments_train)
predictions = pipeline.predict(tweets_test)
print(classification_report(predictions,sentiments_test))
print(confusion_matrix(predictions,sentiments_test))
print(accuracy_score(predictions,sentiments_test))

# -

predictions


with open('classifier_trained.pkl', 'wb') as fid:
    pickle.dump(pipeline, fid) 




