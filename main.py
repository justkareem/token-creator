from time import sleep
from token_creator import send_local_create_tx
from twitter import *
from gemini import analyze_tweet_with_gemini

MONITORED_USERNAMES = ["cat_gta34720"]  # Example Twitter user IDs


# Main function to process tweets
def process_tweets():
    print("Checking for new tweets...")
    seen_tweets = set()
    for username in MONITORED_USERNAMES:
        user_id = get_user_id(username)
        if not user_id:
            continue
        recent_tweets = get_recent_tweets(user_id)
        for tweet in recent_tweets:
            seen_tweets.add(tweet["id_str"])

    while True:
        for username in MONITORED_USERNAMES:
            user_id = get_user_id(username)
            if not user_id:
                continue
            tweets = get_recent_tweets(user_id)
            for tweet in tweets:
                tweet_id = tweet.get("id_str")
                if not tweet_id:
                    continue  # Skip if no ID

                if tweet_id in seen_tweets:
                    continue
                seen_tweets.add(tweet_id)
                print(f"New tweet found: {tweet['text']}")
                media_urls = tweet.get("media_urls", [])  # Get media URLs if available
                if not tweet.get("text", "") and not media_urls:  # Skip empty tweets
                    continue

                # Analyze the tweet with Gemini
                tweet_analysis = analyze_tweet_with_gemini(tweet, media_urls)
                if tweet_analysis and tweet_analysis.get('meme_level', 0) >= 5:
                    coin_details = {
                        "name": tweet_analysis.get('coin_name', 'DefaultCoin'),
                        "ticker": tweet_analysis.get('ticker', 'DEF'),
                        "description": tweet_analysis.get('coin_description', 'Default Description'),
                        "image": media_urls[0] if media_urls else None,
                        "meme_level": tweet_analysis.get('meme_level', 0)
                    }
                    # Launch coin and optionally purchase
                    send_local_create_tx(coin_details, tweet)
                else:
                    print("The tweet isn't memecoin worth lol")
            sleep(20)


# Run the process once
if __name__ == "__main__":
    process_tweets()
