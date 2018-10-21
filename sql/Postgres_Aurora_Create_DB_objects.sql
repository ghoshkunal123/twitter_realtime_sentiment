-- Create a schema
CREATE SCHEMA ods;

-- Drop table
--drop table ods.kunalawssentimentawscloud;
--drop table stage.kunalawssentimentawscloud;

-- Create table senti
CREATE TABLE ods.kunalawssentimentawscloud_senti(
   created_at timestamp default now(),
   process_time timestamp,
   tweet_track varchar(20),
   sentiments varchar(20) UNIQUE,
   sentiments_tweets_last_hour bigint);

 -- Create table source
 CREATE TABLE ods.kunalawssentimentawscloud_source(
    created_at timestamp default now(),
    process_time timestamp,
    tweet_track varchar(20),
    tweet_source varchar(128) UNIQUE,
    source_tweets_last_hour bigint);

-- Create stage schema and tables for testing
-- CREATE SCHEMA stage;
/*CREATE TABLE stage.kunalawssentimentawscloud_senti(
  created_at timestamp default now(),
  process_time timestamp,
  tweet_track varchar(20),
  sentiments varchar(20),
  sentiments_tweets_last_hour bigint);*/

/*CREATE TABLE stage.kunalawssentimentawscloud_source(
     created_at timestamp default now(),
     process_time timestamp,
     tweet_track varchar(20),
     tweet_source varchar(128),
     source_tweets_last_hour bigint);*/
