import bz2
import os

input_folder = "res/raw_data"
output_folder = "res/data"

#Decompress the data .bz2 and reformat it to .json
for filename in os.listdir(input_folder):
    if filename.endswith(".bz2"):
        input_path = os.path.join(input_folder, filename)
        output_filename = filename[:-4]
        output_path = os.path.join(output_folder, output_filename)

        with bz2.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            f_out.write(f_in.read())

print("Done")
