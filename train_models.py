"""

This files trains a range of modesl with a given training set and chooses the best

"""

from sklearn import svm
import log

from sklearn.ensemble import GradientBoostingRegressor
import sklearn.metrics as met
from sklearn import svm
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR

# Import Linear Regression and a regularized regression function
from sklearn.linear_model import LassoCV
# Finally, import function to make a machine learning pipeline
from sklearn.linear_model import SGDRegressor
from sklearn import linear_model
import numpy as np
from sklearn.linear_model import Ridge



"""

currently not using ,
               "MultiTaskElasticNet"

"""

model_names = ["GradientBoostingRegressor",
               "LinearRegression",
               "SupportVectorRegression",
               "DecisionTreeRegressor",
               "MLPRegressor",
               "SGDRegressor",
               "Lasso",
               "SVR",
               "Ridge"
               ]



def get_result_MSE(y_true, y_predicted):

    err = met.mean_squared_error(y_true, y_predicted)

    #err = met.r2_score(y_true, prediction_result)
    err = np.sqrt(err)

    return err

def train_and_choose_best(X_train, X_test, y_train, y_test):

    global model_names
    first_row = True
    best_model = None
    best_model_name = None
    best_error = None
    y_test_best = []
    y_predicted_best = []

    for model in model_names:

        # get model and train it
        model_obj = train_model(model, X_train, y_train)

        y_predicted = predict_model(model_obj, X_test)

        # test error
        this_model_error = get_result_MSE(y_test, y_predicted)

        log.log_prediction("model: " + model + ", error = " + str(this_model_error))

        # check if better, otherwise ignore

        if first_row:

            best_error = this_model_error
            best_model = model_obj
            best_model_name = model

            first_row = False
        else:
            if this_model_error < best_error:

                best_error = this_model_error
                best_model = model_obj
                best_model_name = model
                y_test_best = y_test
                y_predicted_best = y_predicted

    log.log_prediction("best model: " + best_model_name)

    for i in range(len(y_test_best)):

        s = "predicted:; " + str(y_predicted_best[i])
        s += ";truth:; " + str(y_test_best[i])
        log.log_prediction(s)


    return best_model


def predict_model(model, X):

    prediction_result = model.predict(X)
    return prediction_result


def train_model(m, x, y):

    if m == "GradientBoostingRegressor":
        model = train_gradient_boosting_regressor(x, y)
    if m == "LinearRegression":
        model = train_linear_regression(x, y)
    if m == "SupportVectorRegression":
        model = train_support_vector_regression(x, y)
    if m == "DecisionTreeRegressor":
        model = train_decision_tree_regressor(x, y)
    if m == "MLPRegressor":
        model = train_neural_network(x, y)
    if m == "SGDRegressor":
        model = train_SGDRegressor(x, y)
    if m == "Lasso":
        model = train_Lasso(x, y)
    if m == "SVR":
        model = train_SVR(x, y)
    if m == "Ridge":
        model = train_Ridge(x, y)
    if m == "MultiTaskElasticNet":
        model = train_MultiTaskElasticNet(x, y)

    return model



def train_MultiTaskElasticNet(X_train, y_train):
    model = linear_model.MultiTaskElasticNet(alpha=0.1)
    model.fit(X_train, y_train)
    return model

def train_Ridge(X_train, y_train):

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    return model


def train_SVR(X_train, y_train):

    model = SVR(C=1.0, epsilon=0.2)
    model.fit(X_train, y_train)
    return model


def train_Lasso(X_train, y_train):

    model = linear_model.Lasso(alpha=0.1)
    model.fit(X_train, y_train)
    return model


def train_SGDRegressor(X_train, y_train):

    model = SGDRegressor()
    model.fit(X_train, y_train)
    return model


def train_neural_network(X_train, y_train):

    model = MLPRegressor()
    model.fit(X_train, y_train)
    return model


def train_decision_tree_regressor(X_train, y_train):

    model = tree.DecisionTreeRegressor()
    model.fit(X_train, y_train)
    return model


def train_support_vector_regression(X_train, y_train):

    model = svm.SVR()
    model.fit(X_train, y_train)
    return model


def train_linear_regression(X_train, y_train):

    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_gradient_boosting_regressor(X_train, y_train):

    model = GradientBoostingRegressor(n_estimators=100, max_depth=10, random_state=1)
    model.fit(X_train, y_train)
    return model

