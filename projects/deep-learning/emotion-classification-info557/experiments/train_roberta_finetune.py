"""Fifth comparison variant: RoBERTa-base FINE-TUNED end-to-end (PyTorch + MPS).

Uses PyTorch with Apple Metal Performance Shaders since tensorflow-metal is
incompatible with our TF version. RoBERTa-base on M-series GPU finishes in
~5-15 min for the full 5-seed ensemble vs ~30+ hours on CPU.

Architecture mirrors train_bert_finetune.py exactly to keep the comparison
clean - only the embedding-stage backbone changes (RoBERTa-base 124M params,
12 layers, 768 hidden vs bert_tiny 4M params, 2 layers, 128 hidden):

  text -> AutoTokenizer (RoBERTa BPE)
       -> RobertaModel last_hidden_state (B, 128, 768)
       -> GaussianNoise(0.009)
       -> Conv1d(254, 3, relu)
       -> Dropout1d(0.3)  [SpatialDropout1D equivalent]
       -> max-pool over time
       -> Linear(254, 14, with class-prior bias init)
       -> BCEWithLogitsLoss + label smoothing 0.05

Same 5-seed ensemble, same rare-class word-swap + duplicate augmentation,
same threshold 0.5 evaluation as all the other variants.
"""
import os
import sys
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from train_dev import (
    augment_data_with_vocab, class_vocabulary, emotions,
)

# ----------------------------------------------------------------------------
# Hyperparameters (BERT-paper conventions for fine-tuning)
# ----------------------------------------------------------------------------
PRESET = 'FacebookAI/roberta-base'
MAX_LEN = 128
EMBED_DIM = 768
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
MAX_EPOCHS = 5
PATIENCE = 1
LABEL_SMOOTHING = 0.05
GAUSSIAN_NOISE_STD = 0.009
DROPOUT_P = 0.3
CONV_FILTERS = 254
CONV_KERNEL = 3
SEEDS = [42, 43, 44, 45, 46]
DEVICE = torch.device('mps' if torch.backends.mps.is_available()
                      else ('cuda' if torch.cuda.is_available() else 'cpu'))

SAVE_DIR = Path(__file__).parent / 'saved_models_roberta_finetune'


# ----------------------------------------------------------------------------
# Data prep
# ----------------------------------------------------------------------------
def prepare_text_data():
    import pandas as pd
    train_csv = pd.read_csv('train.csv', keep_default_na=False)
    dev_csv = pd.read_csv('dev.csv', keep_default_na=False)
    train_csv['labels'] = train_csv['labels'].apply(lambda x: x.split())
    dev_csv['labels'] = dev_csv['labels'].apply(lambda x: x.split())

    label_counts = {}
    for lbls in train_csv['labels']:
        for lbl in lbls:
            label_counts[lbl] = label_counts.get(lbl, 0) + 1
    rare = [lbl for lbl, c in label_counts.items() if c / len(train_csv) < 0.03]
    class_vocab = class_vocabulary(train_csv['text'], train_csv['labels'], rare)

    aug_rows = []
    for text, lbls in zip(train_csv['text'], train_csv['labels']):
        rare_in_row = [lbl for lbl in lbls if lbl in rare]
        if rare_in_row:
            for _ in range(4):
                pick = random.choice(rare_in_row)
                aug_rows.append({
                    'text': augment_data_with_vocab(text, class_vocab[pick]),
                    'labels': lbls,
                })
    if aug_rows:
        train_csv = pd.concat([train_csv, pd.DataFrame(aug_rows)],
                               ignore_index=True)

    def to_multihot(label_lists):
        idx = {emo: i for i, emo in enumerate(emotions)}
        out = np.zeros((len(label_lists), len(emotions)), dtype=np.float32)
        for i, lbls in enumerate(label_lists):
            for lbl in lbls:
                if lbl in idx:
                    out[i, idx[lbl]] = 1.0
        return out

    return (train_csv['text'].values,
            to_multihot(train_csv['labels'].tolist()),
            dev_csv['text'].values,
            to_multihot(dev_csv['labels'].tolist()))


def duplicate_rare_class_rows(texts, y, threshold=0.025, copies=4):
    new_t, new_y = [texts], [y]
    for cls in range(y.shape[1]):
        pos = np.where(y[:, cls] == 1)[0]
        if len(pos) / len(y) < threshold:
            for _ in range(copies):
                new_t.append(texts[pos])
                new_y.append(y[pos])
    return np.concatenate(new_t), np.concatenate(new_y, axis=0)


def bias_init_from_priors(y_train):
    p = np.clip(y_train.mean(axis=0), 1e-7, 1 - 1e-7)
    return np.log(p / (1 - p)).astype(np.float32)


