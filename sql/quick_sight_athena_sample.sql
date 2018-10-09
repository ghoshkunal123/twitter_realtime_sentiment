SELECT id
,lang
,sentiments
,regexp_extract(source,'.(>)([\w+\s+]+)(</a>)',2) access_from_app
,user.id user_id
,user.name user_name
,user.screen_name user_screen_name
,user.location user_location
,user.description user_description
,user.followers_count user_followers_count
,user.friends_count user_friends_count
,user.listed_count user_listed_count
,user.favourites_count user_favourites_count
,user.statuses_count user_statuses_count
,user.lang user_lang
,hashtags_text.text hashtags_text
,user_mentions_name.screen_name user_mentions_screen_name
,user_mentions_name.name user_mentions_name
,text
from "kunalawssentiment"."kunalawssentimentawscloud"
cross join unnest(entities.hashtags) as t(hashtags_text)
cross join unnest(entities.user_mentions) as t(user_mentions_name)
where dt=format_datetime(current_timestamp,'YYYY-MM-dd');