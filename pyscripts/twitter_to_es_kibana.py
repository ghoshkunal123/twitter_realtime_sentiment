'''
Created on September 25, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to stream data from twitter stream API to Elastic Search
On 10/09/2018 created the first version
'''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweet_util import get_tweet
from config import *
import json
import boto3
import botocore
from elasticsearch import Elasticsearch, RequestsHttpConnection, ElasticsearchException
from requests_aws4auth import AWS4Auth
import requests
import json
from datetime import *


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        #print(get_tweet(all_data))
        #print(type(get_tweet(all_data)))
        # Send to elastic search
        try:
            credentials = boto3.Session().get_credentials()
        except botocore.exceptions.ClientError as e:
            print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))

        try:
            awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es',
                               session_token=credentials.token)
            es = Elasticsearch(hosts=[{'host': eshost, 'port': 443}], http_auth=awsauth, use_ssl=True,
                               verify_certs=True, connection_class=RequestsHttpConnection)
            print('Passes index connection')
        except ElasticsearchException as es1:
            print('Error: Cannot connect to Elastic Search.')

        if not (es.indices.exists(index=es_index, ignore=[400, 404])):
            try:
                es.indices.create(index=es_index, ignore=[400, 404])
                #print('Passes index creation')
            except ElasticsearchException as es2:
                print('Failed to create index.')

        try:
            es.index(index=es_index, doc_type=es_index_doc_type, body=get_tweet(all_data))
        except ElasticsearchException as es2:
            print('Failed posting to index.')
            print(str(es2))
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
