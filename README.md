## Polysomnography Analysis 2023

This repo contains Python code for processing and running analysis on polysomnography data.

## How to run analysis

Set `thresholds` and `threads` in `runner_plotter.py`, and set the `duration` and `frequency` booleans in `generate_append_WASO.py`. This will include those calculated columns in the output csvs. Then run `runner_plotter.py` to generate the plots and csvs.