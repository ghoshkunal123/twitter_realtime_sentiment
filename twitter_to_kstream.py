'''
Created on September 28, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to stream data from twitter stream API to kinesis stream
On 09/28/2018 created the first version
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
        #print(get_tweet(all_data))
        # Send to kinesis stream
        try:
            kinesis = boto3.client('kinesis','us-east-1')
            kinesis_shard=kinesis.describe_stream(StreamName=kinesis_stream)['StreamDescription']['Shards'][0]['ShardId']
            kinesis.put_record(StreamName=kinesis_stream, Data=json.dumps(get_tweet(all_data))+'\n',PartitionKey=kinesis_shard)
        except botocore.exceptions.ClientError as e:
            print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))
        return(True)

    def on_timeout(self):
        print('Timeout.......')
        return(True) # Continue listening

    def on_error(self, status):
        print(status)
        return (True)  # Continue listening

auth=OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["awscloud"])