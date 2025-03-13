"""
Module model_training.py - Module for training and saving classification and regression models.
This module loads data, trains models, and saves them to disk.
"""
import json
import pickle
import argparse
import importlib
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split, GridSearchCV

from band_gap_ml.config import Config


def get_model_class(model_type, task):
    """Get the model class and import the corresponding module based on the given model type and task."""
    module_path, class_name = Config.MODEL_TYPES.get(model_type).get(task).rsplit('.', maxsplit=1)
    print(f"Importing {class_name} from {module_path}")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def train_and_save_models(
        classification_data_path=None,
        regression_data_path=None,
        model_type='RandomForest',
        model_dir=None,
        classification_params=None,
        regression_params=None,
        use_grid_search=False
):
    print(f"Starting model training for {model_type}")

    # 1. Use provided paths or default Config paths to the DATA files
    classification_data_path = classification_data_path or Config.CLASSIFICATION_DATA_PATH
    regression_data_path = regression_data_path or Config.REGRESSION_DATA_PATH

    if model_dir:
        model_dir = Path(model_dir)

    # Create a unique folder with timestamp for saving models and scalers
    model_dir = Config.create_model_type_directory(model_type, model_dir)

    models_statistics_file = model_dir / 'models_statistics.json'

    classification_params = classification_params or Config.DEFAULT_GRID_PARAMS.get(model_type, {}).get('classification')
    # Classification step
    classification_results = train_classification_model(
        classification_data_path, model_type, use_grid_search, classification_params
    )

    regression_params = regression_params or Config.DEFAULT_GRID_PARAMS.get(model_type, {}).get('regression')
    # Regression step
    regression_results = train_regression_model(
        regression_data_path, model_type, use_grid_search, regression_params
    )

    models_statistics = {
        "model_type": model_type,
        "use_grid_search": use_grid_search,
        "classification": {
            "best_params": classification_results["best_params"],
            "metrics": classification_results["metrics"]
        },
        "regression": {
            "best_params": regression_results["best_params"],
            "metrics": regression_results["metrics"]
        }
    }

    # Save models and scalers
    save_models_and_scalers(model_dir, classification_results, regression_results)

    # Save model statistics to json file
    with open(models_statistics_file, 'w') as file:
        json.dump(models_statistics, file, indent=4)

    print("Model training completed successfully")
    return models_statistics


def train_classification_model(data_path, model_type, use_grid_search, params):
    print("1. Start training of classifier ...")
    classification_data = pd.read_csv(data_path)
    X_classification = classification_data.iloc[:, 3:139].values
    Y_classification = classification_data.iloc[:, 2].astype('int').values

    X_train, X_test, Y_train, Y_test = train_test_split(
        X_classification, Y_classification, test_size=0.2, random_state=15, shuffle=True
    )

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    ClassifierModel = get_model_class(model_type, 'classification')

    if use_grid_search:
        best_classifier, best_params = perform_grid_search(ClassifierModel, X_train_scaled, Y_train, params, 'classification')

    else:
        best_classifier = ClassifierModel()
        best_classifier.fit(X_train_scaled, Y_train)
        best_params = "Default parameters"

    Y_pred = best_classifier.predict(X_test_scaled)

    metrics_dict = calculate_classification_metrics(Y_test, Y_pred)
    print_classification_metrics(model_type, best_params, metrics_dict)

    # Train final model on entire dataset
    X_scaled = scaler.fit_transform(X_classification)
    final_model = ClassifierModel(**best_params) if use_grid_search else ClassifierModel()
    final_model.fit(X_scaled, Y_classification)

    return {
        "best_params": best_params,
        "metrics": metrics_dict,
        "final_model": final_model,
        "scaler": scaler
    }


