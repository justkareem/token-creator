import time
import requests
import json


# Function: Fetch user ID
def get_user_id(username):
    url = f"https://x.com/i/api/graphql/QGIw94L0abhuohrr76cSbw/UserByScreenName"
    variables = {
        "screen_name": username
    }
    features = {
        "hidden_profile_subscriptions_enabled": True,
        "profile_label_improvements_pcf_label_in_post_enabled": False,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "subscriptions_verification_info_is_identity_verified_enabled": True,
        "subscriptions_verification_info_verified_since_enabled": True,
        "highlights_tweets_tab_ui_enabled": True,
        "responsive_web_twitter_article_notes_tab_enabled": True,
        "subscriptions_feature_can_gift_premium": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True
    }
    field_toggles = {"withAuxiliaryUserLabels": False}
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "cookie": "guest_id=v1:171431189368611161; night_mode=2; guest_id_marketing=v1:171431189368611161; guest_id_ads=v1:171431189368611161; kdt=YuZqwnOnZL9h05pSxA3GFsD0MFgRaAuDmxCxXs84; auth_token=18cdcf673bc00e1eef611aac96f580a943d2e924; ct0=34b186d6b5dcfe438607532c7fed9dcb5be13b2b7e660be05b33b8926c40fa59fa258f6626e05223229344b216bce0c88cf7356400a01c813d35d1521139319ade76f29b4a1727ac5d2f93333ee08057; twid=u=1601514279458557953; personalization_id=\"v1_572d9eJK/Otpo3l6nrWNWA==\"; lang=en; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w=",
        "origin": "https://x.com",
        "priority": "u=1, i",
        "referer": "https://x.com/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-client-transaction-id": "nGuh9FjEkD5PrgoxoPWvzu4Ay2RvHUpCwSJVfsj1JDBG/mSkKnJswtFcYIuRyeacv3bFn5+cnCwL/iCajq1JkOfGNoT5nw",
        "x-csrf-token": "34b186d6b5dcfe438607532c7fed9dcb5be13b2b7e660be05b33b8926c40fa59fa258f6626e05223229344b216bce0c88cf7356400a01c813d35d1521139319ade76f29b4a1727ac5d2f93333ee08057",
        "x-twitter-active-user": "no",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en"
    }

    while True:
        response = requests.get(url, headers=headers, params={
            "variables": json.dumps(variables),
            "features": json.dumps(features),
            "fieldToggles": json.dumps(field_toggles)
        })

        if response.status_code == 200:
            user_id = response.json().get("data", {}).get("user", {}).get("result", {}).get("rest_id")
            if user_id:
                return user_id
        elif response.status_code == 429:
            reset_time = int(response.headers.get("x-rate-limit-reset", time.time() + 60))  # Default to 60 seconds
            sleep_duration = reset_time - time.time()
            if sleep_duration > 0:
                print(f"Rate limited. Sleeping for {sleep_duration:.2f} seconds.")
                time.sleep(sleep_duration)
        else:
            print(f"Error fetching user ID for {username}: {response.status_code}, {response.text}")
            return None


# Function: Fetch recent tweets
def get_recent_tweets(user_id):
    url = "https://x.com/i/api/graphql/tzh4soFIeC6EUW0aLxrYpQ/UserTweets"
    variables = {
        "userId": f"{user_id}",
        "count": 20,
        "includePromotedContent": True,
        "withQuickPromoteEligibilityTweetFields": True,
        "withVoice": True,
        "withV2Timeline": True
    }
    features = {
        "profile_label_improvements_pcf_label_in_post_enabled": False,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "premium_content_api_read_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "cookie": "guest_id=v1:171431189368611161; night_mode=2; guest_id_marketing=v1:171431189368611161; guest_id_ads=v1:171431189368611161; kdt=YuZqwnOnZL9h05pSxA3GFsD0MFgRaAuDmxCxXs84; auth_token=18cdcf673bc00e1eef611aac96f580a943d2e924; ct0=34b186d6b5dcfe438607532c7fed9dcb5be13b2b7e660be05b33b8926c40fa59fa258f6626e05223229344b216bce0c88cf7356400a01c813d35d1521139319ade76f29b4a1727ac5d2f93333ee08057; twid=u=1601514279458557953; personalization_id=\"v1_572d9eJK/Otpo3l6nrWNWA==\"; lang=en; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w=",
        "origin": "https://x.com",
        "priority": "u=1, i",
        "referer": "https://x.com/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-client-transaction-id": "nGuh9FjEkD5PrgoxoPWvzu4Ay2RvHUpCwSJVfsj1JDBG/mSkKnJswtFcYIuRyeacv3bFn5+cnCwL/iCajq1JkOfGNoT5nw",
        "x-csrf-token": "34b186d6b5dcfe438607532c7fed9dcb5be13b2b7e660be05b33b8926c40fa59fa258f6626e05223229344b216bce0c88cf7356400a01c813d35d1521139319ade76f29b4a1727ac5d2f93333ee08057",
        "x-twitter-active-user": "no",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en"
    }

    while True:
        response = requests.get(url, headers=headers, params={
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        })

        if response.status_code == 200:
            entries = response.json().get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get(
                "timeline", {}).get("instructions", [])
            tweets = []
            for entry in entries:
                if entry["type"] == "TimelineAddEntries":
                    for tweet_entry in entry.get("entries", []):
                        tweet_content = tweet_entry.get("content", {}).get("itemContent", {}).get("tweet_results",
                                                                                                  {}).get(
                            "result", {})
                        tweet_legacy = tweet_content.get("legacy", {})
                        quoted_status = tweet_content.get("quoted_status_result", {})
                        quoted_user = quoted_status.get("result", {}).get("core", {}).get("user_results", {}).get(
                            "result",
                            {}).get(
                            "legacy", {}).get("name")
                        tweet = {
                            "id_str": tweet_legacy.get("id_str"),
                            "text": tweet_legacy.get("full_text"),
                            "author_name": tweet_content.get("core", {}).get("user_results", {}).get("result", {}).get(
                                "legacy", {}).get("name"),
                            "author_screen_name": tweet_content.get("core", {}).get("user_results", {}).get("result",
                                                                                                            {}).get(
                                "legacy", {}).get("screen_name"),
                            "likes": tweet_legacy.get("favorite_count"),
                            "retweets": tweet_legacy.get("retweet_count"),
                            "created_at": tweet_legacy.get("created_at"),
                            "time": time.time(),
                            "replies": tweet_legacy.get("reply_count"),
                            "lang": tweet_legacy.get("lang"),
                            "media_urls": [
                                media.get("media_url_https")
                                for media in tweet_legacy.get("extended_entities", {}).get("media", [])
                                if media.get("type") == "photo"
                            ],
                            "quote_tweet_text": f'{quoted_status.get("result", {}).get("legacy", {}).get("full_text", None)} - {quoted_user}'
                        }
                        tweets.append(tweet)
            return tweets
        elif response.status_code == 429:
            reset_time = int(response.headers.get("x-rate-limit-reset", time.time() + 60))  # Default to 60 seconds
            sleep_duration = reset_time - time.time()
            if sleep_duration > 0:
                print(f"Rate limited. Sleeping for {sleep_duration:.2f} seconds.")
                time.sleep(sleep_duration)
        else:
            print(f"Error fetching tweets for {user_id}: {response.status_code}, {response.text}")
            return None
