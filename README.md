# Chirp - Compact Hub for Instant Real-time Posting

Chirp is a lightweight platform inspired by Twitter (now X), developed as part of the "Beyond Relational Databases" course (205.2). It showcases the modeling and implementation of a key-value database using Redis to manage a real-time feed of user posts (chirps).

## Authors

- Ana Gomes  
- Flavien Gomez

## Features

- Parse and filter tweet data in JSON format.
- Store chirps and user data efficiently using Redis key-value structures.
- Display the latest 5 chirps.
- Display top 5 users by:
  - Number of followers
  - Number of chirps posted
- Simple web UI built using Streamlit.

## Technologies

- Python 3
- Redis
- Streamlit

## Project Structure

```
.
├── get_data.py          # Decompress raw .bz2 tweet files
├── filter_data.py       # Filter English tweets and remove retweets
├── populate_db.py       # Import structured tweet data into Redis
├── display_data.py      # Streamlit app for visualization
├── res/
│   ├── raw_data/        # Input .bz2 files
│   ├── data/            # Extracted raw JSON files
│   └── filtered_tweets.json  # Cleaned and filtered tweet dataset
```

## Installation & Usage

### 1. Install Requirements

Make sure Redis is running locally on port `6379`.

```bash
pip install streamlit 
```

### 2. Data Preparation

- Place your `.bz2` tweet data files in `res/raw_data/`
- Extract and process the data:

```bash
python get_data.py
python filter_data.py
```

### 3. Populate Redis

```bash
python populate_db.py
```

### 4. Launch Web App

```bash
streamlit run display_data.py
```

## Redis Data Model

- `chirp:{id}` → hash of chirp metadata
- `user:{id}` → hash of user profile
- `chirps_by_date` → sorted set of chirp IDs by timestamp
- `follower_ranking` → sorted set of user IDs by follower count
- `chirp_count` → sorted set of user IDs by chirp count


