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
filename = "datafullnight2_SE_waso.csv"
# =================================================

import wandb
wandb.init(project="visualize-sklearn")

argparser = argparse.ArgumentParser()
argparser.add_argument('--param_file', type=str)
args = argparser.parse_args()
paramfilepath = args.param_file



finalarray = ["second interval", "rf_params", "lasso_params", "rf_r^2", "lasso_r^2", "WASO (min)"]

# Importing the dataset
df = pd.read_csv(filename)

print(df)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

output_data = []

xtr, xtest, ytr, ytest = train_test_split(X.values, y, test_size=0.25, random_state=0)

rf_params = json.load(open(paramfilepath, "r"))

# this is the same as the above, but with the best parameters from the previous step
rf_predictor = RandomForestRegressor(**rf_params)
rf_predictor.fit(xtr, ytr)
cols = X.columns

pprint(len(cols))
pprint(len(rf_predictor.feature_importances_))

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
    'autoscored_eff_plots\\Feature Importances for waso interval ' + str(input_threshold) + '.png')
plt.show()

np.savetxt("autoscored_eff_plots/output_" + str(input_threshold) + ".csv", np.asarray(output_data), delimiter=",", fmt='%s')

finalarray.append(output_data)

np.savetxt("autoscored_eff_plots/finaldata.csv", np.asarray(finalarray), delimiter=",", fmt='%s')
