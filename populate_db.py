import redis
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

with open("res/filtered_tweets.json", "r", encoding="utf-8") as f:
    for line in f:
        tweet = json.loads(line)

        # get chirp
        chirp_id = tweet["id"]
        chirp_key = f"chirp:{chirp_id}"
        r.hset(chirp_key, mapping={
            "chirp_id": chirp_id,
            "user_id": tweet["user"]["id"],
            "created_at": tweet["created_at"],
            "text": tweet["text"],
            "source": tweet["source"],
            "retweet_count": tweet["retweet_count"],
            "favorite_count": tweet["favorite_count"],
            "lang": tweet["lang"]
        })

        # user
        user = tweet["user"]
        user_key = f"user:{user['id']}"
        r.hset(user_key, mapping={
            "user_id": user["id"],
            "name": user["name"],
            "screen_name": user["screen_name"],
            "followers_count": user["followers_count"],
            "friends_count": user["friends_count"],
            "created_at": user["created_at"],
        })

        # last 5 chirps
        r.lpush("latest_chirps", chirp_id)
        r.ltrim("latest_chirps", 0, 4)

        # follower ranking
        r.zadd("follower_ranking", {user["id"]: user["followers_count"]})

