import json
import os

folder_path = 'res/data'
output_file_path = 'res/filtered_tweets.json'

all_filtered_tweets = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            total_chirps = []

            for line in f:
                try:
                    total_chirps.append(json.loads(line))
                except json.JSONDecodeError:
                    print("Error in line:", line)
            
        # filter, only english, no retweets
        for chirp in total_chirps:
            if "created_at" in chirp and chirp.get("lang") == "en" and "retweeted_status" not in chirp:
                all_filtered_tweets.append(chirp)

# get all the data in one json file (easier to populate in redis)
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for tweet in all_filtered_tweets:
        json_line = json.dumps(tweet, ensure_ascii=False)
        outfile.write(json_line + "\n")

print("Done")
