"""Pretrained-embedding comparison variant: GloVe 6B 100d.

Identical to train_dev.py EXCEPT the Embedding layer is initialized from
GloVe vectors (instead of random init). Everything else — augmentation,
Conv1D backbone, BCE+label-smoothing, 5-seed ensemble — is unchanged so
the F1 difference is attributable to the embedding choice alone.

GloVe downloaded once on first run (~822 MB zip → glove.6B.100d.txt
extracted, ~350 MB). Cached under experiments/glove/.
"""
import os
import sys
import json
import urllib.request
import zipfile
import random
import keras
import numpy as np

# Reuse the from-scratch project's data pipeline + helpers verbatim
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from train_dev import (
    load_data, augment_data, bias_output, f1_score,
    ensemble_predict, emotions,
)

GLOVE_DIR = os.path.join(os.path.dirname(__file__), 'glove')
GLOVE_URL = 'https://nlp.stanford.edu/data/glove.6B.zip'
GLOVE_FILE = os.path.join(GLOVE_DIR, 'glove.6B.100d.txt')
EMBEDDING_DIM = 100


def ensure_glove():
    if os.path.exists(GLOVE_FILE):
        return
    os.makedirs(GLOVE_DIR, exist_ok=True)
    zip_path = os.path.join(GLOVE_DIR, 'glove.6B.zip')
    print(f"Downloading GloVe (~822 MB) to {zip_path} — one-time only...")
    urllib.request.urlretrieve(GLOVE_URL, zip_path)
    print("Extracting glove.6B.100d.txt...")
    with zipfile.ZipFile(zip_path) as z:
        z.extract('glove.6B.100d.txt', GLOVE_DIR)
    os.remove(zip_path)
    print("GloVe ready.")


def load_glove_vectors():
    print(f"Loading GloVe vectors from {GLOVE_FILE}...")
    vectors = {}
    with open(GLOVE_FILE, encoding='utf-8') as f:
        for line in f:
            parts = line.rstrip().split(' ')
            vectors[parts[0]] = np.asarray(parts[1:], dtype='float32')
    print(f"  {len(vectors):,} word vectors loaded ({EMBEDDING_DIM}d)")
    return vectors


def build_embedding_matrix(vocabulary, glove_vectors):
    """Map our vocab indices to GloVe vectors; OOV -> small random init."""
    rng = np.random.default_rng(seed=0)
    matrix = rng.normal(scale=0.05, size=(len(vocabulary), EMBEDDING_DIM)).astype('float32')
    matrix[0] = 0.0  # padding token
    hits = 0
    for i, word in enumerate(vocabulary):
        v = glove_vectors.get(word.lower())
        if v is not None:
            matrix[i] = v
            hits += 1
    print(f"  vocab coverage: {hits}/{len(vocabulary)} ({hits/len(vocabulary)*100:.1f}%)")
    return matrix


def build_glove_cnn(vocabulary, n_outputs, embedding_matrix, output_bias=None):
    """Same architecture as train_dev.convolutional_neural_network, but with
    GloVe-initialized Embedding (trainable=True for fine-tuning during training)."""
    bias_init = keras.initializers.Constant(output_bias) if output_bias is not None else 'zeros'

    model = keras.Sequential([
        keras.layers.Input(shape=(None,)),
        keras.layers.Embedding(
            input_dim=len(vocabulary),
            output_dim=EMBEDDING_DIM,
            embeddings_initializer=keras.initializers.Constant(embedding_matrix),
            trainable=True,  # let GloVe vectors fine-tune to the task
        ),
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


if __name__ == '__main__':
    # Run from the project root so train.csv / dev.csv resolve via load_data()
    project_root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(project_root)

    ensure_glove()

    random.seed(42)
    np.random.seed(42)

    X_train, y_train, X_dev, y_dev, vocabulary, _, vectorizer = load_data()
    X_train, y_train = augment_data(X_train, y_train)
    output_bias = bias_output(y_train)

    glove_vectors = load_glove_vectors()
    embedding_matrix = build_embedding_matrix(vocabulary, glove_vectors)

    save_dir = os.path.join('experiments', 'saved_models_glove')
    os.makedirs(save_dir, exist_ok=True)

    models = []
    for seed in [42, 43, 44, 45, 46]:
        keras.utils.set_random_seed(seed)
        model, params = build_glove_cnn(vocabulary, len(emotions), embedding_matrix, output_bias)
        model.fit(X_train, y_train, validation_data=(X_dev, y_dev), **params)
        model.save(os.path.join(save_dir, f'model_seed_{seed}.keras'))
        models.append(model)

    with open(os.path.join(save_dir, 'vocab.json'), 'w') as f:
        json.dump(vectorizer.get_vocabulary(), f)

    y_dev_pred = ensemble_predict(models, X_dev)
    f1 = f1_score(y_dev, y_dev_pred).numpy()
    print(f"\n=== GloVe ensemble dev F1: {f1:.4f} ===")
