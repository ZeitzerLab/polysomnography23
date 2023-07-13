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

def calculate_waso_and_duration(threshold_minutes, filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    current_nonzero_window_length = 0
    waso = 0
    count = 0
    sleepduration = 0

    for line in lines:
        digit = int(line.strip())

        if digit == 0:
            current_nonzero_window_length += 1
        else:
            sleepduration += .25
            if current_nonzero_window_length > 0:
                wake_time_min = (15 * current_nonzero_window_length) / 60
                current_nonzero_window_length = 0

                if wake_time_min > threshold_minutes:
                    waso += wake_time_min
                    count += 1
    return waso, count, sleepduration


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

# not in ids: 200033
# not in ids: 201671
# not in ids: 202310
# not in ids: 202708
# not in ids: 203135

# drop files not in ids
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

# # show items in ids not in files

#ids is generated from the original csv
#fileids is generated from the files in the directory
for i in fileids:
    if i not in ids:
        print("not in ids: " + i)

print(len(ids))
print(len(fileids))
    

for filename in tqdm(files):
    # print(filename.split('.')[0].split('-')[1])
    if filename.split('.')[0].split('-')[1] in ids:
        file_path = os.path.join(directory_path, filename)
        sleepdur = 0
        for i, threshold in enumerate(thresholds):
            waso, freq, sleepdur = calculate_waso_and_duration(threshold, file_path)
            wasoresults[i].append(waso)
            freqresults[i].append(freq)
        sleepdurations.append(sleepdur)

# Dropping the columns
df = df.drop(cols2drop, axis=1)

# # TODO: make the sleep to wake column average over total sleep time

# # sum of ["N1 (min)", "N2 (min)", "N3 (min)", "REM (min)"] is sleep duration

# # add a sleep duration column 

# add to original DF because this value is not thresholded
import pprint
for i in zip(files, sleepdurations):
    pprint.pprint(i)

# print last 5 of files and ids lists
print(files[-5:])
print(ids[-5:])
exit()
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


