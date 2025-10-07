#uses sys path to get python path since I had issues with libraries not being found despite correct python interpreter
import os
import sys
sys.path.append(
    os.path.abspath('/Users/matthewthompson/Documents/Academics/DS Masters Academics/Foundation of Data Science/Final Project/final-project-BlueFlashX1/venv/lib/python3.13/site-packages/')
)

#===========================

#list of imports 
import argparse
import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline          import Pipeline
from sklearn.compose           import ColumnTransformer
from sklearn.preprocessing     import OneHotEncoder, StandardScaler
from sklearn.ensemble          import RandomForestClassifier
from sklearn.metrics           import roc_auc_score

#==============================

def train(train_path, dev_path, model_path="model.pkl"):
    # reads both train and dev data
    train_df = pd.read_csv(train_path)
    dev_df   = pd.read_csv(dev_path)

    # adds the patient frequency count (frequency encode)
    train_df['patient_freq'] = train_df.groupby('patient_id')['patient_id'].transform('count')
    dev_df  ['patient_freq'] = dev_df.groupby('patient_id')['patient_id'].transform('count')

    # dropped unnecessary columns that may not meaningfully contribute to predicting readmission within 30 days
    drop_cols = [
        'encounter_id',
        'patient_id',
        'readmitted_within_30_days_frequency', #just in case 
        'has_chronic_pain',
        'has_hypertension',
        'has_diabetes',
        'has_asthma',
        'has_depression'
    ]
    train_df = train_df.drop(columns=drop_cols, errors='ignore')
    dev_df   = dev_df.drop(columns=drop_cols,   errors='ignore')

    # separates feature and targets
    y_train = train_df['readmitted_within_30_days'].astype(int)
    X_train = train_df.drop(columns=['readmitted_within_30_days'])

    y_dev   = dev_df['readmitted_within_30_days'].astype(int)
    X_dev   = dev_df.drop(columns=['readmitted_within_30_days'])

    # setting up the preprocessor pipelines below
    cat_cols = ['gender','race','ethnicity','payer_type']
    num_cols = [c for c in X_train.columns if c not in cat_cols]

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
        ('num', StandardScaler(),                   num_cols),
    ], remainder='drop')

    clf = Pipeline([
        ('pre',   preprocessor),
        ('model', RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_split=20,
            min_samples_leaf=10,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42
        ))
    ])

    # trains and evaluates on dev
    clf.fit(X_train, y_train)
    y_proba_dev = clf.predict_proba(X_dev)[:,1]
    print(f"ROC AUC on dev set: {roc_auc_score(y_dev, y_proba_dev):.4f}")

    # retrains on full data
    full_df = pd.concat([train_df, dev_df], ignore_index=True)
    y_full  = full_df['readmitted_within_30_days'].astype(int)
    X_full  = full_df.drop(columns=['readmitted_within_30_days'])
    clf.fit(X_full, y_full)

    # saves the model
    joblib.dump(clf, model_path)
    print(f"Model pipeline saved to '{model_path}'")


def predict(model_path, input_path, output_path="submission.csv"):
    # loads the pipeline and data from def train
    clf   = joblib.load(model_path)
    df_in = pd.read_csv(input_path)

    # frequency encoded the patient_id
    df_in['patient_freq'] = df_in.groupby('patient_id')['patient_id'].transform('count')

    # drop columns that are not meaningful for prediction
    drop_cols = [
        'patient_id',
        'readmitted_within_30_days_frequency',
        'has_chronic_pain',
        'has_hypertension',
        'has_diabetes',
        'has_asthma',
        'has_depression'
    ]
    feat = df_in.drop(columns=drop_cols, errors='ignore')

    # separate X and true y, but keeps encounter_id for output for the submission
    X_new        = feat.drop(columns=['readmitted_within_30_days'], errors='ignore')
    encounter_id = df_in['encounter_id']

    # predicts probabilities
    probs = clf.predict_proba(X_new)[:,1]

    # saves to csv
    submission = pd.DataFrame({
        'encounter_id':               encounter_id,
        'readmitted_within_30_days':  probs
    })
    submission.to_csv(output_path, index=False)
    print(f"Wrote {len(submission)} rows to '{output_path}'")


def test(model_path, input_path, output_path="submission.csv"):
    # same process as predict but with test.csv
    clf    = joblib.load(model_path)
    df_test = pd.read_csv(input_path)


    df_test['patient_freq'] = df_test.groupby('patient_id')['patient_id'].transform('count')


    drop_cols = [
        'patient_id',
        'readmitted_within_30_days_frequency',
        'has_chronic_pain',
        'has_hypertension',
        'has_diabetes',
        'has_asthma',
        'has_depression'
    ]
    feat = df_test.drop(columns=drop_cols, errors='ignore')


    y_test     = feat['readmitted_within_30_days'].astype(int)
    X_test     = feat.drop(columns=['readmitted_within_30_days'], errors='ignore')
    encounter_id = df_test['encounter_id']


    probs = clf.predict_proba(X_test)[:, 1]
    preds = clf.predict(X_test)


    print(f"Test ROC AUC: {roc_auc_score(y_test, probs):.4f}")


    submission = pd.DataFrame({
        'encounter_id':               encounter_id,
        'readmitted_within_30_days':  probs
    })
    submission.to_csv(output_path, index=False)
    print(f"Submission saved to '{output_path}'")


#modified args to include test 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train or predict readmission model")
    parser.add_argument("command", choices=["train","predict", "test"],
                        help="train, predict, or test")
    parser.add_argument("--train_path", help="Path to train.csv")
    parser.add_argument("--dev_path",   help="Path to dev.csv (for train)")
    parser.add_argument("--input_path", help="Path to CSV to predict (for predict)")
    parser.add_argument("--model_path", default="model.pkl", help="Path to save/load model")
    parser.add_argument("--output_path", default="submission.csv", help="Path to write predictions")
    args = parser.parse_args()

    if args.command == "train":
        assert args.train_path and args.dev_path
        train(args.train_path, args.dev_path, args.model_path)
    elif args.command == "predict":
        assert args.input_path
        predict(args.model_path, args.input_path, args.output_path)
    else:  # test
        assert args.input_path
        test(args.model_path, args.input_path)