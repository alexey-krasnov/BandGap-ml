import pickle

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def train_classifier(X_train, Y_train, n_estimators=70, max_features=28):
    classifier = RandomForestClassifier(n_estimators=n_estimators, max_features=max_features, n_jobs=-1, random_state=101)
    classifier.fit(X_train, Y_train)
    return classifier


def train_regressor(X_train, Y_train, n_estimators=200):
    regressor = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1, random_state=101)
    regressor.fit(X_train, Y_train)
    return regressor


def save_model(model, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(model, file)


def load_model(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)
