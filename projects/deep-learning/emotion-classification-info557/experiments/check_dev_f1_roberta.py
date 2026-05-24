"""Honest dev F1 re-evaluation for the RoBERTa-base ensemble.

Loads the per-seed dev probabilities that were saved at the end of each
seed's training run (via the same inference pipeline that would be used
at test time), averages them, computes F1 at threshold 0.5, and prints
both micro F1 and per-class F1.

This is the analog of `check_dev_f1.py` but for the PyTorch RoBERTa runs.

Run from project root:
    cd /path/to/graduate-project-matthewqilanthompson-1
    source venv/bin/activate
    python experiments/check_dev_f1_roberta.py
"""
import sys, os
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
from train_dev import emotions

SAVE_DIR = Path(__file__).parent / 'saved_models_roberta_finetune'


def f1(t, p):
    tp = ((t == 1) & (p == 1)).sum()
    fp = ((t == 0) & (p == 1)).sum()
    fn = ((t == 1) & (p == 0)).sum()
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    return 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0


def evaluate_ensemble(prob_files, y_true, label):
    all_probs = [np.load(p) for p in prob_files]
    ensemble_probs = np.mean(all_probs, axis=0)
    y_pred = (ensemble_probs >= 0.5).astype(np.float32)

    micro = f1(y_true.flatten(), y_pred.flatten())
    macro = np.mean([f1(y_true[:, i], y_pred[:, i])
                     for i in range(len(emotions))])

    print(f"\n=== {label} ({len(prob_files)} seeds) ===")
    print(f"Micro-F1 : {micro:.4f}")
    print(f"Macro-F1 : {macro:.4f}")
    print("\nPer-class F1:")
    for i, emo in enumerate(emotions):
        per_class = f1(y_true[:, i], y_pred[:, i])
        n_train_pos = int(y_true[:, i].sum())
        marker = ""
        if per_class == 0.0:
            marker = "  <-- still zero"
        elif emo in ('anger', 'annoyance', 'disapproval') and per_class > 0:
            marker = "  <-- came OFF zero"
        print(f"  {emo:12s} (n_dev={n_train_pos:3d}) : {per_class:.4f}{marker}")

    return ensemble_probs, micro, macro


def main():
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    # Load dev labels (multi-hot encoded, same as train_roberta_finetune does)
    dev = pd.read_csv('dev.csv', keep_default_na=False)
    y_true = np.zeros((len(dev), len(emotions)), dtype=np.float32)
    for i, lbl_str in enumerate(dev['labels']):
        for lbl in lbl_str.split():
            if lbl in emotions:
                y_true[i, emotions.index(lbl)] = 1.0

    print(f"Dev set: {len(dev)} rows, {len(emotions)} classes")
    print(f"Multi-label rows: {(y_true.sum(axis=1) > 1).sum()}")
    print(f"Zero-label rows : {(y_true.sum(axis=1) == 0).sum()}")

    all_files = sorted(SAVE_DIR.glob('model_seed_*_dev_probs.npy'))
    if not all_files:
        print(f"\nNo per-seed prediction files found in {SAVE_DIR}")
        print("Run train_roberta_finetune.py first.")
        return

    # 5-seed full ensemble
    evaluate_ensemble(all_files, y_true, label="5-seed full ensemble")

    # 4-seed peak (drop seed 46) — per decisions.txt this scored 0.8310
    files_no_46 = [p for p in all_files if 'seed_46' not in p.name]
    if len(files_no_46) == 4:
        evaluate_ensemble(files_no_46, y_true,
                          label="4-seed (drop seed 46, peak per decisions.txt)")

    # Verify against pre-aggregated ensemble file if it exists
    pre_agg = SAVE_DIR / 'dev_predictions.npy'
    if pre_agg.exists():
        cached = np.load(pre_agg)
        recomputed = np.mean([np.load(p) for p in all_files], axis=0)
        max_diff = np.abs(cached - recomputed).max()
        print(f"\nSanity: cached `dev_predictions.npy` vs recomputed: "
              f"max_abs_diff = {max_diff:.2e} "
              f"({'match' if max_diff < 1e-6 else 'MISMATCH'})")


if __name__ == '__main__':
    main()
