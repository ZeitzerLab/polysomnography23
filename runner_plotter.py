import os
import subprocess

# ==========================================================
thresholds = [.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
threads = 128
# ==========================================================


print("Generating CSV Data")

for i in range(len(thresholds)):
    thresholds[i] = str(thresholds[i])

subprocess.run(["python", "generate_append_WASO.py", "--thresholds"] + thresholds)


threads = str(threads)
for threshold in thresholds:
    print("---------  threshold: " + threshold)
    subprocess.run(["python", "all_data_analysis.py", "--threads", threads, "--wasoint", threshold])
    subprocess.run(["python", "feat_imp_plotter.py", "--wasoint", threshold])

