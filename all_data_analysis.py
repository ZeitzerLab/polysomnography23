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
col2drop = ["LTDP10", "REST10", "ESS_s1", "nsrrid"] # these are all the response variables
target_column = "LTDP10"
# =================================================

# import wandb
# wandb.init(project="visualize-sklearn")

argparser = argparse.ArgumentParser()
argparser.add_argument('--wasoint', default=2)
argparser.add_argument('--threads', type=int, default=32)
args = argparser.parse_args()
wasointerval = args.wasoint
threads = args.threads

def rf_optimizer(xtrain, ytrain):
    # Create the random grid
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.arange(start=50, stop=200, step=50)]
    n_estimators = [10, 20, 50, 100, 200, 500, 1000]
    # Number of features to consider at every split
    max_features = [1.0, "sqrt", 0.5]
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.arange(2, 100, step=10)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [1, 2, 3, 4, 5, 7, 8]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [2, 4, 8, 12]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf}
    
    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    # Random search of parameters, using 5 fold cross validation,
    # search across 100 different combinations, and use all available cores
    rf_regressor = RandomizedSearchCV(estimator=RandomForestRegressor(bootstrap=True), param_distributions=random_grid,
                                      n_iter=100,
                                      cv=5, verbose=3,
                                      random_state=42, n_jobs=threads)

        
    # Fit the random search model
    rf_regressor.fit(xtrain, ytrain)
    pprint(rf_regressor.best_params_)

    print("CV RESULTS")
    cv_results_df = pd.DataFrame(rf_regressor.cv_results_)

    # sort by rank_test_score descending
    cv_results_df.sort_values(by=['rank_test_score'], inplace=True, ascending=False)

    # Export the DataFrame to a CSV file
    cv_results_df.to_csv('cv_results.csv', index=False)

    # wandb.sklearn.plot_learning_curve(rf_regressor.best_estimator_, xtrain, ytrain)
    return rf_regressor.best_params_

finalarray = ["second interval", "rf_params", "lasso_params", "rf_r^2", "lasso_r^2", "WASO (min)"]

# Importing the dataset
# create the filename
filename = "csvdata/datafullnight2_SE_waso" + str(wasointerval) + ".csv"
if wasointerval == 0:
    filename = "csvdata/datafullnight2_SE.csv"

df = pd.read_csv(filename)

print(df)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

xtr, xtest, ytr, ytest = train_test_split(X.values, y, test_size=0.25, random_state=0)

print("RANDOM FOREST PARAMETER OPTIMIZATION")   
rf_params = rf_optimizer(xtr, ytr)

# rf_params is json
# write to file
with open('optimized_params/rf_params_wasothreshold' + str(wasointerval) + '.json', 'w') as fp:
    json.dump(rf_params, fp)