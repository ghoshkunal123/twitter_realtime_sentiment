'''
Created on September 25, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to stream data from twitter stream API to s3
On 09/25/2018 created the first version
'''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweet_util import get_tweet
from config import *
import json
import boto3
import botocore
import datetime
import os
import uuid
import datetime


class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        bucekt_prefix_add = datetime.datetime.strftime(datetime.datetime.now(), 'dt=%Y-%m-%d')
        filename = str(uuid.uuid4()) + '_' + datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S%f') + '.json'
        #print(get_tweet(all_data))
        # Send to s3
        try:
            s3 = boto3.resource('s3', region)
            object = s3.Object(bucket_name,os.path.join(bucekt_prefix,bucekt_prefix_add,filename))
            object.put(Body=json.dumps(get_tweet(all_data)))
        except botocore.exceptions.ClientError as e:
            print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))
        return(True)

    def on_timeout(self):
        print('Timeout.......')
        return(True) # Continue listening

    def on_error(self, status):
        print(status)
        return(True)  # Continue Listening


auth=OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=track)