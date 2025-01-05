import streamlit as st
import pandas as pd
from band_gap_ml.band_gap_predictor import predict_eg_from_file, predict_eg_from_formula
from band_gap_ml.model_training import train_and_save_models

# Set title and description
st.title('BandGap-ml: Band Gap Prediction')
st.write("""
    This app allows you to predict the band gap of materials either by uploading a CSV file or by entering chemical formulas.
""")

# Section to train models (optional for users who want to retrain)
train_button = st.button('Train Models')
if train_button:
    st.write("Training models...")
    train_and_save_models()
    st.success("Models trained successfully!")

# File upload for CSV
uploaded_file = st.file_uploader("Upload CSV file with chemical formulas", type=["csv"])
if uploaded_file:
    # Read the file into a pandas DataFrame
    try:
        input_data = pd.read_csv(uploaded_file)

        # Predict band gaps from the uploaded file
        if st.button('Predict Band Gaps from File'):
            # input_data = pd.read_csv(uploaded_file)
            predictions = predict_eg_from_file(input_data=input_data)
            st.write("Predictions from the uploaded file:")

            # Display predictions in a table with formulas
            prediction_df = pd.DataFrame(predictions, columns=["Predicted Band Gap"])
            result_df = pd.concat([input_data, prediction_df], axis=1)
            st.write(result_df)
    except Exception as e:
        st.error(f"Error reading the file: {e}")

# Section for entering chemical formulas
st.subheader("Or, enter chemical formulas manually:")
formulas_input = st.text_area(
    "Enter one or more chemical formulas (separate by commas):",
    "BaLa2In2O7, TiO2, Bi4Ti3O12"
)

if formulas_input:
    formulas = [formula.strip() for formula in formulas_input.split(",")]
    if st.button('Predict Band Gaps from Formulas'):
        predictions = predict_eg_from_formula(formula=formulas)
        st.write("Predictions for the entered formulas:")

        # Display predictions in a table
        prediction_df = pd.DataFrame({"Formula": formulas, "Predicted Band Gap": predictions})
        st.write(prediction_df)
