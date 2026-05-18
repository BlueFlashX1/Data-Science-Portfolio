from typing import Tuple, List, Dict
import os
import json
import random
import keras
import tensorflow as tf
import numpy as np
import pandas as pd

#modified from program 4 assignment
#based on eda.ipynb it seems there is a lot of empty labels and class imbalance
#multi-label classification: https://keras.io/examples/nlp/multi_label_classification/
#class imbalance handled via focal loss (keras.losses.BinaryFocalCrossentropy) + threshold tuning on dev

# AI assistance: GitHub Copilot inline autocomplete (https://github.com/features/copilot).                                                                     
# No prompts entered; suggestions came from code context as I typed.                                                                                           
# Autocomplete contributed to: class_vocabulary() lines 83-104, f1_score() body lines 119-130,                                                                  
# bias_output() log-odds lines 133-142, model save block lines 295-299, per-class F1 print lines 309-320.

################
# submission 1:
# based on submission 1, its pretty casual with predicting and predicted more empty label cases
# than 58% in dev and 0 on anger, annoyance, disapproval, and few other negative emotions so need
# better handling on both empty cases and class imbalance

# submission 2:
# for this submission 2nd attempt, I decided to switch binary focal crossentropy
# to BCE with label smoothing and threshold to 0.5
# and added bias initialization functions (to account for class imbalance)
# for overall stability without dropping F1 score down much so it could possibly do well on test

# final submission: 
# this time, i tried text-level in-class word swap (variant inspired from Wei & Zou 2019 EDA) 
# - no WordNet here nor pretrained embeddings
# surprisingly, this swap method score roughly tied with pure dupe method 
# at ~0.72 F1 on dev but I decided to keep both dupe and swap methods
# for potentially better coverage and generalization of rare classes for test phase

# Citation:
# Wei, J., & Zou, K. (2019). EDA: Easy Data Augmentation Techniques for Boosting 
# Performance on Text Classification Tasks (arXiv:1901.11196). 
# arXiv. https://doi.org/10.48550/arXiv.1901.11196


# overall, I think I hit the limits I couldn't break over 0.73 and 
# exhausted course techniques taught so decided to stop here. The main bottleneck overall seems to be
# synonyms for smenatic connections and probably need better understanding of the linguistics or more confidence
# in predicting rare classes with this many empty labels + class imbalance

################

emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'confusion', 'curiosity', 'disapproval', 'gratitude', 'joy',
            'love', 'optimism', 'sadness', 'surprise']

# eda data augmentation techniques focusing on rare classes 
def augment_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # simple augmentation by duplicating samples of rare classes
    augmented_X = []
    augmented_y = []
    for i in range(y.shape[1]):
        pos_indices = np.where(y[:, i] == 1)[0]
        if len(pos_indices) / len(y) < 0.025:
            # duplicate 4 times so each rare example shows up 5x in training (1 original + 4 dupes)
            augmented_X.append(X[pos_indices])
            augmented_y.append(y[pos_indices])
            augmented_X.append(X[pos_indices])
            augmented_y.append(y[pos_indices])
            augmented_X.append(X[pos_indices])
            augmented_y.append(y[pos_indices])
            augmented_X.append(X[pos_indices])
            augmented_y.append(y[pos_indices])
    
    if augmented_X:
        augmented_X = np.vstack(augmented_X)
        augmented_y = np.vstack(augmented_y)
        X = np.vstack([X, augmented_X])
        y = np.vstack([y, augmented_y])
    
    return X, y

# build word list per class from training data only
def class_vocabulary(texts, label_lists, target_classes):
    STOPWORDS = {'the', 'is', 'in', 'and', 'to', 'of', 'a', 'that', 'it', 
                'with', 'as', 'for', 'was', 'on', 'but', 'are',
                'by', 'this', 'be', 'at', 'from', 'or', 'which', 
                'an', 'not', 'all', 'they', 'their', 'has', 'have',
                'if', 'we', 'can', 'my', 'me', 'do', 'he', 'she', 'his', 
                'her', 'them', 'what', 'who', 'when', 'where', 'why', 'how'}
    class_vocab = {}
    for text, labels in zip(texts, label_lists):
        for label in labels:
            if label in target_classes:
                if label not in class_vocab: 
                    class_vocab[label] = set() 
                for word in text.split(): 
                    word = word.lower()
                    if word.isalpha() and len(word) > 2 and word not in STOPWORDS: 
                        # filter out short words, non-alpha, and stopwords
                        class_vocab[label].add(word)
    # convert sets to lists
    for label in class_vocab:
        class_vocab[label] = list(class_vocab[label])
    return class_vocab

# word swap using only training vocab (inspired by Wei & Zou 2019 EDA paper, no WordNet)
def augment_data_with_vocab(text, class_vocab_for_class, replace_pct=0.1):
    words = text.split()
    swappable = [i for i, word in enumerate(words) if word.lower() in class_vocab_for_class]
    if not swappable:
        return text
    n_replace = max(1, int(len(words) * replace_pct))
    chosen = random.sample(swappable, min(n_replace, len(swappable)))
    for i in chosen:
        words[i] = random.choice(class_vocab_for_class)
    return ' '.join(words)

