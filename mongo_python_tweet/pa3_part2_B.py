import emoji
from pymongo import MongoClient

def extract_emojis(text):
    return ''.join(emoji_data for emoji_data in text if emoji_data in emoji.UNICODE_EMOJI)
def extract_state(text):
    temp = str(text).split(", ")
    if len(temp)==2 and len(temp[1])==2:
        return temp[1]
    else:
        return None

if __name__ == "__main__":
    # calling main function
    client = MongoClient('localhost', 27017)
    db = client['usa_db']
    collection = db['usa_tweets_collection']
    tweets_iterator = collection.find()
    count=0

    statistic = {}
    statistic_per_state = []
    statistic_per_emoji = []
    for tweet in tweets_iterator:
        result = extract_emojis(tweet['text'])
        if tweet['place'] :
            state_name = extract_state(tweet['place']['full_name'])
        else:
            state_name = None
        if result:
            for i in result:
                if i in statistic.keys():
                    statistic[i]+=1
                else:
                    statistic[i]=1

                if state_name is not None and state_name:
                    flag_state = 0
                    flag_emoji = 0
                    for k in range(len(statistic_per_state)):
                        if statistic_per_state[k]['state_name'] == state_name:
                            if i in statistic_per_state[k].keys():
                                statistic_per_state[k][i]+=1
                            else:
                                statistic_per_state[k][i]=1
                            flag_state = 1
                            break
                    if flag_state == 0:
                        var = {}
                        var[i]=1
                        var['state_name']=state_name
                        statistic_per_state.append(var)

                    for k in range(len(statistic_per_emoji)):
                        if statistic_per_emoji[k]['emoji'] == i:
                            if state_name in statistic_per_emoji[k].keys():
                                statistic_per_emoji[k][state_name]+=1
                            else:
                                statistic_per_emoji[k][state_name]=1
                            flag_emoji = 1
                            break
                    if flag_emoji == 0:
                        var = {}
                        var[state_name]=1
                        var['emoji']=i
                        statistic_per_emoji.append(var)
    top15 = []
    for i in range(0,15):
        max = 0
        max_flag = ""
        for j in statistic:
            if max<statistic[j]:
                max = statistic[j]
                max_flag = j
        if max != 0 and max_flag != "":
            variable = {}
            variable[max_flag]=max
            top15.append(variable)
            statistic[max_flag]=0
    print("Top 15 emojis used in the entire tweets:")
    print(top15)

    top5forTree = []
    s = '🎄'
    for i in range(0, 5):
        max = 0
        max_flag = ""
        for j in range(len(statistic_per_state)):
            if s in statistic_per_state[j].keys():
                if max<statistic_per_state[j][s]:
                    max = statistic_per_state[j][s]
                    max_flag = j
        if max != 0 and max_flag != "":
            variable = {}
            variable[statistic_per_state[max_flag]['state_name']] = max
            top5forTree.append(variable)
            statistic_per_state[max_flag][s] = 0
    print("Top 5 states for the emoji 🎄 :")
    print(top5forTree)

    top5forMA = []
    s = 'MA'
    for j in range(len(statistic_per_state)):
        if s == statistic_per_state[j]['state_name']:
            for i in range(0,5):
                max = 0
                max_flag = ""
                for e in statistic_per_state[j].keys():
                    if e!= "state_name" and max<statistic_per_state[j][e]:
                        max = statistic_per_state[j][e]
                        max_flag = e
                if max != 0:
                    variable = {}
                    variable[max_flag] = max
                    top5forMA.append(variable)
                    statistic_per_state[j][max_flag] = 0
            break
    print("Top 5 emojis for MA:")
    print(top5forMA)

    top5forEmoji = []
    useEmoji = []
    for j in range(len(statistic_per_state)):
        variable = {}
        variable['state_name'] = statistic_per_state[j]['state_name']
        sum = 0
        for v in statistic_per_state[j]:
            if v != "state_name":
                sum += statistic_per_state[j][v]
        variable['sum'] = sum
        useEmoji.append(variable)

    for i in range(0, 5):
        max = 0
        max_flag = ""
        for j in range(len(useEmoji)):
            if max<useEmoji[j]['sum']:
                max = useEmoji[j]['sum']
                max_flag = j
        if max != 0 and max_flag != "":
            variable = {}
            variable[useEmoji[max_flag]['state_name']] = max
            top5forEmoji.append(variable)
            useEmoji[max_flag]['sum'] = 0
    print("Top 5 states that use emojis:")
    print(top5forEmoji)




