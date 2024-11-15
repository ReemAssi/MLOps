# Diamond Price Prediction API

A FastAPI-based application for predicting diamond prices using machine learning models. The application is containerized using Docker for seamless deployment.

## Features
- **Machine Learning Model**: Uses RandomForestRegressor model to predict diamond prices based on various input features (e.g., carat, cut, color, clarity, etc.).
- **FastAPI**: Built using FastAPI for fast and efficient API development.
- **Dockerized**: The entire application is containerized using Docker for easy deployment and portability.
- **Predictions**: API endpoint for making predictions by sending a POST request with the necessary diamond details.

## Docker Hub Repository
You can find the Docker image for this project on Docker Hub at:
[Docker Hub](https://hub.docker.com/repository/docker/reem02/diamond-prediction-api/general)

#### Simply pull and run the image using:
docker pull reem02/diamond-prediction-api:v1

docker run -d -p8000:8000 reem02/diamond-prediction-api:v1 

