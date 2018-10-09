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
## (A) In order to Stream Twitter to S3 bucket, analyze with Athena and visualize with QuickSight 
### Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information
```shell
# Configuration to run the job
ckey=""
csecret=""
atoken=""
asecret=""
region='''
bucket_name=''
bucekt_prefix=''
kinesis_stream=''
track=[]
```
### Open Athena in AWS Console and run the sql in twitter_realtime_sentiment/sql/Athena_KunalAWSSentiment_KunalAWSSentimentawscloud.sql

### Create a lambda function f_msck_repair_table_KunalAWSSentimentawscloud
Copy the code from twitter_realtime_sentiment/lambda/f_msck_repair_table_KunalAWSSentimentawscloud
Create an s3 trigger on Event Type ObjectCreated on s3 kunal-dl-stage and prefix KunalAWSSentiment-awscloud
Choose the runtime environment as Python 3.6
Make sure that msck repair table points to the right KunalAWSSentiment database and table KunalAWSSentimentawscloud

### Visualize the dashboard on QuickSight
Add the data source choosing Athena, edit SQL and the sample sql under sql/quick_sight_athena_sample.sql