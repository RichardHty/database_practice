from pymongo import MongoClient
from textblob import TextBlob
import re

def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

if __name__ == "__main__":
    # calling main function
    client = MongoClient('localhost', 27017)
    db = client['twitterdb']
    collection = db['twitter_search']
    tweets_iterator = collection.find({"text": {"$regex": "/.*data.*/", "$options": "i"}})

    count_total = 0
    count_geo = 0
    for tweet in tweets_iterator:
        count_total+=1

        print(get_tweet_sentiment(tweet['text'])+" sentiment for the tweet: "+tweet['text'])
        if tweet['user']['geo_enabled']:
            count_geo+=1

    print("\nThe number of tweets that have 'data' somewhere in the tweet’s text(case insensitive): "+str(count_total)+"\n")
    print(str(count_geo)+" of them are geo_enabled.")

