#converting the Twitter json dump in MongoDB to CSV using PyMongo
from pymongo import MongoClient
from operator import itemgetter
import csv
import os

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']

if os.path.exists('usa_tweets.csv'):
    os.remove('usa_tweets.csv')
with open('usa_tweets.csv', 'w') as outfile:
  field_names = ['text', 'user', 'created_at', 'geo','location']
  writer = csv.DictWriter(outfile, delimiter=',', fieldnames=field_names)
  writer.writeheader()

  # tweets_iterator = collection.find().limit(1)
  # for data in tweets_iterator:
  #   print(data['user']['location'])

  for data in db.usa_tweets_collection.find():
    writer.writerow({
      'text': data['text'],
      'user': data['user'],
      'created_at': data['created_at'],
      'geo': data['geo']['coordinates'],
      'location' : data['user']['location']
    })

  outfile.close()