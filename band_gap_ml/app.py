import time
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel

from band_gap_ml.band_gap_predictor import BandGapPredictor

# Start time to calculate loading time
start = time.time()

# Initialize FastAPI app
app = FastAPI(
    title="Band Gap Predictor API",
    description="API for predicting band gaps of materials based on their chemical formulas",
    version="0.3.3"
)

# Initialize the predictor
predictor = BandGapPredictor()

# End time to calculate loading time
end = time.time()
print(f'Band Gap Predictor web service is ready to work...')
print(f"Launching took {time.strftime('%H:%M:%S', time.gmtime(end - start))}")


class FormulaInput(BaseModel):
    formula: Union[str, List[str]]
    model_type: Optional[str] = "best_model"


class PredictionResult(BaseModel):
    composition: str
    is_semiconductor: int
    semiconductor_probability: float
    band_gap: float


@app.post("/predict_bandgap_from_formula", response_model=List[PredictionResult])
async def predict_band_gap(formula_input: FormulaInput):
    """
    Predict band gap for a chemical formula or list of formulas.
    """
    try:
        # Create a new predictor with the specified model type if provided
        if formula_input.model_type != "best_model":
            current_predictor = BandGapPredictor(model_type=formula_input.model_type)
        else:
            current_predictor = predictor

        # Get predictions
        result_df = current_predictor.predict_from_formula(formula_input.formula)

        # Convert DataFrame to list of dictionaries
        predictions = []
        for _, row in result_df.iterrows():
            predictions.append({
                "composition": row["Composition"],
                "is_semiconductor": int(row["is_semiconductor"]),
                "semiconductor_probability": float(row["semiconductor_probability"]),
                "band_gap": float(row["band_gap"])
            })

        return predictions
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")


@app.post("/predict_bandgap_from_file")
async def predict_from_file(file_path: str = Form(...), model_type: Optional[str] = Form("best_model")):
    """
    Predict band gaps from a file containing chemical formulas.
    """
    try:
        # Create a new predictor with the specified model type if provided
        if model_type != "best_model":
            current_predictor = BandGapPredictor(model_type=model_type)
        else:
            current_predictor = predictor

        # Get predictions
        result_df = current_predictor.predict_from_file(file_path)

        # Convert DataFrame to list of dictionaries
        predictions = []
        for _, row in result_df.iterrows():
            predictions.append({
                "composition": row["Composition"],
                "is_semiconductor": int(row["is_semiconductor"]),
                "semiconductor_probability": float(row["semiconductor_probability"]),
                "band_gap": float(row["band_gap"])
            })

        return predictions
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")


@app.get("/healthcheck")
async def healthcheck():
    """
    Check if the server is running.
    """
    return {"status": "Server is up and running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5039)