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
import json
import argparse

# =================================================
col2drop = ["LTDP10", "REST10", "ESS_s1", "nsrrid"]
target_column = "LTDP10"
# =================================================

argparser = argparse.ArgumentParser()
argparser.add_argument('--wasoint', type=str)
args = argparser.parse_args()
wasoint = args.wasoint



finalarray = ["second interval", "rf_params", "lasso_params", "rf_r^2", "lasso_r^2", "WASO (min)"]

# Importing the dataset
filename = "csvdata/datafullnight2_SE_waso" + str(wasoint) + ".csv"
if wasoint == "0":
    filename = "csvdata/datafullnight2_SE.csv"
df = pd.read_csv(filename)

# print(df)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

xtr, xtest, ytr, ytest = train_test_split(X.values, y, test_size=0.25, random_state=0)

paramfilepath = "optimized_params/rf_params_wasothreshold" + wasoint + ".json"
rf_params = json.load(open(paramfilepath, "r"))

# this is the same as the above, but with the best parameters from the previous step
rf_predictor = RandomForestRegressor(**rf_params)
rf_predictor.fit(xtr, ytr)
cols = X.columns

# pprint(len(cols))
# pprint(len(rf_predictor.feature_importances_))

# wasocolname = "WASO_" + str(wasoint) + "min"

# total = 0
# for i in rf_predictor.feature_importances_:
#     # sum 
#     total += i

# print("total: " + str(total))

# # waso divided by total
# wasoimp = rf_predictor.feature_importances_[cols.get_loc(wasocolname)] / total
# print("waso importance: " + str(wasoimp))

# this gets the feature importances and sorts them
dict = {rf_predictor.feature_importances_[d]: cols[d] for d in range(0, len(cols))}
featuredict = OrderedDict(sorted(dict.items()))

# pprint(featuredict)
# plt.figure(figsize=(featuredict.values(),featuredict.keys()))
# plt.bar([featuredict[i][1] for i in range(0, len(featuredict))], [featuredict[i][0] for i in range(0, len(featuredict))])
plt.bar(featuredict.values(), featuredict.keys())
plt.title('Feature Importances')
# plt.tick_params(axis="x", which="major", pad=10)
plt.xticks(rotation=90)

y_pred_rf = rf_predictor.predict(xtest)
plt.text(0, 0.02, "error:" + str(mean_squared_error(ytest, y_pred_rf)))
plt.text(0, 0.015, "r2:" + str(np.corrcoef(ytest, y_pred_rf)[0][1]))
plt.tight_layout()

# plt.setp(featuredict.values(), rotation=30, horizontalalignment='right')
plt.savefig(
    'featureimpplots/Feature Importances for waso interval ' + str(wasoint) + '.png')
plt.show()