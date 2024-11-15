import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from model import DiamondPricePredictor


class DiamondFeatures(BaseModel):
    carat: float
    cut: str
    color: str
    clarity: str
    depth: float
    table: float
    x: float
    y: float
    z: float


app = FastAPI()
predictor = DiamondPricePredictor()

# Change the file path to '/app/diamonds.csv' which is the correct path in the Docker container
predictor.load_data('/app/diamonds.csv')
predictor.preprocess_data()
predictor.train()


@app.get("/")
def index():
    return {"message": "Diamond Price Prediction API"}


@app.post("/diamond/predict")
def predict_diamond_price(features: DiamondFeatures):
    input_data = pd.DataFrame([features.dict()])

    input_data = input_data[['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z']]

    # Predict the price using the model
    predicted_price = predictor.predict(input_data)
    return {"predicted_price": predicted_price}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
