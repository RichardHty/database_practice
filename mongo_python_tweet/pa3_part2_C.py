from pymongo import MongoClient
import pprint
import re
from bson.son import SON

def extract_state(text):
    temp = str(text).split(", ")
    if len(temp)==2 and len(temp[1])==2:
        return temp[1]
    else:
        return None


client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']
regex = '.*CA'
regexDB = re.compile(regex)

pipeline = [
    {'$match':{'place.full_name':regexDB}},
    {'$group':{'_id':'$place.name','count':{'$sum':1}}},
    {'$sort':SON([('count',-1)])}, {'$limit':5}
]

statistic_per_state = {}
tweets_iterator = collection.find()
for tweet in tweets_iterator:
    if tweet['place']:
        state_name = extract_state(tweet['place']['full_name'])
    else:
        state_name = None

    if state_name is not None and state_name:
        if state_name in statistic_per_state.keys():
            statistic_per_state[state_name]+=1
        else:
            statistic_per_state[state_name] = 1

top5forStates = []
for i in range(0, 5):
    max = 0
    max_flag = ""
    for j in statistic_per_state:
        if max < statistic_per_state[j]:
            max = statistic_per_state[j]
            max_flag = j
    if max != 0 and max_flag != "":
        variable = {}
        variable[max_flag] = max
        top5forStates.append(variable)
        statistic_per_state[max_flag] = 0

print("Top 5 states that have tweets :")
print(top5forStates)

print("Top 5 cities that tweet in the state of California:")
pprint.pprint(list(collection.aggregate(pipeline)))



