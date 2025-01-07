import argparse
import pandas as pd

from band_gap_ml.models import load_model
from band_gap_ml.vectorizer import FormulaVectorizer
from band_gap_ml.config import Config


def load_models_and_scalers():
    """Load models and scalers from pre-saved paths."""
    classifier_model = load_model(Config.CLASSIFICATION_MODEL_PATH)
    regressor_model = load_model(Config.REGRESSION_MODEL_PATH)
    scaler_class = load_model(Config.SCALER_CLASSIFICATION_PATH)
    scaler_reg = load_model(Config.SCALER_REGRESSION_PATH)
    return classifier_model, regressor_model, scaler_class, scaler_reg


def prepare_features(input_data):
    """
    Prepare feature vectors for input chemical formulas using the FormulaVectorizer.

    Parameters:
        input_data (pd.DataFrame): Input data containing a 'Composition' column.

    Returns:
        pd.DataFrame: Transformed feature vectors.
    """
    vectorizer = FormulaVectorizer()
    features = []

    for formula in input_data['Composition']:
        vectorized = vectorizer.vectorize_formula(formula)
        features.append(vectorized)
        # print(f'Formula: {formula}, Vector Length: {len(vectorized)}')  # Debugging line

    X = pd.DataFrame(features, columns=vectorizer.column_names)
    return X


def predict_band_gap(input_data, classifier_model, regressor_model, scaler_class, scaler_reg):
    """
    Predict band gaps using the provided classifier and regressor models.

    Parameters:
        input_data (pd.DataFrame): Feature vectors for chemical formulas.
        classifier_model: Trained classification model.
        regressor_model: Trained regression model.
        scaler_class: Fitted scaler for classification input data.
        scaler_reg: Fitted scaler for regression input data.

    Returns:
        list: Predicted band gaps (regression values or classification results).
    """
    # Scale the data
    X_scaled_class = scaler_class.transform(input_data)
    X_scaled_reg = scaler_reg.transform(input_data)

    # Predict classification and regression results
    classification_result = classifier_model.predict(X_scaled_class)
    regression_result = regressor_model.predict(X_scaled_reg)

    # Combine classification and regression results
    final_result = [
        regression_result[i] if classification_result[i] == 1 else classification_result[i]
        for i in range(len(classification_result))
    ]

    return final_result


def load_input_data(file_path):
    """
    Load input data from a file (CSV or Excel).

    Parameters:
        file_path (str): Path to the input file.

    Returns:
        pd.DataFrame: Input data with 'Composition' column.
    """
    if file_path.endswith('.csv'):
        input_data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        input_data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    return input_data


def predict_eg_from_file(file_path=None, input_data=None):
    """
    Predict band gaps from an input file containing chemical formulas.

    Parameters:
        file_path (str): Path to the input file. Default is None
        input_data (pd.DataFrame, optional): Input data with 'Composition' column. Defaults to None.

    Returns:
        list: Predicted band gaps.
    """
    if file_path:
        # Load input data
        input_data = load_input_data(file_path)

     # Ensure the column for formulas is named 'Composition'
    if 'Composition' not in input_data.columns:
        # Assume the first column contains the formulas
        first_column = input_data.columns[0]
        input_data.rename(columns={first_column: 'Composition'}, inplace=True)
    print(input_data)
    # Prepare feature vectors
    X = prepare_features(input_data)

    # Load models and scalers
    classifier_model, regressor_model, scaler_class, scaler_reg = load_models_and_scalers()

    # Perform prediction
    return predict_band_gap(X, classifier_model, regressor_model, scaler_class, scaler_reg)


def predict_eg_from_formula(formula):
    """
    Predict band gap from a single chemical formula input.

    Parameters:
        formula (str): Chemical formula as a string.

    Returns:
        float or int: Predicted band gap value.
    """
    # Prepare single formula as DataFrame
    input_dict = {'Composition': []}
    if isinstance(formula, list):
        input_dict['Composition'].extend(formula)
        input_data = pd.DataFrame(input_dict)
        print(input_data)
    elif isinstance(formula, str):
        input_dict['Composition'].append(formula)
        input_data = pd.DataFrame(input_dict)
    X = prepare_features(input_data)

    # Load models and scalers
    classifier_model, regressor_model, scaler_class, scaler_reg = load_models_and_scalers()

    # Perform prediction and return results
    return predict_band_gap(X, classifier_model, regressor_model, scaler_class, scaler_reg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Band Gap from Chemical Formula or File')
    parser.add_argument('--file', type=str, help='Path to input file (csv/excel) with chemical formulas')
    parser.add_argument('--formula', type=str, help='Single chemical formula for prediction')

    args = parser.parse_args()

    if args.file:
        predictions = predict_eg_from_file(args.file)
        print("Predictions from file:", predictions)

    if args.formula:
        prediction = predict_eg_from_formula(args.formula)
        print(f"Prediction for formula '{args.formula}':", prediction)
