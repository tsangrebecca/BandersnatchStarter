import os
import joblib  # save and load Python projects, storing models
from pandas import DataFrame
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from datetime import datetime

class Machine:

    def __init__(self, df: DataFrame):
        # Initialize features and target data
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])

        # Define model
        self.model = RandomForestClassifier()
        self.model.fit(features, target)
        self.initialized_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __call__(self, feature_basis: DataFrame):
        # Use the best model to make a prediction
        prediction = self.model.predict(feature_basis)
        # Return probabilities of each class, and find the highest probability
        probability = self.model.predict_proba(feature_basis).max()

        print(f"Feature Basis: {feature_basis}")  # Print the input features
        print(f"Prediction: {prediction}, Probability: {probability}")

        # Return the first prediction and the highest probability
        return prediction[0], probability

    def save(self, filepath):
        """ Save the best model to a file using joblib """
        # joblib.dump(self.model, 'model.joblib') # 'model.joblib'
        # print(f"Model saved to {filepath}")
        with open(filepath, 'wb') as f:
            joblib.dump((self.model, self.name, self.initialized_at), f)

    @staticmethod
    def open(filepath):
        """ Load a saved model from a file using joblib """
        with open(filepath, 'rb') as file:  # opens file in binary read mode
            data = joblib.load(file)

        # __new__ is a method for creating a new instance of a class quickly
        machine = Machine.__new__(Machine) 
        # assign previously saved model to attributes of the new machine instance
        machine.model = data['model'] 
        machine.name = data['model_name']
        machine.initialized_at = data['initialized_at']
        return machine
        # return joblib.load('model.joblib')

    def info(self):
        """ Return info about the best model and the timestamp when it was initialized """
        return f"Best Model: {self.name}, Initialized at: {self.initialized_at}"
