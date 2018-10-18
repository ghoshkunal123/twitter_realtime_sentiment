# twitter_realtime_sentiment
Twitter feed and simple sentiment analysis

## Get Started
Following are the pre-requirements for this project
1. Create a Twitter Account and App 
[Twitter App](https://developer.twitter.com)
2. AWS Account
[Create AWS Account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)

## [Clone project](https://github.com/ghoshkunal123/twitter_realtime_sentiment)
## Set up environment
```shell
sudo python3 -m pip install --upgrade pip
cd twitter_realtime_sentiment
sudo python3 -m pip install -r requirements.txt
```
## (A) In order to Stream Twitter to Kinesis Stream and write to S3 bucket, analyze with Athena and visualize with QuickSight 
### Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information
```shell
# Configuration to run the job
ckey=""
csecret=""
atoken=""
asecret=""
region='us-east-1'
bucket_name='kunal-dl-stage'
bucekt_prefix='KunalAWSSentiment-awscloud'
kinesis_stream='KunalAWSSentiment-awscloud'
track=["awscloud"]
```

### Open S3 in AWS Console
Create an S3 bucket with the same name as denoted by the variable bucket_name in the config.py

### Open Athena in AWS Console 
Run the sql in twitter_realtime_sentiment/sql/Athena_KunalAWSSentiment_KunalAWSSentimentawscloud.sql

### Create a lambda function f_msck_repair_table_KunalAWSSentimentawscloud
Copy the code from twitter_realtime_sentiment/lambda/f_msck_repair_table_KunalAWSSentimentawscloud.py
Create an s3 trigger on Event Type ObjectCreated on s3 kunal-dl-stage and prefix KunalAWSSentiment-awscloud
Choose the runtime environment as Python 3.6
Make sure that msck repair table points to the right KunalAWSSentiment database and table KunalAWSSentimentawscloud
Add a trigger to the lambda picking the above stated kinesis stream

### Create a lambda function f_stream_KunalAWSSentiment-awscloud_to_s3
Copy the code from twitter_realtime_sentiment/lambda/f_stream_KunalAWSSentiment-awscloud_to_s3.py
Create a Kinesis trigger on the kinesis stream mentioned by the variable kinesis_stream in the config.py using the Lambda Admin Role
Choose the runtime environment as Python 3.6
Make sure that variables point to the right region, S3 buckets and prefixes

### Run the script twitter_to_s3.py
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_kstream.py &
```

### Visualize the dashboard on QuickSight
Add the data source choosing Athena, edit SQL and the sample sql under sql/quick_sight_athena_sample.sql and create visualization and publish to dashboard


## (B) In order to Stream Twitter to S3 bucket, analyze with Athena and visualize with QuickSight 
### Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information
```shell
# Configuration to run the job
ckey=""
csecret=""
atoken=""
asecret=""
region='us-east-1'
bucket_name='kunal-dl-stage'
bucekt_prefix='KunalAWSSentiment-awscloud'
kinesis_stream='KunalAWSSentiment-awscloud'
track=["awscloud"]
```

### Open S3 in AWS Console
Create an S3 bucket named 

### Open Athena in AWS Console 
Run the sql in twitter_realtime_sentiment/sql/Athena_KunalAWSSentiment_KunalAWSSentimentawscloud.sql

### Create a lambda function f_msck_repair_table_KunalAWSSentimentawscloud
Copy the code from twitter_realtime_sentiment/lambda/f_msck_repair_table_KunalAWSSentimentawscloud
Create an s3 trigger on Event Type ObjectCreated on s3 kunal-dl-stage and prefix KunalAWSSentiment-awscloud
Choose the runtime environment as Python 3.6
Make sure that msck repair table points to the right KunalAWSSentiment database and table KunalAWSSentimentawscloud

### Run the script twitter_to_s3.py
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_s3.py &
```

### Visualize the dashboard on QuickSight
Add the data source choosing Athena, edit SQL and the sample sql under sql/quick_sight_athena_sample.sql and create visualization and publish to dashboard


## (C) In order to Stream Twitter to Elastic Search and search and visualize with Kibana
### Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information
```shell
# Configuration to run the job
ckey=""
csecret=""
atoken=""
asecret=""
region='us-east-1'
bucket_name='kunal-dl-stage'
bucekt_prefix='KunalAWSSentiment-awscloud'
kinesis_stream='KunalAWSSentiment-awscloud'
track=["awscloud"]
eshost = 'search-kunalawssentiment-awscloud-ot7sscaqlklrykg72y56ybqahq.us-east-1.es.amazonaws.com'
es_index='twitter_stream'
es_index_doc_type='tweet'
```

### Open Elastic Search in AWS Console
Create an elastic search domain named kunalawssentiment-awscloud with number of nodes desired and update the eshost variable accordingly after creation.

### Run the script twitter_to_es_kibana.py
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_es_kibana.py &
```

### Search and visualize the dashboard on Kibana
Open Kibana and discover the data to begin with, create visualization and add them to dashboard.

### Housekeep Elastic Search index
Schedule the script below in crontab to delete the elastic search index daily.
```shell
59 23 * * * /usr/bin/python3 /home/ec2-user/environment/pyscripts/delete_es_index.py
0 0 * * * /usr/bin/python3 /home/ec2-user/environment/pyscripts/twitter_to_es_kibana.py
```