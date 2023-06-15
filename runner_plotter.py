import os
import subprocess
thresholds = [.25, 0.5, 0.75, 1, 2, 3, 4, 5, 10]

for threshold in thresholds:
    print("---------  threshold: " + str(threshold))
    # subprocess.run(["python", "all_data_analysis.py", "--threads", "128", "--wasoint", str(threshold)])
    subprocess.run(["python", "feat_imp_plotter.py", "--wasoint", str(threshold)])

