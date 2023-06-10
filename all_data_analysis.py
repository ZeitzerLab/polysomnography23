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

import wandb
wandb.init(project="visualize-sklearn")


# =================================================
col2drop = ["LTDP10", "REST10", "ESS_s1", "nsrrid"]
target_column = "LTDP10"
filename = "datafullnight2_SE_waso.csv"
# =================================================



def rf_optimizer(xtrain, ytrain):
    # Create the random grid
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.arange(start=50, stop=1000, step=100)]
    n_estimators = [10, 20, 50, 100, 200, 500, 1000]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.arange(2, 100, step=10)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [5, 7, 8, 10, 20]
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
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    rf_regressor = RandomizedSearchCV(estimator=RandomForestRegressor(bootstrap=True), param_distributions=random_grid,
                                      n_iter=25,
                                      cv=5, verbose=1,
                                      random_state=42, n_jobs=30)
    # Fit the random search model
    rf_regressor.fit(xtrain, ytrain)
    pprint(rf_regressor.best_params_)
    return rf_regressor.best_params_

finalarray = ["second interval", "rf_params", "lasso_params", "rf_r^2", "lasso_r^2", "WASO (min)"]

# Importing the dataset
df = pd.read_csv(filename)

print(df)

X = df.drop(columns=col2drop)
y = df.iloc[:, df.columns.get_loc(target_column)].values

output_data = []

xtr, xtest, ytr, ytest = train_test_split(X.values, y, test_size=0.25, random_state=0)

print("RANDOM FOREST PARAMETERS")
rf_params = rf_optimizer(xtr, ytr)
#WASO_2min,WASO_3min,WASO_4min,WASO_5min
# need to repeat with only 1 of these columns in the data
for j in [rf_params.get('n_estimators'), 500, 1000, 1500, 2000, 2500]:
    rf_predictor = RandomForestRegressor(**rf_params)
    rf_predictor.fit(xtr, ytr)
    cols = X.columns

    pprint(len(cols))
    pprint(len(rf_predictor.feature_importances_))

    dict = {rf_predictor.feature_importances_[d]: cols[d] for d in range(0, len(cols))}

    featuredict = OrderedDict(sorted(dict.items()))

    # pprint(featuredict)
    # plt.figure(figsize=(featuredict.values(),featuredict.keys()))
    # plt.bar([featuredict[i][1] for i in range(0, len(featuredict))], [featuredict[i][0] for i in range(0, len(featuredict))])
    plt.bar(featuredict.values(), featuredict.keys())
    plt.title('Feature Importances interval ' + str(i) + ' estimators ' + str(j) + " " + 'sleep_' + str(
        i) + '_renewed.csv')
    # plt.tick_params(axis="x", which="major", pad=10)
    plt.xticks(rotation=90)

    y_pred_rf = rf_predictor.predict(xtest)
    plt.text(0, 0.02, "error:" + str(mean_squared_error(ytest, y_pred_rf)))
    plt.text(0, 0.015, "r2:" + str(np.corrcoef(ytest, y_pred_rf)[0][1]))
    plt.tight_layout()

    # plt.setp(featuredict.values(), rotation=30, horizontalalignment='right')
    plt.savefig(
        'autoscored_eff_plots\\Feature Importances for interval ' + str(i) + ' estimators ' + str(j) + '.png')
    plt.show()

# lasso_predictor = Lasso(**lasso_params)
# lasso_predictor.fit(xtest, ytest)

y_pred_rf = rf_predictor.predict(xtest)
# y_pred_lasso = lasso_predictor.predict(xtest)

rf_coeff = np.corrcoef(ytest, y_pred_rf)[0][1]
# lasso_coeff = np.corrcoef(ytest, y_pred_lasso)[0][1]
#
output_data.append(rf_params)
# output_data.append(lasso_params)
output_data.append(str(rf_coeff))
print(rf_coeff)
# print(lasso_coeff)
# output_data.append(str(lasso_coeff))
#
np.savetxt("autoscored_eff_plots/output_" + str(i) + ".csv", np.asarray(output_data), delimiter=",", fmt='%s')
#
finalarray.append(output_data)

np.savetxt("autoscored_eff_plots/finaldata.csv", np.asarray(finalarray), delimiter=",", fmt='%s')
