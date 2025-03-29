import redis
import json
from dateutil import parser  # Install with: pip install python-dateutil

# Connect to Redis (ensure you're in the correct DB)
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def populate_db():
    # Optional: flush the DB to start fresh
    r.flushdb()
    
    # Open the JSON file containing the tweets
    with open("res/filtered_tweets.json", "r", encoding="utf-8") as f:
        for line in f:
            tweet = json.loads(line)

            # Get chirp details
            chirp_id = tweet["id"]
            chirp_key = f"chirp:{chirp_id}"

            # Store chirp data in a hash
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

            # Parse the 'created_at' field into a Unix timestamp
            try:
                timestamp = parser.parse(tweet["created_at"]).timestamp()
            except Exception as e:
                print(f"Error parsing date for chirp {chirp_id}: {tweet['created_at']}", e)
                continue

            # Add the chirp ID to a sorted set keyed by creation timestamp
            r.zadd("chirps_by_date", {chirp_id: timestamp})

            # Store user data
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

            # Update the follower ranking sorted set (score = followers_count)
            r.zadd("follower_ranking", {user["id"]: user["followers_count"]})
            
            # Update the chirp count sorted set: increment the count for the user by 1
            r.zincrby("chirp_count", 1, user["id"])

if __name__ == "__main__":
    populate_db()
    print("Database populated successfully.")
