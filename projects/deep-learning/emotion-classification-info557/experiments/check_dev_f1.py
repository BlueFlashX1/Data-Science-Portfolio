import json, keras, numpy as np, pandas as pd
from train_dev import f1_score, ensemble_predict, emotions

with open('saved_models/vocab.json') as f:
    vocab = json.load(f)
vec = keras.layers.TextVectorization(max_tokens=10000, output_mode='int')
vec.set_vocabulary(vocab)

models = [keras.models.load_model(f'saved_models/model_seed_{s}.keras',
                                   custom_objects={'f1_score': f1_score})
          for s in [42, 43, 44, 45, 46]]

dev = pd.read_csv('dev.csv', keep_default_na=False)

# multi-hot encode gold labels (empty label string => all-zero row, which is valid)
y_true = np.zeros((len(dev), len(emotions)), dtype=np.float32)
for i, lbl_str in enumerate(dev['labels']):
    for lbl in lbl_str.split():
        if lbl in emotions:
            y_true[i, emotions.index(lbl)] = 1

probs = ensemble_predict(models, vec(dev['text']).numpy())

# Use train_dev's own f1_score (the same one that produced the 0.7218 figure)
f1_train_dev = f1_score(y_true, probs).numpy()
print(f"\ntrain_dev.f1_score on dev (threshold 0.5): {f1_train_dev:.4f}")

# Also report sklearn-style macro / micro for context
y_pred = (probs >= 0.5).astype(int).astype(np.float32)
def f1(t, p):
    tp = ((t == 1) & (p == 1)).sum()
    fp = ((t == 0) & (p == 1)).sum()
    fn = ((t == 1) & (p == 0)).sum()
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec  = tp / (tp + fn) if (tp + fn) else 0
    return 2 * prec * rec / (prec + rec) if (prec + rec) else 0

micro = f1(y_true.flatten(), y_pred.flatten())
macro = np.mean([f1(y_true[:, i], y_pred[:, i]) for i in range(len(emotions))])

print(f"Micro-F1 (manual)                         : {micro:.4f}")
print(f"Macro-F1 (manual)                         : {macro:.4f}")
print(f"\nDev rows with NO label: {(y_true.sum(axis=1) == 0).sum()} / {len(dev)}")
print(f"Dev rows with multi-label: {(y_true.sum(axis=1) > 1).sum()} / {len(dev)}")
