"""
FastAPI web service for predicting band gaps of materials based on their chemical formulas.

The API accepts chemical formulas as input and returns the predicted band gaps along with classification probabilities.

"""
import io
import pandas as pd
import time
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the predictor
predictor = BandGapPredictor()

# End time to calculate loading time
end = time.time()
print(f'Band Gap Predictor web service is ready to work...')
print(f"Launching took {time.strftime('%H:%M:%S', time.gmtime(end - start))}")


class PredictionResult(BaseModel):
    composition: str
    is_semiconductor: int
    semiconductor_probability: float
    band_gap: float

@app.post("/predict_bandgap", response_model=List[PredictionResult])
async def predict_band_gap(
        formula: Optional[Union[str, List[str]]] = Form(None),
        model_type: Optional[str] = Form("best_model"),
        file: Optional[UploadFile] = File(None)
):
    try:
        current_predictor = BandGapPredictor(model_type=model_type) if model_type != "best_model" else predictor

        if file:
            # Handle file upload
            contents = await file.read()
            if file.filename.endswith('.csv'):
                input_data = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            elif file.filename.endswith('.xlsx'):
                input_data = pd.read_excel(io.BytesIO(contents))
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
            result_df = current_predictor.predict_from_file(input_data=input_data)
        elif formula:
            result_df = current_predictor.predict_from_formula(formula)
        else:
            raise ValueError("Please provide either a formula or a file.")

        # Convert DataFrame to list of dictionaries
        predictions = []
        for _, row in result_df.iterrows():
            predictions.append({
                "composition": str(row["Composition"]),
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
    uvicorn.run(app, host="127.0.0.1", port=3000)