import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, f1_score
from sklearn.model_selection import train_test_split
import numpy as np
import os

def train(task, train_path, dev_path, model_path="model.pkl"):
    """
    Train a model for the specified task.

    Args:
        task (str): The task name, one of "penguins", "hotels", or "gss16".
        train_path (str): Path to the training dataset CSV file.
        dev_path (str): Path to the development dataset CSV file.
        model_path (str): Path to save the trained model.
    """
    # Load datasets
    train_df = pd.read_csv(train_path)
    dev_df = pd.read_csv(dev_path)

    if task == "penguins":
        # Features and target for Penguins Classification
        X_train, y_train = train_df.drop(columns=["species"]), train_df["species"]
        X_dev, y_dev = dev_df.drop(columns=["species"]), dev_df["species"]

        model = RandomForestClassifier(random_state=42)
        metric = accuracy_score
        metric_name = "Accuracy"

    elif task == "hotels":
        # Features and target for Hotels Cancellation Prediction
        X_train, y_train = train_df.drop(columns=["canceled"]), train_df["canceled"]
        X_dev, y_dev = dev_df.drop(columns=["canceled"]), dev_df["canceled"]

        model = RandomForestClassifier(random_state=42)
        metric = roc_auc_score
        metric_name = "ROC AUC"

    elif task == "gss16":
        # Features and target for GSS16 Survey Regression
        X_train, y_train = train_df.drop(columns=["wrkstat"]), train_df["wrkstat"]
        X_dev, y_dev = dev_df.drop(columns=["wrkstat"]), dev_df["wrkstat"]

        model = RandomForestRegressor(random_state=42)
        metric = mean_squared_error
        metric_name = "MSE"

    else:
        raise ValueError("Unsupported task. Choose from 'penguins', 'hotels', or 'gss16'.")

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate on development data
    y_pred = model.predict(X_dev)
    if task == "gss16":
        score = metric(y_dev, y_pred)
        print(f"{metric_name} on dev set: {score:.4f}")
    else:
        score = metric(y_dev, y_pred)
        print(f"{metric_name} on dev set: {score:.4f}")

    # Save the model
    import joblib
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")


def predict(task, model_path, input_path, output_path="submission.csv"):
    """
    Predict outcomes using a trained model for the specified task.

    Args:
        task (str): The task name, one of "penguins", "hotels", or "gss16".
        model_path (str): Path to the trained model.
        input_path (str): Path to the input dataset CSV file.
        output_path (str): Path to save the predictions CSV file.
    """
    # Load the model
    import joblib
    model = joblib.load(model_path)

    # Load the input data
    input_df = pd.read_csv(input_path)

    if task == "penguins":
        X = input_df
        target_column = "species"
    elif task == "hotels":
        X = input_df
        target_column = "canceled"
    elif task == "gss16":
        X = input_df
        target_column = "wrkstat"
    else:
        raise ValueError("Unsupported task. Choose from 'penguins', 'hotels', or 'gss16'.")

    # Generate predictions
    predictions = model.predict(X)

    # Save predictions to the output file
    submission = pd.DataFrame({target_column: predictions})
    submission.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")


if __name__ == "__main__":
    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Train or predict for the Data Insights Challenge.")
    parser.add_argument("command", choices=["train", "predict"], help="Whether to train a model or make predictions.")
    parser.add_argument("--task", choices=["penguins", "hotels", "gss16"], required=True, help="Task name.")
    parser.add_argument("--train_path", help="Path to the training dataset CSV file.")
    parser.add_argument("--dev_path", help="Path to the development dataset CSV file.")
    parser.add_argument("--model_path", default="model.pkl", help="Path to save/load the model.")
    parser.add_argument("--input_path", help="Path to the input dataset for predictions.")
    parser.add_argument("--output_path", default="submission.csv", help="Path to save predictions.")
    args = parser.parse_args()

    # Execute the requested command
    if args.command == "train":
        train(args.task, args.train_path, args.dev_path, args.model_path)
    elif args.command == "predict":
        predict(args.task, args.model_path, args.input_path, args.output_path)
