"""Fourth comparison variant: RoBERTa-base FINE-TUNED end-to-end.

The frozen-feature variant (train_bert.py) underperformed the from-scratch
baseline. This script tests the hypothesis that fine-tuning the entire
RoBERTa backbone — letting it adapt to GoEmotions during training — is
what actually unlocks pretrained-LM accuracy. This is what the leaderboard
top scorers most likely did.

Differences vs train_bert.py:
  - backbone.trainable = True   (was False)
  - learning_rate = 2e-5        (BERT paper convention; Adam's default 1e-3
                                 would catastrophically destroy pretrained
                                 weights)
  - batch_size = 16             (memory; 124M-param backbone × 5 seeds)
  - max epochs = 5, early-stop patience = 1   (BERT fine-tunes converge fast;
                                               more epochs typically overfit)
  - rare-class word-swap augmentation IS applied (this is the actual data
    pipeline used by the from-scratch and GloVe variants — we can do it
    here because we re-encode through BERT every step anyway)

Same as train_bert.py: 5-seed ensemble, BCE + label smoothing 0.05,
GaussianNoise + Conv1D + GMP + Dense head, threshold 0.5 evaluation.
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from train_dev import (
    augment_data, augment_data_with_vocab, class_vocabulary,
    bias_output, f1_score, ensemble_predict, emotions,
)

PRESET = 'bert_tiny_en_uncased'   # 4M params, 2 layers, 128 hidden — CPU-friendly
MAX_LEN = 128
EMBED_DIM = 128                   # bert_tiny hidden dim
LEARNING_RATE = 5e-5              # bumped from 2e-5: bert_tiny needs more push
BATCH_SIZE = 16
MAX_EPOCHS = 20                   # bumped from 5: previous run never converged (ended at val_f1 ~0.10-0.19, still climbing)
PATIENCE = 3                      # bumped from 1: more tolerance for bert_tiny's slow start


def prepare_text_data():
    """Load train+dev, apply rare-class word-swap augmentation, return raw
    text arrays + multi-hot label arrays. Mirrors train_dev.load_data() but
    without integer vectorization (BERT preprocessor handles tokenization).
    """
    import pandas as pd
    import tensorflow as tf

    train_csv = pd.read_csv('train.csv', keep_default_na=False)
    dev_csv = pd.read_csv('dev.csv', keep_default_na=False)
    train_csv['labels'] = train_csv['labels'].apply(lambda x: x.split())
    dev_csv['labels'] = dev_csv['labels'].apply(lambda x: x.split())

    # Identify rare classes (< 3% of train)
    label_counts = {}
    for labels in train_csv['labels']:
        for label in labels:
            label_counts[label] = label_counts.get(label, 0) + 1
    rare = [lbl for lbl, c in label_counts.items() if c / len(train_csv) < 0.03]
    class_vocab = class_vocabulary(train_csv['text'], train_csv['labels'], rare)

    # Word-swap augmentation: 4 variants per rare-class example
    aug_rows = []
    for text, labels in zip(train_csv['text'], train_csv['labels']):
        rare_in_row = [lbl for lbl in labels if lbl in rare]
        if rare_in_row:
            for _ in range(4):
                pick = random.choice(rare_in_row)
                aug_rows.append({
                    'text': augment_data_with_vocab(text, class_vocab[pick]),
                    'labels': labels,
                })
    if aug_rows:
        train_csv = pd.concat([train_csv, pd.DataFrame(aug_rows)], ignore_index=True)

    # Multi-hot encode labels (same StringLookup pattern as train_dev)
    sl = keras.layers.StringLookup(
        vocabulary=emotions, output_mode='multi_hot', num_oov_indices=0)
    y_train = sl(tf.ragged.constant(train_csv['labels'].tolist())).numpy()
    y_dev = sl(tf.ragged.constant(dev_csv['labels'].tolist())).numpy()

    return (train_csv['text'].values, y_train,
            dev_csv['text'].values, y_dev)


def duplicate_rare_class_rows(texts, y, threshold=0.025, copies=4):
    """Text-aware version of train_dev.augment_data — duplicate rare-class
    rows (text strings + label vectors together)."""
    new_t, new_y = [texts], [y]
    for cls in range(y.shape[1]):
        pos = np.where(y[:, cls] == 1)[0]
        if len(pos) / len(y) < threshold:
            for _ in range(copies):
                new_t.append(texts[pos])
                new_y.append(y[pos])
    return np.concatenate(new_t), np.concatenate(new_y, axis=0)


def build_finetuned_model(n_outputs, output_bias=None):
    """End-to-end trainable model: text → preprocessor → backbone (trainable)
    → CNN head → multi-label sigmoid. Same head architecture as train_dev.py
    so the comparison isolates the embedding strategy."""
    print(f"Loading {PRESET} preprocessor + backbone (TRAINABLE)...")
    preprocessor = keras_hub.models.BertTextClassifierPreprocessor.from_preset(
        PRESET, sequence_length=MAX_LEN,
    )
    backbone = keras_hub.models.BertBackbone.from_preset(PRESET)
    backbone.trainable = True   # KEY DIFFERENCE from train_bert.py

    bias_init = keras.initializers.Constant(output_bias) if output_bias is not None else 'zeros'

    text_input = keras.Input(shape=(), dtype='string', name='text')
    preprocessed = preprocessor(text_input)
    backbone_out = backbone(preprocessed)
    # BertBackbone returns a dict {'sequence_output', 'pooled_output'};
    # we want the per-token sequence to feed Conv1D.
    sequence_output = (backbone_out['sequence_output']
                       if isinstance(backbone_out, dict) else backbone_out)
    x = keras.layers.GaussianNoise(0.009)(sequence_output)
    x = keras.layers.Conv1D(254, kernel_size=3, activation='relu')(x)
    x = keras.layers.SpatialDropout1D(0.3)(x)
    x = keras.layers.GlobalMaxPooling1D()(x)
    output = keras.layers.Dense(
        n_outputs, activation='sigmoid', bias_initializer=bias_init,
    )(x)

    model = keras.Model(text_input, output, name='roberta_finetune')
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=keras.losses.BinaryCrossentropy(label_smoothing=0.05),
        metrics=['precision', 'recall', f1_score],
    )
    return model, {
        'batch_size': BATCH_SIZE,
        'epochs': MAX_EPOCHS,
        'callbacks': [keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=PATIENCE, restore_best_weights=True)],
    }


if __name__ == '__main__':
    project_root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(project_root)

    random.seed(42)
    np.random.seed(42)

    print("Preparing text data (with rare-class word-swap augmentation)...")
    train_texts, y_train, dev_texts, y_dev = prepare_text_data()
    train_texts, y_train = duplicate_rare_class_rows(train_texts, y_train)
    print(f"  train: {len(train_texts):,} texts (after augmentation)")
    print(f"  dev:   {len(dev_texts):,} texts")
    output_bias = bias_output(y_train)

    save_dir = os.path.join('experiments', 'saved_models_bert_finetune')
    os.makedirs(save_dir, exist_ok=True)

    # Wrap raw strings in tf.data.Dataset — numpy string arrays trigger
    # "Invalid dtype: str448" in Keras 3's graph compilation; tf.data
    # handles string tensors cleanly.
    import tensorflow as tf

    def make_ds(texts, labels, batch_size, shuffle):
        ds = tf.data.Dataset.from_tensor_slices((texts, labels))
        if shuffle:
            ds = ds.shuffle(len(texts), seed=42)
        return ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

    train_ds = make_ds(train_texts, y_train, BATCH_SIZE, shuffle=True)
    val_ds = make_ds(dev_texts, y_dev, BATCH_SIZE, shuffle=False)

    models = []
    for seed in [42, 43, 44, 45, 46]:
        print(f"\n{'='*60}\nFine-tuning seed {seed}\n{'='*60}")
        keras.utils.set_random_seed(seed)
        model, params = build_finetuned_model(len(emotions), output_bias)
        # tf.data does its own batching, so don't pass batch_size to fit()
        params_no_bs = {k: v for k, v in params.items() if k != 'batch_size'}
        model.fit(train_ds, validation_data=val_ds, **params_no_bs)
        # Save weights only — model.save() doesn't roundtrip keras_hub's
        # tokenizer vocabulary cleanly (loading raises "No vocabulary has
        # been set"). Architecture is rebuilt deterministically from PRESET
        # in compare.py via the same build_finetuned_model() factory.
        model.save_weights(os.path.join(save_dir, f'model_seed_{seed}.weights.h5'))
        models.append(model)

    print("\nEnsemble evaluation on dev set...")
    # ensemble_predict iterates model.predict; same string-dtype issue, so
    # use predict() directly with the eval tf.data.Dataset.
    eval_ds = make_ds(dev_texts, y_dev, BATCH_SIZE, shuffle=False)
    predictions = [m.predict(eval_ds.map(lambda x, y: x)) for m in models]
    y_dev_pred = np.mean(predictions, axis=0)
    f1 = float(f1_score(y_dev, y_dev_pred).numpy())
    print(f"\n=== {PRESET}-finetuned ensemble dev F1: {f1:.4f} ===")

    # Also save per-class F1 + ensemble probs for compare.py to read without
    # needing to reload the trainable backbones.
    np.save(os.path.join(save_dir, 'dev_predictions.npy'), y_dev_pred)
    with open(os.path.join(save_dir, 'bert_config.json'), 'w') as f:
        json.dump({'preset': PRESET, 'max_len': MAX_LEN, 'embed_dim': EMBED_DIM,
                   'mode': 'finetuned', 'lr': LEARNING_RATE,
                   'batch_size': BATCH_SIZE, 'max_epochs': MAX_EPOCHS,
                   'patience': PATIENCE, 'ensemble_dev_f1': f1}, f)
