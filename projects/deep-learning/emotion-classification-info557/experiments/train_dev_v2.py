from typing import Tuple, List, Dict
import keras
import tensorflow as tf
import numpy as np
import pandas as pd

#two-stage approach: stage 1 is binary (has any emotion yes/no),
#stage 2 is multi-label (which emotions, trained only on non-empty rows)
#multi-label classification: https://keras.io/examples/nlp/multi_label_classification/
#class imbalance handled via focal loss (keras.losses.BinaryFocalCrossentropy) + threshold tuning on dev

emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'confusion', 'curiosity', 'disapproval', 'gratitude', 'joy',
            'love', 'optimism', 'sadness', 'surprise']

# def function for calculating F1 scores
def f1_score(y_true, y_pred):
    y_true = keras.ops.cast(y_true, 'float32')
    y_pred = keras.ops.cast(y_pred >= 0.3, 'float32')
    tp = keras.ops.sum(keras.ops.cast(y_true * y_pred, 'float32'))
    fp = keras.ops.sum(keras.ops.cast((1 - y_true) * y_pred, 'float32'))
    fn = keras.ops.sum(keras.ops.cast(y_true * (1 - y_pred), 'float32'))

    precision = tp / (tp + fp + keras.backend.epsilon())
    recall = tp / (tp + fn + keras.backend.epsilon())

    f1 = 2 * (precision * recall) / (precision + recall + keras.backend.epsilon())
    return keras.ops.mean(f1)

# stage 1: binary conv1d (has emotion yes/no)
def stage1_model(vocabulary: List[str]) -> Tuple[keras.Model, Dict]:
    model = keras.Sequential()

    model.add(keras.layers.Input(shape=(None,)))
    model.add(keras.layers.Embedding(input_dim=len(vocabulary), output_dim=128))
    model.add(keras.layers.GaussianNoise(0.009))
    model.add(keras.layers.Conv1D(254, kernel_size=3, activation='relu'))
    model.add(keras.layers.SpatialDropout1D(0.3))
    model.add(keras.layers.GlobalMaxPooling1D())

    #single sigmoid output for binary
    model.add(keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam',
                loss=keras.losses.BinaryCrossentropy(),
                metrics=['precision', 'recall']
                )

    return model, {'batch_size': 128, 'epochs': 30, 'callbacks': [keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)]}

# stage 2: multi label conv1d (which emotions, trained only on non-empty rows)
def stage2_model(vocabulary: List[str], n_outputs: int) -> Tuple[keras.Model, Dict]:
    model = keras.Sequential()

    model.add(keras.layers.Input(shape=(None,)))
    model.add(keras.layers.Embedding(input_dim=len(vocabulary), output_dim=128))
    model.add(keras.layers.GaussianNoise(0.009))
    model.add(keras.layers.Conv1D(254, kernel_size=3, activation='relu'))
    model.add(keras.layers.SpatialDropout1D(0.3))
    model.add(keras.layers.GlobalMaxPooling1D())

    model.add(keras.layers.Dense(n_outputs, activation='sigmoid'))

    model.compile(optimizer='adam',
                loss=keras.losses.BinaryFocalCrossentropy(),
                metrics=['precision', 'recall', f1_score]
                )

    return model, {'batch_size': 128, 'epochs': 30, 'callbacks': [keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)]}

