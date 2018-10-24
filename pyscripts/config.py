'''
Created on September 25, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to declare the common configuration
On 09/25/2018 created the first version
On 10/09/2018 Addded more for Elastic Search
'''

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