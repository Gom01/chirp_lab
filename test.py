import json
import jq

with open('./res/data/00.json') as f:
    chirps = []
    for line in f:
        try:
            chirps.append(json.loads(line))
        except json.JSONDecodeError:
            print("Error decoding line:", line)
    print("Loaded", len(chirps), "tweets")
