import os
import joblib  # save and load Python projects, storing models
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

# Define a class Machine to encapsulate model training, prediction,
#   saving, loading and info about the model
class Machine:
    # Constructor method to initialize the Machine object with a dataset (df)
    def __init__(self, df: DataFrame):
        # Initialize features and target data
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])

        # Define model and best params
        self.model = RandomForestClassifier(max_depth=30, max_features='sqrt', min_samples_leaf=1, min_samples_split=2, 
                                            n_estimators=200, random_state=42, n_jobs=-1)
        self.model.fit(features, target)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # This method is used to make the class instance behave like a callable function
    # Instead of machine.predict(feature_basis), we can directly use machine(feature_basis)
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
        with open(filepath, 'wb') as f:
            # Saves data to the file object f
            joblib.dump((self.model, self.name, self.timestamp), f)

    # Decorator to indicate that open is a static method, that it can be
    #   called directly on the class Machine (e.g. Machine.open(filepath)) w/o
    #   requiring an instance of Machine
    @staticmethod 
    def open(filepath):
        with open(filepath, 'rb') as f:
            model, name, timestamp = joblib.load(f) # unpack data into 3 variables

        # create a new instance without calling __init__ to prevent re-running any setup code in __init__
        instance = Machine.__new__(Machine) 
        # Assign loaded values to the instance attributes
        instance.model = model
        instance.name = name
        instance.timestamp = timestamp
        return instance # newly created Machine instance

    def info(self):
        """ Return info about the best model and the timestamp when it was initialized """
        return f"Best Model: {self.name}, Initialized at: {self.timestamp}"