from __future__ import print_function
import boto3
import base64
import botocore
import datetime
import os
import uuid

def lambda_handler(event, context):
    region = 'us-east-1'
    bucket_name='kunal-dl-stage'
    bucket_prefix='KunalAWSSentiment-awscloud'
    bucket_prefix_add = datetime.datetime.strftime(datetime.datetime.now(), 'dt=%Y-%m-%d')
    filename = str(uuid.uuid4()) + '_' + datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S%f') + '.json'
    for record in event['Records']:
    #Kinesis data is base64 encoded so decode here
        payload=base64.b64decode(record["kinesis"]["data"])
        try:
            s3 = boto3.resource('s3', region)
            object = s3.Object(bucket_name,os.path.join(bucket_prefix,bucket_prefix_add,filename))
            object.put(Body=payload)
        except botocore.exceptions.ClientError as e:
            print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))