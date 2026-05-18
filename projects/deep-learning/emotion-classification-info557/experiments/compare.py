"""Side-by-side dev F1 comparison: from-scratch CNN vs GloVe vs DistilBERT.

Loads each saved ensemble, runs it on dev.csv with the SAME inference logic
(threshold 0.5, ensemble averaging), reports overall + per-class F1.
"""
import os
import sys
import json
import keras
import numpy as np
import pandas as pd
import tensorflow as tf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from train_dev import f1_score, ensemble_predict, emotions

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SEEDS = [42, 43, 44, 45, 46]


def per_class_f1(y_true, probs, threshold=0.5):
    eps = 1e-7
    y_pred = (probs >= threshold).astype('float32')
    tp = (y_true * y_pred).sum(axis=0)
    fp = ((1 - y_true) * y_pred).sum(axis=0)
    fn = (y_true * (1 - y_pred)).sum(axis=0)
    prec = tp / (tp + fp + eps)
    rec = tp / (tp + fn + eps)
    return 2 * prec * rec / (prec + rec + eps)


def load_ensemble(model_dir):
    return [keras.models.load_model(
        os.path.join(model_dir, f'model_seed_{s}.keras'),
        custom_objects={'f1_score': f1_score}) for s in SEEDS]


def evaluate_scratch(dev_texts, y_dev):
    """Original from-scratch CNN ensemble in saved_models/."""
    with open(os.path.join(PROJECT_ROOT, 'saved_models', 'vocab.json')) as f:
        vocab = json.load(f)
    vec = keras.layers.TextVectorization(max_tokens=10000, output_mode='int')
    vec.set_vocabulary(vocab)
    X = vec(dev_texts).numpy()
    models = load_ensemble(os.path.join(PROJECT_ROOT, 'saved_models'))
    return ensemble_predict(models, X)


def evaluate_glove(dev_texts, y_dev):
    """GloVe-init ensemble in experiments/saved_models_glove/."""
    glove_dir = os.path.join(PROJECT_ROOT, 'experiments', 'saved_models_glove')
    if not os.path.exists(glove_dir):
        return None
    with open(os.path.join(glove_dir, 'vocab.json')) as f:
        vocab = json.load(f)
    vec = keras.layers.TextVectorization(max_tokens=10000, output_mode='int')
    vec.set_vocabulary(vocab)
    X = vec(dev_texts).numpy()
    models = load_ensemble(glove_dir)
    return ensemble_predict(models, X)


def evaluate_bert_frozen(dev_texts, y_dev):
    """RoBERTa-frozen ensemble in experiments/saved_models_bert/."""
    bert_dir = os.path.join(PROJECT_ROOT, 'experiments', 'saved_models_bert')
    cache_path = os.path.join(PROJECT_ROOT, 'experiments', 'bert_cache', 'dev_features.npy')
    if not os.path.exists(bert_dir):
        return None
    if not os.path.exists(cache_path):
        print("RoBERTa-frozen dev cache missing; run train_bert.py first.")
        return None
    X = np.load(cache_path)
    models = load_ensemble(bert_dir)
    return ensemble_predict(models, X)


def evaluate_bert_finetune(dev_texts, y_dev):
    """bert_tiny-finetuned ensemble — read pre-computed dev predictions."""
    pred_path = os.path.join(PROJECT_ROOT, 'experiments',
                              'saved_models_bert_finetune', 'dev_predictions.npy')
    if not os.path.exists(pred_path):
        return None
    return np.load(pred_path)


def evaluate_roberta_finetune(dev_texts, y_dev):
    """RoBERTa-base finetuned (PyTorch+MPS) — read pre-computed dev predictions."""
    pred_path = os.path.join(PROJECT_ROOT, 'experiments',
                              'saved_models_roberta_finetune',
                              'dev_predictions.npy')
    if not os.path.exists(pred_path):
        return None
    return np.load(pred_path)


if __name__ == '__main__':
    os.chdir(PROJECT_ROOT)

    dev = pd.read_csv('dev.csv', keep_default_na=False)
    string_lookup = keras.layers.StringLookup(
        vocabulary=emotions, output_mode='multi_hot', num_oov_indices=0)
    y_dev = string_lookup(
        tf.ragged.constant(dev['labels'].apply(lambda x: x.split()).tolist())
    ).numpy().astype('float32')

    results = {}
    print("Evaluating from-scratch CNN ensemble...")
    results['from-scratch'] = evaluate_scratch(dev['text'], y_dev)
    print("Evaluating GloVe ensemble...")
    results['GloVe-100d'] = evaluate_glove(dev['text'], y_dev)
    print("Evaluating RoBERTa-frozen ensemble...")
    results['RoBERTa-frozen'] = evaluate_bert_frozen(dev['text'], y_dev)
    print("Evaluating bert_tiny-finetuned ensemble...")
    results['bert_tiny-finetuned'] = evaluate_bert_finetune(dev['text'], y_dev)
    print("Evaluating RoBERTa-base-finetuned ensemble (PyTorch/MPS)...")
    results['RoBERTa-base-finetuned'] = evaluate_roberta_finetune(dev['text'], y_dev)

    # Side-by-side overall F1
    print("\n" + "=" * 60)
    print(f"{'Model':<22}  {'Dev F1':>8}  {'Status':<20}")
    print("-" * 60)
    overall = {}
    for name, probs in results.items():
        if probs is None:
            print(f"{name:<22}  {'-':>8}  not trained yet")
            continue
        f1 = float(f1_score(y_dev, probs).numpy())
        overall[name] = f1
        print(f"{name:<22}  {f1:>8.4f}  trained ✓")

    # Side-by-side per-class F1
    available = {k: v for k, v in results.items() if v is not None}
    if len(available) >= 2:
        print("\nPer-class dev F1:")
        names = list(available.keys())
        header = f"  {'class':<13}" + ''.join(f"{n[:18]:>20}" for n in names)
        print(header)
        per_class = {n: per_class_f1(y_dev, p) for n, p in available.items()}
        for i, emo in enumerate(emotions):
            row = f"  {emo:<13}" + ''.join(f"{per_class[n][i]:>20.3f}" for n in names)
            print(row)

    # Headline summary
    if len(overall) > 1:
        best = max(overall.items(), key=lambda kv: kv[1])[0]
        scratch = overall.get('from-scratch')
        if scratch is not None:
            print(f"\nBest: {best} ({overall[best]:.4f})")
            for n, f in overall.items():
                if n == 'from-scratch':
                    continue
                delta = f - scratch
                print(f"  {n:<22} vs from-scratch: {delta:+.4f} F1")
