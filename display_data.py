import redis
import streamlit as st

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def display_data():
    # Display Latest Chirps 
    st.header("Latest Chirps")

    # Retrieve the latest 5 chirp IDs from the sorted set (highest timestamp first)
    chirp_ids = r.zrevrange("chirps_by_date", 0, 4)
    
    for cid in chirp_ids:
        chirp_key = f"chirp:{cid}"
        chirp = r.hgetall(chirp_key)
        if chirp:
            user_key = f"user:{chirp.get('user_id')}"
            user_info = r.hgetall(user_key)

            st.subheader(f"User: {user_info.get('screen_name')}")
            st.write(f"**Text**: {chirp.get('text')}")
            st.write(f"**Created At**: {chirp.get('created_at')}")
            st.write(f"**Retweets**: {chirp.get('retweet_count')}")
            st.write(f"**Favorites**: {chirp.get('favorite_count')}")
            st.write("---")
        else:
            st.write(f"Chirp ID {cid} not found.")

    # Display Top 5 Users by Followers in the Sidebar
    st.sidebar.header("Top 5 Users by Followers")
    top_users_followers = r.zrevrange("follower_ranking", 0, 4, withscores=True)
    
    for user_id, followers_count in top_users_followers:
        user_key = f"user:{user_id}"
        user_info = r.hgetall(user_key)
        if user_info:
            st.sidebar.write(
                f"**Screen Name**: {user_info.get('screen_name')} | "
                f"**Followers**: {int(followers_count)}"
            )
        else:
            st.sidebar.write(f"User ID {user_id} not found.")
    
    # Display Top 5 Users by Chirp Count in the Sidebar
    st.sidebar.header("Top 5 Users by Chirp Count")
    top_users_chirps = r.zrevrange("chirp_count", 0, 4, withscores=True)
    
    for user_id, chirp_count in top_users_chirps:
        user_key = f"user:{user_id}"
        user_info = r.hgetall(user_key)
        if user_info:
            st.sidebar.write(
                f"**Screen Name**: {user_info.get('screen_name')} | "
                f"**Chirps**: {int(chirp_count)}"
            )
        else:
            st.sidebar.write(f"User ID {user_id} not found.")

if __name__ == "__main__":
    display_data()
