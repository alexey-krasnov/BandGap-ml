import streamlit as st
import pandas as pd
from band_gap_ml.band_gap_predictor import BandGapPredictor
from band_gap_ml.model_training import train_and_save_models
from datetime import datetime


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
    st.warning("Please refresh the page to use newly trained models.")


# Model selection using buttons in a horizontal layout
st.write("### Select Available Trained Model Type For Prediction:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    best_model_btn = st.button('Best Model', key='best_model_btn', use_container_width=True)
with col2:
    rf_btn = st.button('RandomForest', key='rf_btn', use_container_width=True)
with col3:
    gb_btn = st.button('GradientBoosting', key='gb_btn', use_container_width=True)
with col4:
    xgb_btn = st.button('XGBoost', key='xgb_btn', use_container_width=True)

# Determine which model is selected
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'best_model'

if best_model_btn:
    st.session_state.selected_model = 'best_model'
elif rf_btn:
    st.session_state.selected_model = 'RandomForest'
elif gb_btn:
    st.session_state.selected_model = 'GradientBoosting'
elif xgb_btn:
    st.session_state.selected_model = 'XGBoost'

# Display currently selected model
st.info(f"Currently using: **{st.session_state.selected_model}**")

# Initialize predictor with selected model
@st.cache_resource
def get_predictor(model_type):
    return BandGapPredictor(model_type=model_type)

predictor = get_predictor(st.session_state.selected_model)


# Function to handle file download
def download_predictions_as_csv(data_frame, prefix="predicted_band_gaps"):
    """
    Function to create a downloadable CSV file with predictions and timestamp in the filename.

    Parameters:
        data_frame (pd.DataFrame): The data frame containing the predictions.
        prefix (str): Prefix for the file name.
    """
    # Get the current timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    file_name = f"{prefix}_{timestamp}.csv"

    # Convert DataFrame to CSV and create a download button
    csv = data_frame.to_csv(index=False)
    st.download_button(
        label="Download Predictions as CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )

# File upload for CSV
uploaded_file = st.file_uploader("Upload CSV file with chemical formulas written in the first column. ", type=["csv"])
if uploaded_file:
    try:
        input_data = pd.read_csv(uploaded_file)

        # Predict band gaps from the uploaded file
        if st.button('Predict Band Gaps from File'):
            with st.spinner('Predicting band gaps...'):
                predictions = predictor.predict_from_file(input_data=input_data)
                st.write("Predictions from the uploaded file:")
                st.write(predictions)

                # Call the function to allow file download
                download_predictions_as_csv(predictions)

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
        with st.spinner('Predicting band gaps...'):
            predictions = predictor.predict_from_formula(formula=formulas)
            st.write("Predictions for the entered formulas:")
            st.write(predictions)

            # Call the function to allow file download
            download_predictions_as_csv(predictions, prefix="predicted_band_gaps_formulas")

# Add information about the selected model
st.sidebar.header("Model Information")
st.sidebar.write(f"**Selected Model:** {st.session_state.selected_model}")

if st.session_state.selected_model == 'best_model':
    st.sidebar.write("""
    The best model is a RandomForest-based model that has been optimized for band gap prediction.
    """)
elif st.session_state.selected_model == 'RandomForest':
    st.sidebar.write("""
    Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training.
    """)
elif st.session_state.selected_model == 'GradientBoosting':
    st.sidebar.write("""
    Gradient Boosting is a machine learning technique that builds an ensemble of decision trees in a stage-wise fashion.
    """)
elif st.session_state.selected_model == 'XGBoost':
    st.sidebar.write("""
    XGBoost is an optimized distributed gradient boosting library designed to be highly efficient, flexible and portable.
    """)

def show_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f2f2f2;
            color: black;
            text-align: center;
            padding: 5px;
            z-index: 999;
            font-size: 12px;
        }
        .footer a {
            color: #1f77b4;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="footer">
            <p>&copy; 2024 BandGap-ml. Predicting material band gaps based on chemical composition. <br>
            Developed by <a href="https://github.com/alexey-krasnov" target="_blank">Aleksei Krasnov</a>. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

show_footer()