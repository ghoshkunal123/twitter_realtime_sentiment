'''
Created on September 25, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to TBD
On 09/25/2018 created the first version
'''
import re
from textblob import TextBlob
from datetime import *


class Sentiments:
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    CONFUSED = 'Confused'


#id_field = 'id_str'
emoticons = {
    Sentiments.POSITIVE: '😀|😁|😂|😃|😄|😅|😆|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😜|😝|😸|😹|😺|😻|😼|😽',
    Sentiments.NEGATIVE: '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😾|😿|😰|😱|🙀',
    Sentiments.NEUTRAL: '😐|😑|😳|😮|😯|😶|😴|😵|😲',
    Sentiments.CONFUSED: '😕'
    }


def _sentiment_analysis(tweet):
    tweet['emoticons'] = []
    tweet['sentiments'] = []
    _sentiment_analysis_by_emoticons(tweet)
    if len(tweet['sentiments']) == 0:
        _sentiment_analysis_by_text(tweet)


def _sentiment_analysis_by_emoticons(tweet):
    for sentiment, emoticons_icons in emoticons.items():
        #matched_emoticons = re.findall(emoticons_icons, tweet['text'].encode('utf-8'))
        matched_emoticons = re.findall(emoticons_icons, tweet['text'])
        if len(matched_emoticons) > 0:
            tweet['emoticons'].extend(matched_emoticons)
            tweet['sentiments'].append(sentiment)

    if Sentiments.POSITIVE in tweet['sentiments'] and Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.CONFUSED
    elif Sentiments.POSITIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.POSITIVE
    elif Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.NEGATIVE
    elif Sentiments.NEUTRAL in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.NEUTRAL


def _sentiment_analysis_by_text(tweet):
    #blob = TextBlob(tweet['text'].decode('ascii', errors="replace"))
    blob = TextBlob(tweet['text'])
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity < 0:
        sentiment = Sentiments.NEGATIVE
    elif sentiment_polarity <= 0.2:
        sentiment = Sentiments.NEUTRAL
    else:
        sentiment = Sentiments.POSITIVE
    tweet['sentiments'] = sentiment


def get_tweet(doc):
    tweet=doc
    #tweet[id_field] = doc[id_field]
    #tweet['hashtags'] = map(lambda x: x['text'], doc['entities']['hashtags'])
    #tweet['coordinates'] = doc['coordinates']
    #tweet['timestamp_ms'] = doc['timestamp_ms']
    #tweet['text'] = doc['text']
    #tweet['user'] = {'id': doc['user']['id'], 'name': doc['user']['name']}
    #tweet['mentions'] = re.findall(r'@\w*', doc['text'])
    _sentiment_analysis(tweet)
    return tweet

def get_tweet_curated(doc):
    tweet={}
    tweet['id'] = doc['id']
    tweet['source'] = ''.join(re.findall('>([\S+\s]+)</a>', doc['source']))
    tweet['user'] = {'user_id': doc['user']['id'], 'user_name': doc['user']['name'], 'user_screen_name': doc['user']['screen_name'], 'user_location': doc['user']['location'], 'user_description': doc['user']['description'], 'user_followers_count': doc['user']['followers_count'], 'user_friends_count': doc['user']['friends_count'], 'user_listed_count': doc['user']['listed_count'], 'user_favourites_count': doc['user']['favourites_count'], 'user_statuses_count': doc['user']['statuses_count']}
    tweet['hashtags'] = list(map(lambda x: x['text'], doc['entities']['hashtags']))
    tweet['timestamp_ms'] = datetime.fromtimestamp(int(doc['timestamp_ms']) / 1000.0)
    tweet['created_timestamp_ms'] = datetime.now()
    tweet['mentions'] = re.findall(r'@\w*', doc['text'])
    tweet['text'] = doc['text']
    _sentiment_analysis(tweet)
    return tweet
