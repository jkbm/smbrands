# -*- coding: utf-8 -*-
import json
import re
import os
from .models import Dataset
def get_data(dataset=71):
    cwd = os.getcwd()
    try:
        ds = Dataset.objects.get(pk=dataset)
        fn = ds.filename
        data = json.load(cwd+open('/projects/twitter/static/' + fn +'.json', 'r'))
    except:
        fn = "Falcon Heavy_07022018_1936"
        data = json.load(cwd+open('/projects/twitter/static/' + fn +'.json', 'r'))
    
    

    tweets = []
    print(len(data['statuses']))
    for t in data['statuses']:
        text = re.sub(r"[^a-zA-Z0-9]+", ' ', t['text'])
        tweets.append(text)

    return tweets

def popularWords(tweets):
    cwd = os.getcwd()
    string = ""
    for x in tweets:
        string += str(x)

    words = string.split()
    worddict = {'a': 0}

    import operator
    from itertools import islice

    def wordsplit(text):
        for word in words:
            if word.lower() in worddict:
                worddict[word.lower()] = worddict[word.lower()] + 1
            else:
                worddict[word.lower()] = 1


    wordsplit(words)


    sortdict =  sorted(worddict.items(), key=operator.itemgetter(1), reverse=True)



    cleanword = {}
    for word in worddict:
        if '\\' not in word.lower() and '@' not in word.lower() and '&' not in word.lower():
            if '#' not in word.lower():
                cleanword[word] = worddict[word]

    sortdict =  sorted(cleanword.items(), key=operator.itemgetter(1), reverse=True)
    print([x for x in sortdict if len(x[0])>4 and x[1] > 20])
    print('')
    sortdict=[x for x in sortdict if len(x[0])>4 and x[1] > 20]
    top =  dict(islice(sortdict, 10))

    names = list(sorted(top, key=top.get))
    nums = list(sorted(top.values()))
    print(names)
    print(nums)

    top_dict = {}
    for n in range(0, len(names)):
        top_dict[names[n]] =  nums[n]
    print(top_dict)
    for item in top_dict:
        print(item + ":" + str(top_dict[item]))
    with open(cwd+ "/projects/twitter/static/analysis_data.json", "w") as jsonFile:
            jsonFile.write(json.dumps(top_dict))

def wordFreq(dataset):
    tweets = get_data(dataset)
    popularWords(tweets)

if __name__ == '__main__':

    tweets = get_data(71)
    popularWords(tweets)