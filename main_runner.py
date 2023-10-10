import subprocess

dur = [True]
freq = [True]
target = ["REST10", "LTDP10"]

for d in dur:
    for f in freq:
        for t in target:
            if d and f:
                subprocess.run(["python", "main.py", "--isDurationThresholded", "--isFrequencyThresholded", "--target", t])
                exit()
            if d:
                subprocess.run(["python", "main.py", "--isDurationThresholded", "--target", t])
                continue
            if f:
                subprocess.run(["python", "main.py", "--isFrequencyThresholded", "--target", t])
                continue
            
            print("==================================================================================================")
            print("==================================================================================================")