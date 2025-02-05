"""
Module model_training.py - Module for training and saving classification and regression models.
This module loads data, trains models, and saves them to disk.
"""
import json
import os
import pickle
import argparse
import importlib

import pandas as pd
import numpy as np
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split, RandomizedSearchCV

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
        classification_params=None,
        regression_params=None,
        use_grid_search=False
):
    print(f"Starting model training for {model_type}")

    # Use provided paths or default to Config paths
    classification_data_path = classification_data_path or Config.CLASSIFICATION_DATA_PATH
    regression_data_path = regression_data_path or Config.REGRESSION_DATA_PATH

    model_paths = Config.get_model_paths(model_type)

    # Ensure models directory exists
    model_dir = Config.MODELS_DIR / model_type.lower()
    os.makedirs(model_dir, exist_ok=True)
    print(f"Model directory created: {model_dir}")

    metrics_file = model_dir / 'metrics.txt'

    with open(metrics_file, 'w') as f:
        f.write(f"Metrics for {model_type} models\n\n")

        # Classification step
        print("1. Starting classification training...")
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

        ClassifierModel = get_model_class(model_type, 'classification')

        if use_grid_search:
            print("2. Starting randomized search for classification...")
            n_iter = 20
            cv = 5
            classification_params = classification_params or Config.get_default_grid_params(model_type, 'classification')
            random_search_class = RandomizedSearchCV(
                ClassifierModel(),
                classification_params,
                n_iter=n_iter,
                cv=cv,
                n_jobs=-1,
                verbose=2,
                random_state=42
            )
            random_search_class.fit(X_train_class, Y_train_class)
            best_classifier = random_search_class.best_estimator_
            best_params = random_search_class.best_params_
        else:
            print("2. Training classification model with default parameters...")
            best_classifier = ClassifierModel()
            best_classifier.fit(X_train_class, Y_train_class)
            best_params = "Default parameters"

        Y_pred_class = best_classifier.predict(X_test_class)

        accuracy = best_classifier.score(X_test_class, Y_test_class)
        precision = metrics.precision_score(Y_test_class, Y_pred_class)
        recall = metrics.recall_score(Y_test_class, Y_pred_class)
        f1 = metrics.f1_score(Y_test_class, Y_pred_class)

        f.write("Classification Metrics:\n")
        f.write(f"Best Parameters: {best_params}\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n\n")

        print(f"{model_type} Classification Best Parameters:", best_params)
        print(f"Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)

        # Train final classification model on entire dataset
        print("3. Training final classification model on entire dataset...")
        scaler_class = preprocessing.StandardScaler().fit(X_classification)
        X_scaled_class = scaler_class.transform(X_classification)
        final_classifier_model = ClassifierModel(**best_params) if use_grid_search else ClassifierModel()
        final_classifier_model.fit(X_scaled_class, Y_classification)

        print(f"Saving classification model to {model_paths['classification_model']}")
        with open(model_paths['classification_model'], 'wb') as file:
            pickle.dump(final_classifier_model, file)

        print(f"Saving classification scaler to {model_paths['classification_scaler']}")
        with open(model_paths['classification_scaler'], 'wb') as file:
            pickle.dump(scaler_class, file)

        # Regression
        print("\n4. Starting regression training")
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

        RegressorModel = get_model_class(model_type, 'regression')

        if use_grid_search:
            print("5. Starting randomized search for regression")
            n_iter_reg = 50
            cv_reg = 5
            regression_params = regression_params or Config.get_default_grid_params(model_type, 'regression')
            random_search_reg = RandomizedSearchCV(
                RegressorModel(),
                regression_params,
                n_iter=n_iter_reg,
                cv=cv_reg,
                n_jobs=-1,
                verbose=2,
                random_state=42
            )
            random_search_reg.fit(X_train_reg, Y_train_reg)
            best_regressor = random_search_reg.best_estimator_
            best_params_reg = random_search_reg.best_params_
        else:
            print("5. Training regression model with default parameters...")
            best_regressor = RegressorModel()
            best_regressor.fit(X_train_reg, Y_train_reg)
            best_params_reg = "Default parameters"

        Y_pred_reg = best_regressor.predict(X_test_reg)

        r2 = best_regressor.score(X_test_reg, Y_test_reg)
        mae = metrics.mean_absolute_error(Y_test_reg, Y_pred_reg)
        mse = metrics.mean_squared_error(Y_test_reg, Y_pred_reg)
        rmse = np.sqrt(mse)
        evs = metrics.explained_variance_score(Y_test_reg, Y_pred_reg)

        f.write("Regression Metrics:\n")
        f.write(f"Best Parameters: {best_params_reg}\n")
        f.write(f"R2 Score: {r2:.4f}\n")
        f.write(f"MAE: {mae:.4f}\n")
        f.write(f"MSE: {mse:.4f}\n")
        f.write(f"RMSE: {rmse:.4f}\n")
        f.write(f"Explained Variance Score: {evs:.4f}\n")

        print(f"\n{model_type} Regression Best Parameters:", best_params_reg)
        print("R2 Score:", r2)
        print('MAE:', mae)
        print('MSE:', mse)
        print('RMSE:', rmse)
        print('Explained Variance Score:', evs)

        # Train final regression model on entire dataset
        print("6. Training final regression model on entire dataset")
        scaler_reg = preprocessing.StandardScaler().fit(X_regression)
        X_scaled_reg = scaler_reg.transform(X_regression)
        final_regression_model = RegressorModel(**best_params_reg) if use_grid_search else RegressorModel()
        final_regression_model.fit(X_scaled_reg, Y_regression)

        print(f"Saving regression model to {model_paths['regression_model']}")
        with open(model_paths['regression_model'], 'wb') as file:
            pickle.dump(final_regression_model, file)

        print(f"Saving regression scaler to {model_paths['regression_scaler']}")
        with open(model_paths['regression_scaler'], 'wb') as file:
            pickle.dump(scaler_reg, file)

    print("Model training completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and save models for classification and regression.")
    parser.add_argument("--classification_data", type=str, help="Path to the classification dataset")
    parser.add_argument("--regression_data", type=str, help="Path to the regression dataset")
    parser.add_argument("--model_type", type=str, default="RandomForest", help="Type of model to use")
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
        classification_params=classification_params,
        regression_params=regression_params,
        use_grid_search=args.use_grid_search
    )