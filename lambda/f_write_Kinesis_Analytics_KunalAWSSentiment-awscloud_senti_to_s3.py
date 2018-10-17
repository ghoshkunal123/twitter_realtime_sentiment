# An Amazon Kinesis Analytics application will invoke this function after it has seen determined it has seen all records associated with a
# particular rowtime value.
# If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a tumbling window, this means
# that this function is invoked per tumbling window trigger.
# If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a continuous query or a sliding
# window, this means your Lambda function will be invoked approximately once per second.

# This function requires that the output records of the Kinesis Analytics application has a key identifier (row_id) and rowtimestamp (row_timestamp)
# and the output record format type is specified as JSON.

# A sample output record from Kinesis Analytics application for this function is as below
# {"ROWTIME_TIMESTAMP":"2017-12-15 01:09:50.000","VEHICLEID":"5","VEHICLECOUNT":18}

# Please uncomment the below code as it fit your needs.

from __future__ import print_function
import boto3
import base64
from json import loads
import botocore
import datetime
import os
import uuid


def lambda_handler(event, context):
  region = 'us-east-1'
  payload = event['records']
  bucket_name='kunal-dl-enrich'
  bucket_prefix='KunalAWSSentiment-awscloud'
  bucket_prefix_extra='sentiments'
  bucket_prefix_add = datetime.datetime.strftime(datetime.datetime.now(), 'dt=%Y-%m-%d')
  filename = str(uuid.uuid4()) + '_' + datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S%f') + '.json'

  for record in payload:
      try:
        s3 = boto3.resource('s3', region)
        object = s3.Object(bucket_name,os.path.join(bucket_prefix,bucket_prefix_extra,bucket_prefix_add,filename))
        payload = base64.b64decode(record['data'])
        object.put(Body=payload)
      except botocore.exceptions.ClientError as e:
        print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))