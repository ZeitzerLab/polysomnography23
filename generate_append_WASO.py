import os
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

def remove_leading_zeros(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    leading_zeros_removed = False
    consecutive_ones_count = 0

    for line in lines:
        digit = int(line.strip())

        if not leading_zeros_removed:
            if digit != 0 and digit != 1:
                leading_zeros_removed = True
                consecutive_ones_count = 0
                modified_lines.append(str(digit))
            elif digit == 0:
                consecutive_ones_count = 0
            elif digit == 1:
                if consecutive_ones_count == 5:
                    leading_zeros_removed = True
                    # add 6 ones to the modified lines
                    modified_lines.extend(['1'] * 6)
                    continue
                consecutive_ones_count += 1
        else:
            modified_lines.append(str(digit))

    try:    
        # remove trailing zeros from modified lines
        while modified_lines[-1] == '0':
            modified_lines.pop()
    except IndexError:
        print(filename)

    with open(filename, 'w') as file:
        file.write('\n'.join(modified_lines))

def calculate_waso_and_duration_thresholded(threshold_minutes, filepath):
    print("Calculating WASO and duration for " + filepath)
    print("Threshold: " + str(threshold_minutes))
    with open(filepath, 'r') as file:
        lines = file.readlines()

    current_sleep_window_length = 0
    current_wake_window_length = 0
    sleepduration = 0
    wakeduration = 0
    calculated_sleeptowake_frequency = 0

    for line in lines:
        digit = int(line.strip())

        if digit != 0:
            # sleep
            current_sleep_window_length += 1

            # if wake window is greater than 0, then we have a wake window to add
            if current_wake_window_length > 0:
                wakedurationinminutes = (15 * current_wake_window_length) / 60
                current_wake_window_length = 0

                # DO NOT THRESHOLD WASO HERE
                wakeduration += wakedurationinminutes
            
        else:
            # wake
            current_wake_window_length += 1

            # if sleep window is greater than 0, then we have a sleep window to add
            if current_sleep_window_length > 0:
                sleeptimeinminutes = (15 * current_sleep_window_length) / 60
                current_sleep_window_length = 0
                
                sleepduration += sleeptimeinminutes
                if sleeptimeinminutes >= threshold_minutes:
                    calculated_sleeptowake_frequency += 1
    print("wake duration: " + str(wakeduration))
    print("sleep duration: " + str(sleepduration))
    print("sleep to wake frequency: " + str(calculated_sleeptowake_frequency))
    return wakeduration, calculated_sleeptowake_frequency, sleepduration

# # for testing
# calculate_waso_and_duration_thresholded(0.25, "donehypnogram/shhs1-999999.hypnogram.txt")
# exit()

wasoresults = []
freqresults = []
sleepdurations = []

for threshold in thresholds:
    wasoresults.append([])
    freqresults.append([])
original_csv = "csvdata/datafullnight2_SE.csv"

directory_path = Path("donehypnogram")
files = os.listdir(directory_path)
files = sorted(files)

# drop files not in ids (see notes.txt)
files.remove("shhs1-200033.hypnogram.txt")
files.remove("shhs1-201671.hypnogram.txt")
files.remove("shhs1-202310.hypnogram.txt")
files.remove("shhs1-202708.hypnogram.txt")
files.remove("shhs1-203135.hypnogram.txt")

fileids = [filename.split('.')[0].split('-')[1] for filename in files]

df = pd.read_csv(original_csv)

# DROP BAD ROWS (see notes.txt)
df = df[df["nsrrid"] != 200230]
df = df[df["nsrrid"] != 202180]
df = df[df["nsrrid"] != 202310]
df = df[df["nsrrid"] != 203065]

ids = [str(i) for i in df["nsrrid"].values]

# show items in ids not in files

# ids is generated from the original csv
# fileids is generated from the files in the directory
for i in fileids:
    if i not in ids:
        print("not in ids: " + i)    

for filename in tqdm(files):
    # print(filename.split('.')[0].split('-')[1])
    if filename.split('.')[0].split('-')[1] in ids:

        file_path = os.path.join(directory_path, filename)
        # remove leading zeros
        remove_leading_zeros(file_path)
        for i, threshold in enumerate(thresholds):
            waso, freq, sleepdur = calculate_waso_and_duration_thresholded(threshold, file_path)
            wasoresults[i].append(waso)
            freqresults[i].append(freq)
        if "999999" in filename:
            print("waso: " + str(waso))
            print("freq: " + str(freq))
            print("sleepdur: " + str(sleepdur))
        sleepdurations.append(sleepdur)

for i in zip(files, sleepdurations):
    print(i)

# # add columns to df
df["sleepdur"] = sleepdurations

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
        newsleepdurcolumn = "S?W/sleepdur_" + str(threshold)
        allcols[newsleepdurcolumn] = allcols[newfreqname] / allcols["sleepdur"]

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
        newsleepdurcolumn = "S?W/sleepdur_" + str(threshold)
        clone[newsleepdurcolumn] = clone[newfreqname] / (clone["sleepdur"] + clone["sleepdur"])
    clone.to_csv("csvdata/datafullnight2_SE_waso" + str(threshold) + ".csv", index=False)


