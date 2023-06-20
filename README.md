## Polysomnography Analysis 2023

This repo contains Python code for processing and running analysis on polysomnography data.

## How to run analysis

### 1. Install dependencies
Run `pip install -r requirements.txt` to install dependencies.

### 2. Configure parameters
Parameters:
- `thresholds`: WASO window durations to include
- `duration`: Whether to calculate WASO duration
- `frequency`: Whether to calculate WASO frequency
- `cols2drop`: Columns to drop from the dataframe
- `threads`: Number of threads to use for parallel processing