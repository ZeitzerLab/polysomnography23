import pickle
from collections import OrderedDict
from pprint import pprint

import matplotlib.pyplot as plt
# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
import json
import argparse

# =================================================
col2drop = ["LTDP10", "REST10", "ESS_s1", "nsrrid"]
target_column = "LTDP10"
# =================================================


argparser = argparse.ArgumentParser()
argparser.add_argument('--param_file', type=str)
argparser.add_argument('--wasoint', type=int, default=2)

args = argparser.parse_args()
wasointerval = args.wasoint
paramfilepath = args.param_file



finalarray = ["second interval", "rf_params", "lasso_params", "rf_r^2", "lasso_r^2", "WASO (min)"]

# Importing the dataset
filename = "csvdata/datafullnight2_SE_waso" + str(wasointerval) + ".csv"
df = pd.read_csv(filename)



print(df)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

output_data = []

xtr, xtest, ytr, ytest = train_test_split(X.values, y, test_size=0.25, random_state=0)

paramfilepath = "optimized_params/rf_params_wasothreshold" + str(wasointerval) + ".json"
rf_params = json.load(open(paramfilepath, "r"))

# need to plot auc curves for tree depth sizes

test_results = []
train_results = []
max_depths = np.arange(5, 100, step=5)
for max_depth in max_depths:
    rf = RandomForestRegressor(max_depth=max_depth, n_jobs=-1)
    rf.fit(xtr, ytr)
    train_pred = rf.predict(xtr)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(ytr, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    y_pred = rf.predict(xtest)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(ytest, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_depths, train_results, 'b', label="Train AUC")
line2, = plt.plot(max_depths, test_results, 'r', label="Test AUC")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('Tree depth')
plt.show()