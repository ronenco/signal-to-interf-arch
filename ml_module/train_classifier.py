# This file will train the classifier and save the model
# We'll use the RandomForestClassifier from scikit-learn

import os
import sys
import numpy as np
from dataset_generator import generate_dataset
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# These are the libraries for the ML:
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
# To save the model:
import joblib


def main():
    # Parameters:
    num_samples = 1000
    fft_size = 128
    # Generate Dataset
    X, y = generate_dataset(num_samples, fft_size)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Train the RandomForestClassifier:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Print the classification report and accuracy
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Single Tone", "Two Tones", "Noise"]))
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()
    print("Training and saving the model...")