# def function for calculating F1 scores 
def f1_score(y_true, y_pred):
    y_true = keras.ops.cast(y_true, 'float32')
    y_pred = keras.ops.cast(y_pred >= 0.5, 'float32')
    tp = keras.ops.sum(keras.ops.cast(y_true * y_pred, 'float32'))
    fp = keras.ops.sum(keras.ops.cast((1 - y_true) * y_pred, 'float32'))
    fn = keras.ops.sum(keras.ops.cast(y_true * (1 - y_pred), 'float32'))

    precision = tp / (tp + fp + keras.backend.epsilon())
    recall = tp / (tp + fn + keras.backend.epsilon())

    f1 = 2 * (precision * recall) / (precision + recall + keras.backend.epsilon())
    return keras.ops.mean(f1)

#compute bias initialization for output layer based on training label distribution
def bias_output(y_train: np.ndarray) -> np.ndarray:
    # calculate the positive class ratio for each label
    pos_ratios = np.mean(y_train, axis=0)
    epsilon = 1e-7
    pos_ratios = np.clip(pos_ratios, epsilon, 1 - epsilon)
    
    #compute bias initialization using log odds to account for class imbalance
    bias_init = np.log(pos_ratios / (1 - pos_ratios))
    
    return bias_init

# def Conv1D (modified from program 4 assignment)
def convolutional_neural_network(vocabulary: List[str], n_outputs: int, output_bias: np.ndarray = None) \
        -> Tuple[keras.Model, Dict]:
    model = keras.Sequential()
    
    #input shape is text sequence length that may vary
    model.add(keras.layers.Input(shape=(None,)))
    
    #embedding layer
    model.add(keras.layers.Embedding(input_dim=len(vocabulary), output_dim=128))
    
    # gaussian noise
    model.add(keras.layers.GaussianNoise(0.009))
    
    # Conv1D with 254 filters and kernel size of 3, relu activation
    model.add(keras.layers.Conv1D(254, kernel_size=3, activation='relu'))
    model.add(keras.layers.SpatialDropout1D(0.3))

    #global max pooling and dropout
    model.add(keras.layers.GlobalMaxPooling1D())
    
    #bias initizer
    bias_init = (keras.initializers.Constant(output_bias)) if output_bias is not None else 'zeros'
    
    #multi label classification with sigmoid activation
    model.add(keras.layers.Dense(n_outputs, activation='sigmoid', bias_initializer=bias_init))
    
    # BCE with label smoothing so threshold 0.5 works without tuning per dataset
    model.compile(optimizer='adam',
                loss=keras.losses.BinaryCrossentropy(label_smoothing=0.05),
                metrics=['precision', 'recall', f1_score]
                )
    
    return model, {'batch_size': 128, 'epochs': 30, 
                'callbacks': [keras.callbacks.EarlyStopping(
                    monitor='val_loss', patience=3, restore_best_weights=True)
                            ]
                }

# LSTM didnt do so well but will keep this code for reference
# def lstm_neural_network(vocabulary: List[str], n_outputs: int) \
#         -> Tuple[keras.Model, Dict]:
#     model = keras.Sequential()
#
#     #input shape is comment sequence length that may vary
#     model.add(keras.layers.Input(shape=(None,)))
#     # shape=(None,) means variable length
#     #embedding layer
#     model.add(keras.layers.Embedding(input_dim=len(vocabulary), output_dim=128, mask_zero=True))
#
#     #LSTM and dropout
#     model.add(keras.layers.LSTM(64, return_sequences=False))
#
#     #dropout to 0.3 instead
#     model.add(keras.layers.Dropout(0.3))
#
#     #multi label classification with sigmoid activation
#     model.add(keras.layers.Dense(n_outputs, activation='sigmoid'))
#
#     # loss function for multi label classification
#     model.compile(optimizer='adam', loss=keras.losses.BinaryFocalCrossentropy(), metrics=['precision', 'recall', f1_score])
#
#     return model, {'batch_size': 128, 'epochs': 10, 'callbacks': [keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)]}

