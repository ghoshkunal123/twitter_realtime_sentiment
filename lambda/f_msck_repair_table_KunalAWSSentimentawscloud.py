import json
import boto3
import botocore

def lambda_handler(event, context):
    athena_response=''
    # Call the msck repair table kunalawssentiment.KunalAWSSentimentawscloud
    try:
        athena_client=boto3.client('athena','us-east-1')
        athena_response=athena_client.start_query_execution(QueryString='msck repair table kunalawssentiment.KunalAWSSentimentawscloud',ResultConfiguration={'OutputLocation': 's3://aws-athena-query-results-247402750169-us-east-1/f_msck_repair_table_KunalAWSSentimentawscloud/'})
    except botocore.exceptions.ClientError as e:
        print('{}: {}'.format(e.response['Error']['Code'], e.response['Error']['Message']))
    return(athena_response)