def load_data():
    train_csv = pd.read_csv('data/train.csv', keep_default_na=False)
    dev_csv = pd.read_csv('data/dev.csv', keep_default_na=False)
    dev_csv_raw = dev_csv.copy()

    vectorizer = keras.layers.TextVectorization(max_tokens=10000,
                                                output_mode='int',
                                                output_sequence_length=None)
    vectorizer.adapt(train_csv['text'])

    train_csv['labels'] = train_csv['labels'].apply(lambda x: x.split())

    #StringLookup + ragged tensor pattern from https://keras.io/examples/nlp/multi_label_classification/
    string_lookup = keras.layers.StringLookup(vocabulary=emotions,
                                            output_mode='multi_hot',
                                            num_oov_indices=0
                                            )
    train_labels_ragged = tf.ragged.constant(train_csv['labels'].tolist())
    y_train_multi_hot = string_lookup(train_labels_ragged).numpy()

    dev_csv['labels'] = dev_csv['labels'].apply(lambda x: x.split())
    dev_labels_ragged = tf.ragged.constant(dev_csv['labels'].tolist())
    y_dev_multi_hot = string_lookup(dev_labels_ragged).numpy()

    #binary target: 1 if any emotion, 0 if empty
    y_train_binary = (y_train_multi_hot.sum(axis=1) > 0).astype('float32')
    y_dev_binary = (y_dev_multi_hot.sum(axis=1) > 0).astype('float32')

    vocabulary = vectorizer.get_vocabulary()

    X_train = vectorizer(train_csv['text']).numpy()
    X_dev = vectorizer(dev_csv['text']).numpy()

    return X_train, y_train_multi_hot, y_train_binary, X_dev, y_dev_multi_hot, y_dev_binary, vocabulary, dev_csv_raw

#average all model predictions
def ensemble_predict(models: List[keras.Model], X: np.ndarray) -> np.ndarray:
    predictions = [model.predict(X) for model in models]
    return np.mean(predictions, axis=0)

#run the training
if __name__ == "__main__":
    X_train, y_train_mh, y_train_bin, X_dev, y_dev_mh, y_dev_bin, vocabulary, dev_csv_raw = load_data()

    #stage 1 ensemble (binary, all rows)
    print("training stage 1 (binary has-emotion)...")
    stage1_models = []
    for seed in [42, 43, 44, 45, 46]:
        keras.utils.set_random_seed(seed)
        model, params = stage1_model(vocabulary)
        model.fit(X_train, y_train_bin, validation_data=(X_dev, y_dev_bin), **params)
        stage1_models.append(model)

    #stage 2 ensemble (multi-label, only non-empty rows)
    non_empty_mask_train = y_train_bin > 0
    non_empty_mask_dev = y_dev_bin > 0
    X_train_ne = X_train[non_empty_mask_train]
    y_train_ne = y_train_mh[non_empty_mask_train]
    X_dev_ne = X_dev[non_empty_mask_dev]
    y_dev_ne = y_dev_mh[non_empty_mask_dev]

    print(f"training stage 2 (multi-label) on {len(X_train_ne)} non-empty rows...")
    stage2_models = []
    for seed in [42, 43, 44, 45, 46]:
        keras.utils.set_random_seed(seed)
        model, params = stage2_model(vocabulary, len(emotions))
        model.fit(X_train_ne, y_train_ne, validation_data=(X_dev_ne, y_dev_ne), **params)
        stage2_models.append(model)

    #two-stage prediction on dev
    probs_s1 = ensemble_predict(stage1_models, X_dev).flatten()   #(500,)
    probs_s2 = ensemble_predict(stage2_models, X_dev)             #(500, 14)

    #stage 1 threshold: if below, predict empty; else use stage 2
    t1 = 0.9
    t2 = 0.3
    has_emotion = probs_s1 >= t1
    #start with zeros, fill in stage 2 predictions only where stage 1 says has emotion
    preds = np.zeros_like(probs_s2, dtype=int)
    preds[has_emotion] = (probs_s2[has_emotion] >= t2).astype(int)

    #f1 on dev (full multi-hot comparison)
    f1 = f1_score(y_dev_mh.astype('float32'), preds.astype('float32')).numpy()
    print(f"Two-stage F1 Score: {f1:.4f}")

    #precision and recall at the used thresholds
    tp = np.sum(y_dev_mh * preds)
    fp = np.sum((1 - y_dev_mh) * preds)
    fn = np.sum(y_dev_mh * (1 - preds))
    precision = tp / (tp + fp + 1e-9)
    recall = tp / (tp + fn + 1e-9)
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}")

    #multi-hot -> label name decoding adapted from invert_multi_hot in
    #https://keras.io/examples/nlp/multi_label_classification/
    dev_csv_raw['labels'] = [' '.join(emotions[i] for i, v in enumerate(row) if v == 1)
                        for row in preds]
    dev_csv_raw[['text', 'labels']].to_csv(
        "submission.zip",
        index=False,
        compression=dict(method='zip', archive_name='submission.csv'))