# ----------------------------------------------------------------------------
# Dataset + Model
# ----------------------------------------------------------------------------
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=MAX_LEN):
        self.encodings = tokenizer(
            list(texts), truncation=True, padding='max_length',
            max_length=max_len, return_tensors='pt',
        )
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        return {
            'input_ids': self.encodings['input_ids'][i],
            'attention_mask': self.encodings['attention_mask'][i],
            'labels': self.labels[i],
        }


class RobertaCnnHead(nn.Module):
    def __init__(self, n_outputs, output_bias=None):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(PRESET)
        self.conv = nn.Conv1d(EMBED_DIM, CONV_FILTERS, kernel_size=CONV_KERNEL)
        self.dropout = nn.Dropout1d(DROPOUT_P)
        self.classifier = nn.Linear(CONV_FILTERS, n_outputs)
        if output_bias is not None:
            with torch.no_grad():
                self.classifier.bias.copy_(torch.from_numpy(output_bias))

    def forward(self, input_ids, attention_mask):
        x = self.backbone(input_ids=input_ids,
                          attention_mask=attention_mask).last_hidden_state
        if self.training:
            x = x + torch.randn_like(x) * GAUSSIAN_NOISE_STD
        x = x.transpose(1, 2)
        x = F.relu(self.conv(x))
        x = self.dropout(x)
        x = x.max(dim=-1).values
        return self.classifier(x)


def smoothed_bce_loss(logits, labels, alpha=LABEL_SMOOTHING):
    smoothed = labels * (1 - alpha) + 0.5 * alpha
    return F.binary_cross_entropy_with_logits(logits, smoothed)


# ----------------------------------------------------------------------------
# Train + evaluate
# ----------------------------------------------------------------------------
@torch.no_grad()
def predict_logits(model, loader, device=None):
    """Run inference. If device is None, use the model's current device.
    Calling sites move the model to CPU before invoking this to avoid
    MPS hangs we observed at the end of fine-tuning runs."""
    model.train(False)
    if device is None:
        device = next(model.parameters()).device
    out = []
    for batch in loader:
        input_ids = batch['input_ids'].to(device)
        mask = batch['attention_mask'].to(device)
        out.append(model(input_ids, mask).cpu())
    return torch.cat(out, dim=0)


