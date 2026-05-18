import argparse
import numpy as np
import pandas
import keras

emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'confusion', 'curiosity', 'disapproval', 'gratitude', 'joy',
            'love', 'optimism', 'sadness', 'surprise']


def train(train_path, dev_path, model_path):
    train_df = pandas.read_csv(train_path, keep_default_na=False)
    dev_df = pandas.read_csv(dev_path, keep_default_na=False)

    model = keras.Sequential(...)
    model.compile(...)
    model.fit(...)

    keras.models.save_model(model, model_path + '.keras')


def predict(model_path, input_path):
    df = pandas.read_csv(input_path, keep_default_na=False)

    model = keras.models.load_model(model_path + '.keras')
    outputs = model.predict(...)

    df['labels'] = ...

    df.to_csv("submission.zip", index=False, compression=dict(
        method='zip', archive_name=f'submission.csv'))


if __name__ == "__main__":
    # parse the command line arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("train_path")
    train_parser.add_argument("dev_path")
    train_parser.add_argument("model_path")
    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("model_path")
    predict_parser.add_argument("input_path")
    args = parser.parse_args()
    kwargs = vars(args)
    globals()[kwargs.pop('command')](**kwargs)
