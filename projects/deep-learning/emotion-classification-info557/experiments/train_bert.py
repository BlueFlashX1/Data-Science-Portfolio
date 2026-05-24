"""Pretrained-embedding comparison variant: RoBERTa-base (frozen feature extractor).

Uses the keras_hub preset `roberta_base_en` — equivalent to
HuggingFace's FacebookAI/roberta-base, which Steven Bethard explicitly
permitted on Slack. NOT a task-specific fine-tune (those are forbidden).

Same architecture pattern as train_dev.py — Conv1D → GlobalMaxPooling →
Dense sigmoid head, BCE+label-smoothing, 5-seed ensemble — except the
input embedding stage is a frozen RoBERTa-base backbone (instead of a
trainable Embedding layer initialized randomly or from GloVe).

Strategy: precompute RoBERTa token-level embeddings ONCE on train+dev
(padded to MAX_LEN=128), cache them to disk, then train 5 lightweight
CNN heads on those frozen features. Keeps the experiment cheap while
giving each ensemble member its own randomly-initialized head.

Requires: keras-hub (`pip install keras-hub`) — TensorFlow-native, no torch.
"""
import os
import sys
import json
import random
import keras
import numpy as np

try:
    import keras_hub
except ImportError:
    print("\nERROR: keras_hub not installed. Run:\n  ./venv/bin/pip install keras-hub\n")
    raise

# Reuse from-scratch project's data + helpers verbatim
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from train_dev import (
    augment_data, bias_output, f1_score,
    ensemble_predict, emotions,
)

PRESET = 'roberta_base_en'   # = HuggingFace FacebookAI/roberta-base
MAX_LEN = 128
EMBED_DIM = 768              # RoBERTa-base hidden size
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'bert_cache')


def build_text_to_features_model():
    """Wrap the keras_hub preprocessor + frozen RoBERTa backbone into a
    single Keras model that maps raw text strings -> token embeddings.

    Returns a model with input shape () (string scalar per batch element)
    and output shape (MAX_LEN, EMBED_DIM).
    """
    print(f"Loading {PRESET} preprocessor + backbone (frozen)...")
    preprocessor = keras_hub.models.RobertaTextClassifierPreprocessor.from_preset(
        PRESET, sequence_length=MAX_LEN,
    )
    backbone = keras_hub.models.RobertaBackbone.from_preset(PRESET)
    backbone.trainable = False

    text_input = keras.Input(shape=(), dtype='string', name='text')
    preprocessed = preprocessor(text_input)
    sequence_output = backbone(preprocessed)
    encoder = keras.Model(text_input, sequence_output, name='roberta_encoder')
    encoder.trainable = False
    return encoder


def build_head(n_outputs, output_bias=None):
    """CNN head that consumes precomputed RoBERTa embeddings.

    Same Conv1D + GMP + Dense backbone as the from-scratch model.
    """
    bias_init = keras.initializers.Constant(output_bias) if output_bias is not None else 'zeros'
    model = keras.Sequential([
        keras.layers.Input(shape=(MAX_LEN, EMBED_DIM)),
        keras.layers.GaussianNoise(0.009),
        keras.layers.Conv1D(254, kernel_size=3, activation='relu'),
        keras.layers.SpatialDropout1D(0.3),
        keras.layers.GlobalMaxPooling1D(),
        keras.layers.Dense(n_outputs, activation='sigmoid', bias_initializer=bias_init),
    ])
    model.compile(
        optimizer='adam',
        loss=keras.losses.BinaryCrossentropy(label_smoothing=0.05),
        metrics=['precision', 'recall', f1_score],
    )
    return model, {
        'batch_size': 128, 'epochs': 30,
        'callbacks': [keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=3, restore_best_weights=True)],
    }


def precompute_or_load_features(train_texts, dev_texts):
    """Cache RoBERTa features to disk to avoid recomputing across reruns."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    train_path = os.path.join(CACHE_DIR, 'train_features.npy')
    dev_path = os.path.join(CACHE_DIR, 'dev_features.npy')

    if os.path.exists(train_path) and os.path.exists(dev_path):
        print(f"Loading cached RoBERTa features from {CACHE_DIR}")
        return np.load(train_path), np.load(dev_path)

    encoder = build_text_to_features_model()

    print(f"Encoding {len(train_texts):,} train texts (MAX_LEN={MAX_LEN}, "
          f"hidden={EMBED_DIM})...")
    X_train = encoder.predict(np.asarray(train_texts), batch_size=32, verbose=1)
    np.save(train_path, X_train.astype('float32'))

    print(f"Encoding {len(dev_texts):,} dev texts...")
    X_dev = encoder.predict(np.asarray(dev_texts), batch_size=32, verbose=1)
    np.save(dev_path, X_dev.astype('float32'))

    return np.load(train_path), np.load(dev_path)


if __name__ == '__main__':
    project_root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(project_root)

    random.seed(42)
    np.random.seed(42)

    # We need raw text strings (not the integer-vectorized X used by
    # train_dev.py), so we rebuild the texts list directly here.
    import pandas as pd
    train_csv = pd.read_csv('data/train.csv', keep_default_na=False)
    dev_csv = pd.read_csv('data/dev.csv', keep_default_na=False)
    train_csv['labels'] = train_csv['labels'].apply(lambda x: x.split())
    dev_csv['labels'] = dev_csv['labels'].apply(lambda x: x.split())

    # Multi-hot labels (same string lookup pattern as train_dev.load_data)
    import tensorflow as tf
    string_lookup = keras.layers.StringLookup(
        vocabulary=emotions, output_mode='multi_hot', num_oov_indices=0)
    y_train = string_lookup(tf.ragged.constant(train_csv['labels'].tolist())).numpy()
    y_dev = string_lookup(tf.ragged.constant(dev_csv['labels'].tolist())).numpy()

    # Note: skipping the rare-class TEXT swap (frozen features prevent
    # re-encoding on the fly). Duplicate-rare-class augmentation is
    # applied AFTER feature extraction since it operates on (X, y) arrays.
    X_train_features, X_dev_features = precompute_or_load_features(
        train_csv['text'], dev_csv['text'])

    X_train_features, y_train = augment_data(X_train_features, y_train)
    output_bias = bias_output(y_train)

    save_dir = os.path.join('experiments', 'saved_models_bert')
    os.makedirs(save_dir, exist_ok=True)

    models = []
    for seed in [42, 43, 44, 45, 46]:
        keras.utils.set_random_seed(seed)
        model, params = build_head(len(emotions), output_bias)
        model.fit(X_train_features, y_train,
                  validation_data=(X_dev_features, y_dev), **params)
        model.save(os.path.join(save_dir, f'model_seed_{seed}.keras'))
        models.append(model)

    # Save preset name so compare.py can identify which model produced these
    with open(os.path.join(save_dir, 'bert_config.json'), 'w') as f:
        json.dump({'preset': PRESET, 'max_len': MAX_LEN,
                   'embed_dim': EMBED_DIM}, f)

    y_dev_pred = ensemble_predict(models, X_dev_features)
    f1 = f1_score(y_dev, y_dev_pred).numpy()
    print(f"\n=== {PRESET}-frozen ensemble dev F1: {f1:.4f} ===")
