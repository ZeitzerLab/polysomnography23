import os

def remove_leading_zeros(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    leading_zeros_removed = False
    consecutive_ones_count = 0

    for line in lines:
        digit = int(line.strip())

        # if not leading_zeros_removed and digit == 1:
        #     if consecutive_ones_count == 6:
        #         leading_zeros_removed = True
        #         # add 6 ones to the modified lines
        #         modified_lines.extend(['1'] * 6)
        #         continue
        #     consecutive_ones_count += 1
        # elif not leading_zeros_removed and (digit != 0 and digit != 1):
        #     leading_zeros_removed = True
        #     modified_lines.append(str(digit))
        # elif not leading_zeros_removed and digit == 0:
        #     continue
        # else:
        #     modified_lines.append(str(digit))

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

from pathlib import Path
from tqdm import tqdm

directory_path = Path("hypnogramFiles\donehypnogram")

# Iterate over each file in the directory
for filename in tqdm(os.listdir(directory_path)):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        remove_leading_zeros(file_path)
