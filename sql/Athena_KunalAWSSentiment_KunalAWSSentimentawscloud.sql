CREATE DATABASE IF NOT EXISTS KunalAWSSentiment 
COMMENT 'Sentiment Analysis for Twitter data feed' 
LOCATION 's3://kunal-dl-stage/KunalAWSSentiment-awscloud' 
WITH DBPROPERTIES ('creator'='Kunal Ghosh', 'Dept.'='AWS Named NorCal');

    CREATE EXTERNAL TABLE KunalAWSSentiment.KunalAWSSentimentawscloud (
        created_at string,
        id bigint,
        id_str string,
        text string,
        source string,
        truncated boolean,
        in_reply_to_status_id string,
        in_reply_to_status_id_str string,
        in_reply_to_user_id string,
        in_reply_to_user_id_str string,
        in_reply_to_screen_name string,
        user struct<id:string,
                  id_str:string,
                  name:string,
                  screen_name:string,
                  location:string,
                  url:string,
                  description:string,
                  translator_type:string,
                  protected:boolean,
                  verified:boolean,
                  followers_count:bigint,
                  friends_count:bigint,
                  listed_count:bigint,
                  favourites_count:bigint,
                  statuses_count:bigint,
                  created_at:string,
                  utc_offset:string,
                  time_zone:string,
                  geo_enabled:boolean,
                  lang:string,
                  contributors_enabled:boolean,
                  is_translator:boolean>,
        geo string,
        coordinates string,
        place struct<country_code:string,
                    country:string,
                    full_name:string,
                    bounding_box:struct<type:string,
                                        coordinates:array<array<array<double>>>
                                        >,
                    attributes:string
                    >,
        contributors string,
        is_quote_status boolean,
        quote_count bigint,
        reply_count bigint,
        retweet_count bigint,
        favorite_count bigint,
        entities struct<hashtags:array<struct<text:string>>,
                       user_mentions:array<struct<screen_name:string,name:string,id:bigint,id_str:string>>
                       >,
        favorited boolean,
        retweeted boolean,
        possibly_sensitive boolean,
        filter_level string,
        lang string,
        timestamp_ms bigint,
        sentiments string
        )
    PARTITIONED BY (dt string)
    ROW FORMAT  serde 'org.openx.data.jsonserde.JsonSerDe'
    LOCATION 's3://kunal-dl-stage/KunalAWSSentiment-awscloud/';