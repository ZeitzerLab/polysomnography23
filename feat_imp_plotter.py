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
col2drop = ["LTDP10", "REST10", "ESS_s1", "nsrrid", "TIMEINBED_mins"]
# =================================================

argparser = argparse.ArgumentParser()
argparser.add_argument('--wasoint', type=str)
argparser.add_argument('--filename', type=str)
argparser.add_argument('--target_column', type=str)
args = argparser.parse_args()
wasoint = args.wasoint
statfilename = args.filename
target_column = args.target_column




# Importing the dataset
filename = "csvdata/datafullnight2_SE_waso" + str(wasoint) + ".csv"
if wasoint == "0":
    filename = "csvdata/datafullnight2_SE.csv"

print("Generating statistics for: " + filename)
df = pd.read_csv(filename)

print(df.columns)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

print(np.argwhere(np.isnan(X)))
print(np.argwhere(np.isnan(y)))

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
print(dict)
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

pltname = "featureimpplots/" + "featimp_" + statfilename.split(".")[0] + "_" + str(wasoint) + '.png'

plt.savefig(pltname)
# plt.show()

# this will just print the feature importances to a csv file

line = str(wasoint)

wasodurimp = [rf_predictor.feature_importances_[d] for d in range(0, len(cols)) if "WASO_min" in cols[d]][0]
line += "," + str(wasodurimp)
wasofreqimp = [rf_predictor.feature_importances_[d] for d in range(0, len(cols)) if "StoWfreq" in cols[d]][0]
line += "," + str(wasofreqimp)

with open(statfilename, "a") as f:
    f.write(line + "," + str(np.corrcoef(ytest, y_pred_rf)[0][1]) + "\n")
