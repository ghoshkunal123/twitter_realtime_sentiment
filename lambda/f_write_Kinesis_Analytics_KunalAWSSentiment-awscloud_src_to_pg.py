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
import base64
import json
import psycopg2
from pgdb_util import *

def lambda_handler(event, context):
    payload = event['records']
    conn = make_conn()
    for record in payload:
        try:
            query_cmd=''
            #query_cmd1=''
            payload = base64.b64decode(record['data'])
            payload_dict=json.loads(payload)
            print('payload : {}'.format(payload))
            print('payload_dict : {}'.format(payload_dict))
            #print(type(payload_dict))
            print(payload_dict['PROCESS_TIME'])
            process_time=payload_dict['PROCESS_TIME']
            tweet_track=payload_dict['TWEET_TRACK']
            tweet_source=payload_dict['SOURCE']
            source_tweets_last_hour=payload_dict['SOURCE_TWEETS_LAST_HOUR']

            query_cmd="insert into ods.kunalawssentimentawscloud_source(process_time,tweet_track,tweet_source,source_tweets_last_hour) values('%s','%s', '%s', %d) on conflict(tweet_source) do update set process_time = EXCLUDED.process_time, source_tweets_last_hour = EXCLUDED.source_tweets_last_hour where ods.kunalawssentimentawscloud_source.process_time < EXCLUDED.process_time or (ods.kunalawssentimentawscloud_source.process_time = EXCLUDED.process_time and ods.kunalawssentimentawscloud_source.source_tweets_last_hour < EXCLUDED.source_tweets_last_hour);" % (process_time,tweet_track,tweet_source,source_tweets_last_hour)
            #query_cmd1="insert into stage.kunalawssentimentawscloud_senti(process_time,tweet_track,sentiments,sentiments_tweets_last_hour) values('%s','%s', '%s', %d);" % (process_time,tweet_track,sentiments,sentiments_tweets_last_hour)
            print('Running the query : {}'.format(query_cmd))
            #print('Running the query : {}'.format(query_cmd1))
            #execute_query(conn, query_cmd1)
            execute_query(conn, query_cmd)
        except:
            #print('Failed executing the query : {}'.format(query_cmd1))
            print('Failed executing the query : {}'.format(query_cmd))
    conn.close()