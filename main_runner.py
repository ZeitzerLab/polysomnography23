import subprocess

dur = [True, False]
freq = [True, False]
target = ["REST10", "LTDP10"]

for d in dur:
    for f in freq:
        for t in target:
            if d and f:
                subprocess.run(["python", "main.py", "--isDurationThresholded", "--isFrequencyThresholded", "--target", t])
            elif d:
                subprocess.run(["python", "main.py", "--isDurationThresholded", "--target", t])
            elif f:
                subprocess.run(["python", "main.py", "--isFrequencyThresholded", "--target", t])