'''
Created on October 16, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to delete the elastic search at the beginning of each day
On 10/16/2018 created the first version
Create a crontab entry
'''

from config import *
import boto3
import botocore
from elasticsearch import Elasticsearch, RequestsHttpConnection, ElasticsearchException
from requests_aws4auth import AWS4Auth
import requests
from datetime import *


try:
    credentials = boto3.Session().get_credentials()
except botocore.exceptions.ClientError as e:
    print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))

try:
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es',
            session_token=credentials.token)
    es = Elasticsearch(hosts=[{'host': eshost, 'port': 443}], http_auth=awsauth, use_ssl=True,
            verify_certs=True, connection_class=RequestsHttpConnection, timeout=30, max_retries=10, retry_on_timeout=True)
except ElasticsearchException as es1:
    print('Error: Cannot connect to Elastic Search.')

if (es.indices.exists(index=es_index, ignore=[400, 404])):
    try:
        es.indices.delete(index=es_index, ignore=[400, 404])
        #print('Passes index deletion')
    except ElasticsearchException as es2:
        print('Failed to delete index.')