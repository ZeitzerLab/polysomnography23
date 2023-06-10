import os
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def calculate_waso(threshold_minutes, filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    current_zero_window_length = 0
    waso = 0

    for line in lines:
        digit = int(line.strip())

        if digit == 0:
            current_zero_window_length += 1
        else:
            if current_zero_window_length > 0:
                wake_time_min = (15 * current_zero_window_length) / 60
                current_zero_window_length = 0

                if wake_time_min > threshold_minutes:
                    waso += wake_time_min    
    return waso


thresholds = [2, 3, 4, 5]
wasoresults = []
for threshold in thresholds:
    wasoresults.append([])
original_csv = "datafullnight2_SE.csv"

directory_path = Path("donehypnogram")
files = os.listdir(directory_path)
files = sorted(files)
fileids = [filename.split('.')[0].split('-')[1] for filename in files]

df = pd.read_csv(original_csv)
ids = [str(i) for i in df["nsrrid"].values]

# show items in ids not in files
for i in ids:
    if i not in fileids:
        print(i)

for filename in tqdm(files):
    # print(filename.split('.')[0].split('-')[1])
    if filename.split('.')[0].split('-')[1] in ids:
        file_path = os.path.join(directory_path, filename)
        for i, threshold in enumerate(thresholds):
            waso = calculate_waso(threshold, file_path)
            wasoresults[i].append(waso)

for i, threshold in enumerate(thresholds):
    newcolname = "WASO_" + str(threshold) + "min"
    df[newcolname] = wasoresults[i]

df.to_csv("datafullnight2_SE_waso.csv", index=False)

            