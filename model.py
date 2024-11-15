import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


class DiamondPricePredictor:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.label_encoders = {}

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath, index_col=0)
        print(self.data.columns)

    def preprocess_data(self):
        categorical_cols = ['cut', 'color', 'clarity']
        for col in categorical_cols:
            le = LabelEncoder()
            self.data[col] = le.fit_transform(self.data[col])
            self.label_encoders[col] = le  # Save the encoder for future use

        self.X = self.data.drop('price', axis=1)
        self.y = self.data['price']

    def train(self):
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def encode_features(self, features):
        # Only encode 'cut', 'color', 'clarity'
        for col in ['cut', 'color', 'clarity']:
            if col in features.columns:
                features[col] = self.label_encoders[col].transform(features[col])
        return features

    def predict(self, features):
        # Apply encoding to the features
        features = self.encode_features(features)
        # Predict the price for new features
        return float(self.model.predict(features)[0])  # Convert to a serializable type
