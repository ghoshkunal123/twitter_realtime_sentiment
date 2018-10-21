# twitter_realtime_sentiment
Consume real time Twitter feed, parse, analyze and run live real time analysis and dashboards

## Get Started
Following are the pre-requirements for this project
1. Create a Twitter Account and App *(required)*
[Twitter App](https://developer.twitter.com)
2. AWS Account *(required)*
[Create AWS Account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)

3. Set up AWS Code Commit *(optional)*
[AWS CodeCommit](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html
)
## [Clone github project](https://github.com/ghoshkunal123/twitter_realtime_sentiment)
## [Clone AWS CodeCommit project](https://git-codecommit.us-east-1.amazonaws.com/v1/repos/twitter_realtime_sentiment)

## Set up environment
```shell
sudo python3 -m pip install --upgrade pip
cd twitter_realtime_sentiment
sudo python3 -m pip install -r requirements.txt
```
## (A) In order to Stream Twitter to Kinesis Stream and write to S3 bucket, analyze with Athena and visualize with QuickSight 

### *Update the twitter_**realtime_sentiment/pyscripts/config.py** file necessary information*
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
### *Open Kinesis in AWS Console*
Create a Kinesis Stream called **KunalAWSSentiment-awscloud** as mentioned by the variable kinesis_stream in the **config.py**

### *Open S3 in AWS Console*
Create an S3 bucket with the same name as denoted by the variable bucket_name in the **config.py**

### *Open Athena in AWS Console* 
Run the sql in **sql/Athena_KunalAWSSentiment_KunalAWSSentimentawscloud.sql**

### *Create a lambda function f_msck_repair_table_KunalAWSSentimentawscloud*
Copy the code from **lambda/f_msck_repair_table_KunalAWSSentimentawscloud.py**
Create an s3 trigger on Event Type ObjectCreated on s3 **kunal-dl-stage** and prefix **KunalAWSSentiment-awscloud**
Choose the runtime environment as Python 3.6
Make sure that **msck repair table** points to the right **KunalAWSSentiment** database and table **KunalAWSSentimentawscloud**
Add a trigger to the lambda picking the above stated kinesis stream

### *Create a lambda function f_stream_KunalAWSSentiment-awscloud_to_s3*
Copy the code from **lambda/f_stream_KunalAWSSentiment-awscloud_to_s3.py**
Create a Kinesis trigger on the kinesis stream mentioned by the variable kinesis_stream in the **config.py** using the Lambda Admin Role
Choose the runtime environment as Python 3.6
Make sure that variables point to the right region, S3 buckets and prefixes

### *Run the script twitter_to_kstream.py*
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_kstream.py &
```

### *Visualize the dashboard on QuickSight*
Add the data source choosing Athena, edit SQL and the sample sql under **sql/quick_sight_athena_sample.sql** and create visualization and publish to dashboard

---

## (B) In order to Stream Twitter to S3 bucket, analyze with Athena and visualize with QuickSight 

### *Update the **pyscripts/config.py** file necessary information*
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

### *Open S3 in AWS Console*
Create an S3 bucket named 

### *Open Athena in AWS Console* 
Run the sql in **sql/Athena_KunalAWSSentiment_KunalAWSSentimentawscloud.sql**

### *Create a lambda function f_msck_repair_table_KunalAWSSentimentawscloud*
Copy the code from **lambda/f_msck_repair_table_KunalAWSSentimentawscloud**
Create an s3 trigger on Event Type ObjectCreated on s3 **kunal-dl-stage** and prefix **KunalAWSSentiment-awscloud**
Choose the runtime environment as Python 3.6
Make sure that **msck repair table** points to the right **KunalAWSSentiment** database and table **KunalAWSSentimentawscloud**

### *Run the script twitter_to_s3.py*
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_s3.py &
```

### *Visualize the dashboard on QuickSight*
Add the data source choosing Athena, edit SQL and the sample sql under **sql/quick_sight_athena_sample.sql** and create visualization and publish to dashboard

---

## (C) In order to Stream Twitter to Elastic Search and search and visualize with Kibana

### *Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information*
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

### *Open Elastic Search in AWS Console*
Create an elastic search domain named **kunalawssentiment-awscloud** with number of nodes desired and update the eshost variable accordingly after creation.

### *Run the script twitter_to_es_kibana.py*
```shell
cd /twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_es_kibana.py &
```

### *Search and visualize the dashboard on Kibana*
Open Kibana and discover the data to begin with, create visualization and add them to dashboard.

### *Housekeep Elastic Search index*
Schedule the script below in crontab to delete the elastic search index daily.
```shell
59 23 * * * /usr/bin/python3 /home/ec2-user/environment/pyscripts/delete_es_index.py
#0 0 * * * /usr/bin/python3 /home/ec2-user/environment/pyscripts/twitter_to_es_kibana.py
```

---
## (D) In order to Stream Twitter to Kinesis Stream analyze with Kinesis Analytics persist in RDS and visualize with QuickSight

### *Update the twitter_realtime_sentiment/pyscripts/config.py file necessary information*
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

### *Open Kinesis in AWS Console*
Create a Kinesis Stream called KunalAWSSentiment-awscloud as mentioned by the variable kinesis_stream in the **config.py**

### *Run the script twitter_to_kstream.py*
```shell
cd twitter_realtime_sentiment/pyscripts
nohup python3 twitter_to_kstream.py &
```

### *Create a Kinesis Analytics Application from AWS Console*
Create a new application named **KunalAWSSentiment-awscloud** and connect to the streaming data choosing the source stream **KunalAWSSentiment-awscloud** and choose to auto discover the schema.

### *Add the Kinesis Analytics SQL*
From the file **sql/Kinesis_Analytics_KunalAWSSentiment-awscloud.sql** copy the SQL to in application SQL editor, choose save and run to start analyzing real time stream.

### *Assign destination for Kinesis Analytics*
Assign destination for **KunalAWSSentiment-awscloud** Kinesis Stream by assigning 
**DESTINATION_SQL_STREAM_SENTIMENT to f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_senti_to_pg**
**DESTINATION_SQL_STREAM_SOURCE to f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_src_to_pg**

### *Create Lambda functions*
#### *Create Lambda **f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_senti_to_pg***
```shell
cd twitter_realtime_sentiment/lambda
sudo yum -y install jq
lambda_name="f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_senti_to_pg"
zip_file="${lambda_name}.zip"
role_arn="arn:aws:iam::<AWS Account Number>:role/Lambda_Admin"
files="f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_senti_to_pg.py pgdb_util.py"
chmod -R 755 ${files}
zip -r "${zip_file}" psycopg2 psycopg2_binary-2.7.5.dist-info $files
subnet_ids=`aws ec2 describe-subnets | jq -r '.Subnets|map(.SubnetId)|join(",")'`
sec_group_id=`aws ec2 describe-security-groups --group-name "default" | jq -r '.SecurityGroups[].GroupId'`

aws lambda create-function \
--region "us-east-1" \
--function-name "${lambda_name}"  \
--zip-file "fileb://${zip_file}" \
--role "${role_arn}" \
--handler "${lambda_name}.lambda_handler" \
--runtime python3.6 \
--timeout 900 \
--description "Merge to ods.kunalawssentimentawscloud_senti in Aurora Postgres" \
--vpc-config SubnetIds="${subnet_ids}",SecurityGroupIds="${sec_group_id}"
```
#### *Create Lambda **f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_src_to_pg***
```shell
cd twitter_realtime_sentiment/lambda
sudo yum -y install jq
lambda_name="f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_src_to_pg"
zip_file="${lambda_name}.zip"
role_arn="arn:aws:iam::<AWS Account Number>:role/Lambda_Admin"
files="f_write_Kinesis_Analytics_KunalAWSSentiment-awscloud_src_to_pg.py pgdb_util.py"
chmod -R 755 ${files}
zip -r "${zip_file}" psycopg2 psycopg2_binary-2.7.5.dist-info $files
subnet_ids=`aws ec2 describe-subnets | jq -r '.Subnets|map(.SubnetId)|join(",")'`
sec_group_id=`aws ec2 describe-security-groups --group-name "default" | jq -r '.SecurityGroups[].GroupId'`

aws lambda create-function \
--region "us-east-1" \
--function-name "${lambda_name}"  \
--zip-file "fileb://${zip_file}" \
--role "${role_arn}" \
--handler "${lambda_name}.lambda_handler" \
--runtime python3.6 \
--timeout 900 \
--description "Merge to ods.kunalawssentimentawscloud_source in Aurora Postgres" \
--vpc-config SubnetIds="${subnet_ids}",SecurityGroupIds="${sec_group_id}"
```
### *Create and RDS Aurora Postgres DB*
Use the AWS Console to create an RDS Aurora Postgres instance, add necessary CIDR ranges to the DB Security groups for access.
Based the region assign a CIDR range to the DB Security Group
[AWS Regions and IP Address Ranges](https://docs.aws.amazon.com/quicksight/latest/user/regions.html)

### *Visualize in QuickSight*
Visualize the realtime dashboards in QuickSight