import os
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument('--thresholds', nargs='+')
argparser.add_argument('--duration', action='store_true')
argparser.add_argument('--frequency', action='store_true')
argparser.add_argument('--cols2drop', nargs='+')
args = argparser.parse_args()
thresholds = args.thresholds
duration = args.duration
frequency = args.frequency
cols2drop = args.cols2drop

print("Generating CSV data with thresholds: " + str(thresholds))
print("Duration included: " + str(duration))
print("Frequency included: " + str(frequency))
print("Columns to drop: " + str(cols2drop))

temp = []
for i in thresholds:
    if "." in i:
        temp.append(float(i))
    else:
        temp.append(int(i))

thresholds = temp
print(thresholds)

def calculate_waso(threshold_minutes, filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    current_zero_window_length = 0
    waso = 0
    count = 0

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
                    count += 1
    return waso, count


wasoresults = []
freqresults = []
for threshold in thresholds:
    wasoresults.append([])
    freqresults.append([])
original_csv = "csvdata/datafullnight2_SE.csv"

directory_path = Path("donehypnogram")
files = os.listdir(directory_path)
files = sorted(files)
# fileids = [filename.split('.')[0].split('-')[1] for filename in files]

df = pd.read_csv(original_csv)

ids = [str(i) for i in df["nsrrid"].values]

# # show items in ids not in files
# for i in ids:
#     if i not in fileids:
#         print(i)

for filename in tqdm(files):
    # print(filename.split('.')[0].split('-')[1])
    if filename.split('.')[0].split('-')[1] in ids:
        file_path = os.path.join(directory_path, filename)
        for i, threshold in enumerate(thresholds):
            waso, freq = calculate_waso(threshold, file_path)
            wasoresults[i].append(waso)
            freqresults[i].append(freq)

# Dropping the columns
df = df.drop(cols2drop, axis=1)

allcols = df.copy(deep=True)

print("Generating csv with all cols")

# this makes a new csv with all thresholds
for i, threshold in enumerate(thresholds):
    if duration:
        newwasoname = "WASO_min" + str(threshold)
        allcols[newwasoname] = wasoresults[i]
    if frequency:
        newfreqname = "WASO_freq" + str(threshold)
        allcols[newfreqname] = freqresults[i]

allcols.to_csv("csvdata/datafullnight2_SE_waso" + "_".join([str(i) for i in thresholds]) + ".csv", index=False)

# this makes a new csv for each threshold
for i, threshold in enumerate(thresholds):
    print("Generating csv for threshold: " + str(threshold))
    clone = df.copy(deep=True)
    if duration:
        newcolname = "WASO_min" + str(threshold)
        clone[newcolname] = wasoresults[i]
    if frequency:
        newfreqname = "WASO_freq" + str(threshold)
        clone[newfreqname] = freqresults[i]
    clone.to_csv("csvdata/datafullnight2_SE_waso" + str(threshold) + ".csv", index=False)


