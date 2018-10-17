/**
 * Welcome to the SQL editor
 * =========================
 *
 * The SQL code you write here will continuously transform your streaming data
 * when your application is running.
 *
 * Get started by clicking "Add SQL from templates" or pull up the
 * documentation and start writing your own custom queries.
 */
 CREATE OR REPLACE STREAM DESTINATION_SQL_STREAM_SENTIMENT
 (process_time timestamp
 ,tweet_track varchar(20)
 ,sentiments varchar(20)
 ,sentiments_tweets_last_hour bigint
 );

 CREATE OR REPLACE PUMP output_pump_sentiment AS INSERT INTO "DESTINATION_SQL_STREAM_SENTIMENT"
 SELECT STREAM ROWTIME,
 'awscloud',
 "sentiments",
 COUNT("id") OVER LAST_HOUR_SENTI AS sentiments_tweets_last_hour
 FROM "SOURCE_SQL_STREAM_001"
 WINDOW LAST_HOUR_SENTI AS (PARTITION BY "sentiments" RANGE INTERVAL '1' HOUR PRECEDING);


CREATE OR REPLACE STREAM DESTINATION_SQL_STREAM_SOURCE
(process_time timestamp
,tweet_track varchar(20)
,source varchar(128)
,source_tweets_last_hour bigint
);

CREATE OR REPLACE PUMP output_pump_source AS INSERT INTO "DESTINATION_SQL_STREAM_SOURCE"
SELECT STREAM ROWTIME,
'awscloud',
SUBSTRING("source", POSITION ('rel="nofollow">' IN "source")+CHAR_LENGTH('rel="nofollow">'), POSITION ('</a>' IN "source")-(POSITION ('rel="nofollow">' IN "source")+CHAR_LENGTH('rel="nofollow">'))) AS source,
COUNT("id") OVER LAST_HOUR_SOURCE AS source_tweets_last_hour
FROM "SOURCE_SQL_STREAM_001"
WINDOW LAST_HOUR_SOURCE AS (PARTITION BY SUBSTRING("source", POSITION ('rel="nofollow">' IN "source")+CHAR_LENGTH('rel="nofollow">'), POSITION ('</a>' IN "source")-(POSITION ('rel="nofollow">' IN "source")+CHAR_LENGTH('rel="nofollow">'))) RANGE INTERVAL '1' HOUR PRECEDING);
