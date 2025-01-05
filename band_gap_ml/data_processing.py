import pandas as pd
from sklearn import preprocessing


def load_classification_data(filepath):
    data = pd.read_csv(filepath)
    X = data.values[:, 3:139]
    Y = data.values[:, 2].astype('int')
    return X, Y


def load_regression_data(filepath):
    data = pd.read_csv(filepath)
    X = data.values[:, 2:138]
    Y = data.values[:, 1]
    return X, Y


def preprocess_data(X_train, X_test=None):
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    return X_train_scaled, scaler