def load_data():    
    train_csv = pd.read_csv('train.csv', keep_default_na=False)
    # keep_default_na=False to prevent empty strings from being converted to NaN
    dev_csv = pd.read_csv('dev.csv', keep_default_na=False)
    dev_csv_raw = dev_csv.copy()
    
    #split labels first since the swap runs on text before vectorization
    train_csv['labels'] = train_csv['labels'].apply(lambda x: x.split())

    #flag rare classes (less than 3% of train) so they get swap augmented
    label_counts = {}
    for labels in train_csv['labels']:
        for label in labels:
            if label not in label_counts:
                label_counts[label] = 0
            label_counts[label] += 1
    rare_classes = [label for label, count in label_counts.items() if count / len(train_csv) < 0.03]

    class_vocab = class_vocabulary(train_csv['text'], train_csv['labels'], rare_classes)

    #4 variants per rare example; originals kept (append, not replace)
    augmented_rows = []
    for text, labels in zip(train_csv['text'], train_csv['labels']):
        rare_in_row = [label for label in labels if label in rare_classes]
        if rare_in_row:
            for _ in range(4):  # 4 variants per rare-class example
                pick_label = random.choice(rare_in_row)
                aug_text = augment_data_with_vocab(text, class_vocab[pick_label])
                augmented_rows.append({'text': aug_text, 'labels': labels})

    if augmented_rows:
        train_csv = pd.concat([train_csv, pd.DataFrame(augmented_rows)], ignore_index=True)

    #text vectorization for both train and dev sets to get the vocabulary
    vectorizer = keras.layers.TextVectorization(max_tokens=10000, 
                                                output_mode='int', 
                                                output_sequence_length=None)
    vectorizer.adapt(train_csv['text'])

    #StringLookup + ragged tensor pattern from https://keras.io/examples/nlp/multi_label_classification/
    string_lookup = keras.layers.StringLookup(vocabulary=emotions, 
                                            output_mode='multi_hot', 
                                            num_oov_indices=0
                                            )
    train_labels_ragged = tf.ragged.constant(train_csv['labels'].tolist())
    y_train_multi_hot = string_lookup(train_labels_ragged)
    
    #process dev set labels for evaluation
    dev_csv['labels'] = dev_csv['labels'].apply(lambda x: x.split())
    dev_labels_ragged = tf.ragged.constant(dev_csv['labels'].tolist())
    y_dev_multi_hot = string_lookup(dev_labels_ragged)
    
    #get the vocabulary from the vectorizer
    vocabulary = vectorizer.get_vocabulary()
    
    X_train = vectorizer(train_csv['text']).numpy()
    X_dev = vectorizer(dev_csv['text']).numpy()
    
    return X_train, y_train_multi_hot.numpy(), X_dev, y_dev_multi_hot.numpy(), vocabulary, dev_csv_raw, vectorizer

#average all model predictions
def ensemble_predict(models: List[keras.Model], X: np.ndarray) -> np.ndarray:
    predictions = [model.predict(X) for model in models]
    return np.mean(predictions, axis=0)

#run the training
if __name__ == "__main__":
    #seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    X_train, y_train, X_dev, y_dev, vocabulary, dev_csv_raw, vectorizer = load_data()

    #duplicate rare class on top of swap augmenting
    X_train, y_train = augment_data(X_train, y_train)

    #compute output bias from training label priors for sigmoid calibration (Goodfellow Ch 8.4)
    output_bias = bias_output(y_train)

    #train multiple models with different random seeds for ensemble
    models = []
    for seed in [42, 43, 44, 45, 46]:
        keras.utils.set_random_seed(seed)
        model, training_params = convolutional_neural_network(vocabulary, len(emotions), output_bias)
        model.fit(X_train, y_train, validation_data=(X_dev, y_dev), **training_params)
        models.append(model)
    
    #save trained models + vectorizer vocab so test phase can skip retraining in a seaparate script
    os.makedirs('saved_models', exist_ok=True)
    for seed, model in zip([42, 43, 44, 45, 46], models):
        model.save(f'saved_models/model_seed_{seed}.keras')
    with open('saved_models/vocab.json', 'w') as f:
        json.dump(vectorizer.get_vocabulary(), f)

    #ensemble predictions on dev set
    y_dev_pred = ensemble_predict(models, X_dev)

    #f1 on dev
    f1 = f1_score(y_dev, y_dev_pred).numpy()
    print(f"Ensemble F1 Score: {f1:.4f}")

    #per-class F1 on dev
    eps = 1e-7
    y_pred_bin = (y_dev_pred >= 0.5).astype('float32')
    y_true = y_dev.astype('float32')
    tp = (y_true * y_pred_bin).sum(axis=0)
    fp = ((1 - y_true) * y_pred_bin).sum(axis=0)
    fn = (y_true * (1 - y_pred_bin)).sum(axis=0)
    prec = tp / (tp + fp + eps)
    rec = tp / (tp + fn + eps)
    per_class_f1 = 2 * prec * rec / (prec + rec + eps)
    print("\nPer-class F1:")
    for emo, score in sorted(zip(emotions, per_class_f1), key=lambda x: -x[1]):
        print(f"  {emo:13s} {score:.3f}")

    ### submission below — disabled, dev phase is over (only printing F1 now)
    #multi-hot -> label name decoding adapted from invert_multi_hot in
    #https://keras.io/examples/nlp/multi_label_classification/
    # preds = (y_dev_pred >= 0.5).astype(int)
    # dev_csv_raw['labels'] = [' '.join(emotions[i] for i, v in enumerate(row) if v == 1)
    #                     for row in preds]
    # dev_csv_raw[['text', 'labels']].to_csv(
    #     "submission.zip",
    #     index=False,
    #     compression=dict(method='zip', archive_name='submission.csv'))