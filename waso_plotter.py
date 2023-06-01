# given all the files, need to plot waso timings with three different thresholds
thresholds = [2, 3, 4, 5] # minutes
# each line in the data represents 15 seconds

import os
import numpy as np
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
    


    



directory_path = Path("donehypnogram")

# Iterate over each file in the directory

# list with 2, 3, 5 min windows
wasoresults = [[], [], [], []]
for filename in tqdm(os.listdir(directory_path)):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        
        wasoresults[0].append(calculate_waso(2, file_path))
        wasoresults[1].append(calculate_waso(3, file_path))
        wasoresults[2].append(calculate_waso(4, file_path))
        wasoresults[3].append(calculate_waso(5, file_path))
    

# # plot the results
# plt.figure(figsize=(10, 10))
# plt.title("WASO for different thresholds")
# plt.xlabel("File number")
# plt.ylabel("WASO (minutes)")
# plt.plot(wasoresults[0], label="2 minutes")
# plt.plot(wasoresults[1], label="3 minutes")
# plt.plot(wasoresults[2], label="5 minutes")
# plt.legend()
# plt.show()

# average waso for each threshold
print("Average waso for 2 minutes: ", np.mean(wasoresults[0]))
print("Average waso for 3 minutes: ", np.mean(wasoresults[1]))
print("Average waso for 4 minutes: ", np.mean(wasoresults[2]))
print("Average waso for 5 minutes: ", np.mean(wasoresults[3]))




