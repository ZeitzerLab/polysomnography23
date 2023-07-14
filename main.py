import subprocess

# ==========================================================
thresholds = [.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
threads = 128
isDurationThresholded = True
isFrequencyThresholded = True
target = "REST10" # or "LTDP10"
cols2drop = ["WASO (min)"]
# ==========================================================


print("Generating CSV Data")

for i in range(len(thresholds)):
    thresholds[i] = str(thresholds[i])

statcols = ["WASO_interval"]
csvgencommand = ["python", "generate_append_WASO.py"] + ["--thresholds"] + thresholds + ["--cols2drop"] + cols2drop
featimpstatcommand = ["python", "feat_imp_plotter.py"]

if isDurationThresholded:
    csvgencommand.append("--duration_threshold")
    featimpstatcommand.append("--duration")
    statcols.append("duration")
if isFrequencyThresholded:
    csvgencommand.append("--frequency")
    featimpstatcommand.append("--frequency")
    statcols.append("frequency")
subprocess.run(csvgencommand)

with open("stats.csv", "a") as f:
    statcols.append("r^2")
    line = ",".join(statcols)
    f.write(line + "\n")

threads = str(threads)
for threshold in thresholds:
    print("---------  threshold: " + threshold)
    subprocess.run(["python", "all_data_analysis.py", "--threads", threads, "--wasoint", threshold])
    subprocess.run(featimpstatcommand + ["--wasoint", threshold])

