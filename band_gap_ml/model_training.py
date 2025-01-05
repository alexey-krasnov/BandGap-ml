"""
Module model_training.py
"""
import os
import pickle
import argparse

import pandas as pd
from sklearn import preprocessing, metrics
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

from band_gap_ml.config import Config


def train_and_save_models(
        classification_data_path=None,
        regression_data_path=None,
        classification_model_path=None,
        scaler_classification_path=None,
        regression_model_path=None,
        scaler_regression_path=None,
):
    """
    Train and save classification and regression models using RandomForestClassifier and RandomForestRegressor, respectively.

    Args:
        classification_data_path (str, optional): Path to the CSV file with classification data. Defaults to Config.CLASSIFICATION_DATA_PATH.
        regression_data_path (str, optional): Path to the CSV file with regression data. Defaults to Config.REGRESSION_DATA_PATH.
        classification_model_path (str, optional): Path to save the classification model. Defaults to Config.CLASSIFICATION_MODEL_PATH.
        scaler_classification_path (str, optional): Path to save the scaler for classification data. Defaults to Config.SCALER_CLASSIFICATION_PATH.
        regression_model_path (str, optional): Path to save the regression model. Defaults to Config.REGRESSION_MODEL_PATH.
        scaler_regression_path (str, optional): Path to save the scaler for regression data. Defaults to Config.SCALER_REGRESSION_PATH.

    Returns:
        None
    """

    # Use provided paths or default to Config paths
    classification_data_path = classification_data_path or Config.CLASSIFICATION_DATA_PATH
    regression_data_path = regression_data_path or Config.REGRESSION_DATA_PATH
    classification_model_path = classification_model_path or Config.CLASSIFICATION_MODEL_PATH
    scaler_classification_path = scaler_classification_path or Config.SCALER_CLASSIFICATION_PATH
    regression_model_path = regression_model_path or Config.REGRESSION_MODEL_PATH
    scaler_regression_path = scaler_regression_path or Config.SCALER_REGRESSION_PATH

    # Ensure models directory exists
    os.makedirs(Config.MODELS_DIR, exist_ok=True)

    # Classification
    classification_data = pd.read_csv(classification_data_path)
    classification_array = classification_data.values
    X_classification = classification_array[:, 3:139]
    Y_classification = classification_array[:, 2].astype('int')

    X_train_class, X_test_class, Y_train_class, Y_test_class = train_test_split(
        X_classification, Y_classification, test_size=0.2, random_state=15, shuffle=True
    )

    scaler_class = preprocessing.StandardScaler().fit(X_train_class)
    X_train_class = scaler_class.transform(X_train_class)
    X_test_class = scaler_class.transform(X_test_class)

    classifier_model = RandomForestClassifier(
        n_estimators=70, max_features=28, n_jobs=-1, random_state=101
    ).fit(X_train_class, Y_train_class)
    Y_pred_class = classifier_model.predict(X_test_class)

    print("Random Forest Classification Accuracy:", classifier_model.score(X_test_class, Y_test_class))
    print("Precision:", metrics.precision_score(Y_test_class, Y_pred_class))
    print("Recall:", metrics.recall_score(Y_test_class, Y_pred_class))
    print("F1 Score:", metrics.f1_score(Y_test_class, Y_pred_class))

    scaler_class = preprocessing.StandardScaler().fit(X_classification)
    X_scaled_class = scaler_class.transform(X_classification)
    final_classifier_model = RandomForestClassifier(
        n_estimators=70, max_features=28, n_jobs=-1, random_state=101
    ).fit(X_scaled_class, Y_classification)

    with open(classification_model_path, 'wb') as file:
        pickle.dump(final_classifier_model, file)

    with open(scaler_classification_path, 'wb') as file:
        pickle.dump(scaler_class, file)

    # Regression
    regression_data = pd.read_csv(regression_data_path)
    regression_array = regression_data.values
    X_regression = regression_array[:, 2:138]
    Y_regression = regression_array[:, 1]

    X_train_reg, X_test_reg, Y_train_reg, Y_test_reg = train_test_split(
        X_regression, Y_regression, test_size=0.2, random_state=101, shuffle=True
    )

    scaler_reg = preprocessing.StandardScaler().fit(X_train_reg)
    X_train_reg = scaler_reg.transform(X_train_reg)
    X_test_reg = scaler_reg.transform(X_test_reg)

    regressor_model = RandomForestRegressor(n_estimators=200, n_jobs=-1, random_state=101).fit(X_train_reg, Y_train_reg)
    Y_pred_reg = regressor_model.predict(X_test_reg)

    print("\nRandom Forest Regression Accuracy:", regressor_model.score(X_test_reg, Y_test_reg))
    print('MAE:', metrics.mean_absolute_error(Y_test_reg, Y_pred_reg))
    print('MSE:', metrics.mean_squared_error(Y_test_reg, Y_pred_reg))
    print('RMSE:', metrics.mean_squared_error(Y_test_reg, Y_pred_reg, squared=False))
    print('Explained Variance Score:', metrics.explained_variance_score(Y_test_reg, Y_pred_reg))
    print('Mean Squared Log Error:', metrics.mean_squared_log_error(Y_test_reg, Y_pred_reg))
    print('Median Absolute Error:', metrics.median_absolute_error(Y_test_reg, Y_pred_reg))

    scaler_reg = preprocessing.StandardScaler().fit(X_regression)
    X_scaled_reg = scaler_reg.transform(X_regression)
    final_regression_model = RandomForestRegressor(n_estimators=200, n_jobs=-1, random_state=101).fit(X_scaled_reg, Y_regression)

    with open(regression_model_path, 'wb') as file:
        pickle.dump(final_regression_model, file)

    with open(scaler_regression_path, 'wb') as file:
        pickle.dump(scaler_reg, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and save models for classification and regression.")
    parser.add_argument("--classification_data", type=str, help="Path to the classification dataset")
    parser.add_argument("--regression_data", type=str, help="Path to the regression dataset")
    parser.add_argument("--classification_model", type=str, help="Path to save the classification model")
    parser.add_argument("--scaler_classification", type=str, help="Path to save the classification scaler")
    parser.add_argument("--regression_model", type=str, help="Path to save the regression model")
    parser.add_argument("--scaler_regression", type=str, help="Path to save the regression scaler")

    args = parser.parse_args()

    train_and_save_models(
        classification_data_path=args.classification_data,
        regression_data_path=args.regression_data,
        classification_model_path=args.classification_model,
        scaler_classification_path=args.scaler_classification,
        regression_model_path=args.regression_model,
        scaler_regression_path=args.scaler_regression,
    )