def train_regression_model(data_path, model_type, use_grid_search, params):
    print("\n4. Start training regressor...")
    regression_data = pd.read_csv(data_path)
    X_regression = regression_data.iloc[:, 2:138].values
    Y_regression = regression_data.iloc[:, 1].values

    X_train, X_test, Y_train, Y_test = train_test_split(
        X_regression, Y_regression, test_size=0.2, random_state=101, shuffle=True
    )

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    RegressorModel = get_model_class(model_type, 'regression')

    if use_grid_search:
        best_regressor, best_params = perform_grid_search(RegressorModel, X_train_scaled, Y_train, params, 'regression')
    else:
        best_regressor = RegressorModel()
        best_regressor.fit(X_train_scaled, Y_train)
        best_params = "Default parameters"

    Y_pred = best_regressor.predict(X_test_scaled)

    metrics_dict = calculate_regression_metrics(Y_test, Y_pred)
    print_regression_metrics(model_type, best_params, metrics_dict)

    # Train final model on entire dataset
    X_scaled = scaler.fit_transform(X_regression)
    final_model = RegressorModel(**best_params) if use_grid_search else RegressorModel()
    final_model.fit(X_scaled, Y_regression)

    return {
        "best_params": best_params,
        "metrics": metrics_dict,
        "final_model": final_model,
        "scaler": scaler
    }

def perform_grid_search(Model, X, y, params, task):
    print(f"Starting grid search for {task}...")
    cv = 5
    params = params or Config.get_default_grid_params(Model.__name__, task)
    grid_search = GridSearchCV(
        Model(), params, cv=cv, n_jobs=-1, verbose=2
    )
    grid_search.fit(X, y)
    print(f"Best score: {grid_search.best_score_}")
    print(f"Best parameters: {grid_search.best_params_}")
    return grid_search.best_estimator_, grid_search.best_params_


def calculate_classification_metrics(y_true, y_pred):
    return {
        "accuracy": metrics.accuracy_score(y_true, y_pred),
        "precision": metrics.precision_score(y_true, y_pred),
        "recall": metrics.recall_score(y_true, y_pred),
        "f1_score": metrics.f1_score(y_true, y_pred)
    }


def calculate_regression_metrics(y_true, y_pred):
    mse = metrics.mean_squared_error(y_true, y_pred)
    return {
        "r2_score": metrics.r2_score(y_true, y_pred),
        "mae": metrics.mean_absolute_error(y_true, y_pred),
        "mse": mse,
        "rmse": np.sqrt(mse),
        "explained_variance_score": metrics.explained_variance_score(y_true, y_pred)
    }


def print_classification_metrics(model_type, best_params, metrics_dict):
    print(f"{model_type} Classification Best Parameters: {best_params}\n")
    for metric, value in metrics_dict.items():
        print(f"{metric.capitalize()}: {value}")


def print_regression_metrics(model_type, best_params, metrics_dict):
    print(f"\n{model_type} Regression Best Parameters: {best_params}\n")
    for metric, value in metrics_dict.items():
        print(f"{metric.upper()}: {value}")


def save_models_and_scalers(model_dir, classification_results, regression_results):
    for task in ['classification', 'regression']:
        results = classification_results if task == 'classification' else regression_results
        for item in ['model', 'scaler']:
            path = model_dir / f'{task}_{item}.pkl'
            obj = results['final_model'] if item == 'model' else results['scaler']
            print(f"Saving {task} {item} to {path}")
            with open(path, 'wb') as file:
                pickle.dump(obj, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and save models for classification and regression.")
    parser.add_argument("--classification_data", type=str, help="Path to the classification dataset")
    parser.add_argument("--regression_data", type=str, help="Path to the regression dataset")
    parser.add_argument("--model_type", type=str, default="RandomForest", help="Type of model to use")
    parser.add_argument("--model_dir", type=str, default="models", help="Directory to save models and scalers")
    parser.add_argument("--classification_params", type=str, help="JSON string of classification model parameters for grid search")
    parser.add_argument("--regression_params", type=str, help="JSON string of regression model parameters for grid search")
    parser.add_argument("--use_grid_search", type=bool, default=True, help="Whether to use grid search or not")

    args = parser.parse_args()

    print("Parsed arguments:", args)

    # Parse JSON strings to dictionaries if provided
    classification_params = json.loads(args.classification_params) if args.classification_params else None
    regression_params = json.loads(args.regression_params) if args.regression_params else None

    train_and_save_models(
        classification_data_path=args.classification_data,
        regression_data_path=args.regression_data,
        model_type=args.model_type,
        model_dir=args.model_dir,
        classification_params=classification_params,
        regression_params=regression_params,
        use_grid_search=args.use_grid_search
    )