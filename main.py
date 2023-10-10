import subprocess

# ==========================================================
thresholds = [.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
threads = 128
# isDurationThresholded = False
# isFrequencyThresholded = True
# target = "REST10" # or "LTDP10"
cols2drop = ["WASO (min)", "S?W shifts"] #TODO: double check whether we should drop these columns
# ==========================================================

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('--isDurationThresholded', action='store_true')
argparser.add_argument('--isFrequencyThresholded', action='store_true')
argparser.add_argument('--rf', action="store_true")
argparser.add_argument('--target', type=str)

args = argparser.parse_args()

isDurationThresholded = args.isDurationThresholded
isFrequencyThresholded = args.isFrequencyThresholded
doRFAnalysis = args.rf
target = args.target

print("Generating CSV Data")

for i in range(len(thresholds)):
    thresholds[i] = str(thresholds[i])

statcols = ["WASO_interval"]
csvgencommand = ["python", "generate_append_WASO.py"] + ["--thresholds"] + thresholds + ["--cols2drop"] + cols2drop
featimpstatcommand = ["python", "feat_imp_plotter.py"]

if isDurationThresholded:
    csvgencommand.append("--duration_threshold")
if isFrequencyThresholded:
    csvgencommand.append("--frequency_threshold")
subprocess.run(csvgencommand)

statcols.append("WASO")
statcols.append("SW_shifts")

statfilename = "stats"
if isDurationThresholded:
    statfilename += "_wasothresholded"
if isFrequencyThresholded:
    statfilename += "_swshiftsthresholded"

statfilename += "_" + target + ".csv"

# with open(statfilename, "a") as f:
#     statcols.append("r^2")
#     line = ",".join(statcols)
#     f.write(line + "\n")

if doRFAnalysis:
    threads = str(threads)
    for threshold in thresholds:
        print("---------  threshold: " + threshold)
        subprocess.run(["python", "all_data_analysis.py", "--threads", threads, "--wasoint", threshold, "--targetcol", target])
        subprocess.run(featimpstatcommand + ["--wasoint", threshold, "--filename", statfilename, "--target_column", target])