def f1_score_multi(y_true, probs, threshold=0.5):
    y_pred = (probs >= threshold).astype(np.float32)
    tp = ((y_true == 1) & (y_pred == 1)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    p = tp / (tp + fp + 1e-9)
    r = tp / (tp + fn + 1e-9)
    return 2 * p * r / (p + r + 1e-9)


def train_one_seed(seed, train_ds, val_ds, output_bias):
    print(f"\n{'='*60}\nFine-tuning RoBERTa-base seed {seed} on {DEVICE}\n{'='*60}")
    torch.manual_seed(seed)
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)

    model = RobertaCnnHead(n_outputs=len(emotions), output_bias=output_bias).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False,
                            num_workers=0)

    best_val_loss = float('inf')
    bad_epochs = 0
    best_state = None

    for epoch in range(1, MAX_EPOCHS + 1):
        model.train(True)
        running_loss = 0.0
        for batch in train_loader:
            input_ids = batch['input_ids'].to(DEVICE)
            mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)
            optimizer.zero_grad()
            logits = model(input_ids, mask)
            loss = smoothed_bce_loss(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        train_loss = running_loss / len(train_loader)

        # validation
        model.train(False)
        val_loss = 0.0
        all_probs, all_labels = [], []
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(DEVICE)
                mask = batch['attention_mask'].to(DEVICE)
                labels = batch['labels'].to(DEVICE)
                logits = model(input_ids, mask)
                val_loss += smoothed_bce_loss(logits, labels).item()
                all_probs.append(torch.sigmoid(logits).cpu().numpy())
                all_labels.append(labels.cpu().numpy())
        val_loss /= len(val_loader)
        probs = np.concatenate(all_probs, axis=0)
        labels_arr = np.concatenate(all_labels, axis=0)
        val_f1 = f1_score_multi(labels_arr, probs)
        print(f"  epoch {epoch}/{MAX_EPOCHS}  "
              f"train_loss {train_loss:.4f}  "
              f"val_loss {val_loss:.4f}  "
              f"val_f1 {val_f1:.4f}")

        if val_loss < best_val_loss - 1e-6:
            best_val_loss = val_loss
            bad_epochs = 0
            best_state = {k: v.detach().cpu().clone()
                          for k, v in model.state_dict().items()}
        else:
            bad_epochs += 1
            if bad_epochs > PATIENCE:
                print(f"  early stop after epoch {epoch}")
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, val_loader


def main():
    """Run-mode CLI:
      python train_roberta_finetune.py            -> trains all seeds; if any
                                                    .pt or per-seed prediction
                                                    file already exists, skip.
                                                    Aggregates ensemble at end
                                                    if all 5 are complete.
      python train_roberta_finetune.py --seed 43  -> trains only seed 43
                                                    (fresh process avoids MPS
                                                    memory accumulation).
      python train_roberta_finetune.py --aggregate -> just builds ensemble
                                                    from saved per-seed
                                                    predictions; no training.
    """
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=None,
                    help='train only this single seed (fresh-process mode)')
    ap.add_argument('--aggregate', action='store_true',
                    help='skip training; build ensemble from existing saved '
                         'per-seed predictions')
    args = ap.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)

    if not args.aggregate:
        print(f"Device: {DEVICE}")
        print("Preparing text data (rare-class word-swap augmentation)...")
        train_texts, y_train_arr, dev_texts, y_dev_arr = prepare_text_data()
        train_texts, y_train_arr = duplicate_rare_class_rows(train_texts,
                                                              y_train_arr)
        print(f"  train: {len(train_texts):,} texts (after augmentation)")
        print(f"  dev:   {len(dev_texts):,} texts")
        output_bias = bias_init_from_priors(y_train_arr)

        print("Tokenizing once for all seeds...")
        tokenizer = AutoTokenizer.from_pretrained(PRESET)
        train_ds = TextDataset(train_texts, y_train_arr, tokenizer)
        val_ds = TextDataset(dev_texts, y_dev_arr, tokenizer)

        seeds_to_run = [args.seed] if args.seed is not None else SEEDS
        for seed in seeds_to_run:
            preds_path = SAVE_DIR / f'model_seed_{seed}_dev_probs.npy'
            if preds_path.exists():
                print(f"\nseed {seed}: per-seed predictions already exist, "
                      f"skipping training")
                continue
            model, val_loader = train_one_seed(seed, train_ds, val_ds,
                                                output_bias)
            torch.save(model.state_dict(), SAVE_DIR / f'model_seed_{seed}.pt')
            # Move model to CPU before predict to dodge an MPS hang we
            # observed at the end of training runs (model finishes saving,
            # but predict_logits on MPS hangs forever in uninterruptible
            # sleep). CPU inference on 500 dev rows is ~5s; cheap.
            model.to('cpu')
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            logits = predict_logits(model, val_loader, device='cpu')
            probs = torch.sigmoid(logits).numpy()
            np.save(preds_path, probs)
            del model

    # Aggregation step (always, after training completes)
    pred_files = sorted(SAVE_DIR.glob('model_seed_*_dev_probs.npy'))
    if len(pred_files) == 0:
        print("\nNo per-seed prediction files found yet — nothing to aggregate.")
        return
    print(f"\nAggregating {len(pred_files)}/{len(SEEDS)} seed predictions...")
    all_probs = [np.load(p) for p in pred_files]
    ensemble_probs = np.mean(all_probs, axis=0)
    np.save(SAVE_DIR / 'dev_predictions.npy', ensemble_probs)

    # Recompute final F1 on dev (re-derive y_dev to avoid relying on training-
    # mode locals being defined when --aggregate is used standalone).
    import pandas as pd
    dev_csv = pd.read_csv('dev.csv', keep_default_na=False)
    label_lists = dev_csv['labels'].apply(lambda x: x.split()).tolist()
    idx = {emo: i for i, emo in enumerate(emotions)}
    y_dev = np.zeros((len(label_lists), len(emotions)), dtype=np.float32)
    for i, lbls in enumerate(label_lists):
        for lbl in lbls:
            if lbl in idx:
                y_dev[i, idx[lbl]] = 1.0
    final_f1 = float(f1_score_multi(y_dev, ensemble_probs))
    print(f"\n=== {PRESET}-finetuned ensemble dev F1 "
          f"({len(pred_files)}-seed): {final_f1:.4f} ===")

    with open(SAVE_DIR / 'config.json', 'w') as f:
        json.dump({
            'preset': PRESET, 'max_len': MAX_LEN, 'embed_dim': EMBED_DIM,
            'mode': 'finetuned-pytorch-mps', 'lr': LEARNING_RATE,
            'batch_size': BATCH_SIZE, 'max_epochs': MAX_EPOCHS,
            'patience': PATIENCE, 'label_smoothing': LABEL_SMOOTHING,
            'ensemble_dev_f1': final_f1, 'device': str(DEVICE),
            'seeds_used': [int(p.stem.split('_')[2]) for p in pred_files],
        }, f, indent=2)


if __name__ == '__main__':
    main()
