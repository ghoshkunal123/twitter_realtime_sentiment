select ts.id
,ts.sentiments
,regexp_extract(ts.source,'.(>)([\w+\s+]+)(</a>)',2) access_from_app
,ts.user.id user_id
,ts.user.name user_name
,ts.user.screen_name user_screen_name
,ht.hashtags_text hashtags_text
,um.user_mentions_screen_name user_mentions_screen_name
,um.user_mentions_name user_mentions_name
,ts.text
from "kunalawssentiment"."kunalawssentimentawscloud" ts
left join
(select id
,hashtags_text.text hashtags_text
from "kunalawssentiment"."kunalawssentimentawscloud"
cross join unnest(entities.hashtags) as t(hashtags_text)
where dt=format_datetime(current_timestamp,'YYYY-MM-dd')) ht
on ts.id = ht.id
left join
(select id
,user_mentions_name.screen_name user_mentions_screen_name
,user_mentions_name.name user_mentions_name
from "kunalawssentiment"."kunalawssentimentawscloud"
cross join unnest(entities.hashtags) as t(hashtags_text)
cross join unnest(entities.user_mentions) as t(user_mentions_name)
where dt=format_datetime(current_timestamp,'YYYY-MM-dd')) um
on ts.id = um.id
where ts.dt=format_datetime(current_timestamp,'YYYY-MM-dd');