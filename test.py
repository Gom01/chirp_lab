import json
import os

folder_path = './res/data'
output_folder = './res/data_filtered'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Only process JSON files
    if filename.endswith('.json'):
        with open(file_path, 'r') as f:
            total_chirps = []
            for line in f:
                try:
                    total_chirps.append(json.loads(line))
                except json.JSONDecodeError:
                    print("Error decoding line:", line)
            # print("Loaded", len(total_chirps), "tweets")

        # Filter by lang = "en", remove "delete" and "RT"
        filtered_lang = []

        for chirp in total_chirps:
            if "created_at" in chirp:
                if chirp.get("lang") == "en":
                    if "retweeted_status" not in chirp:
                        filtered_lang.append(chirp)


        # print("Filtered", len(filtered_lang), "tweets")

        # Save filtered data to a new file in the 'data_filtered' folder
        output_file_path = os.path.join(output_folder, f"filtered_{filename}")

        with open(output_file_path, 'w') as file:
            json.dump(filtered_lang, file, indent=4)

        #print(f"Processed {filename}, {len(filtered_lang)} filtered tweets saved.")
