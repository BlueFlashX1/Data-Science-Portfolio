import json
import keras
import pandas as pd
from train_dev import f1_score, ensemble_predict, emotions

# AI assistance: GitHub Copilot inline autocomplete (https://github.com/features/copilot).                                                                     
# No prompts entered; suggestions came from code context as I typed.                                            
# Autocomplete contributed to: custom_objects arg in load_model line 19,                                                                                       
# to_csv compression block lines 28-32, closing print line 33.

with open('saved_models/vocab.json') as f:
    vocab = json.load(f)
vectorizer = keras.layers.TextVectorization(max_tokens=10000, output_mode='int')
vectorizer.set_vocabulary(vocab)

# load 5 models 
models = [
    keras.models.load_model(f'saved_models/model_seed_{s}.keras',
                            custom_objects={'f1_score': f1_score})
    for s in [42, 43, 44, 45, 46]
]

# predict on test set and write submission
test = pd.read_csv('test-in.csv', keep_default_na=False)
preds = (ensemble_predict(models, vectorizer(test['text']).numpy()) >= 0.5).astype(int)
test['labels'] = [' '.join(emotions[i] for i, v in enumerate(r) if v) for r in preds]

test[['text', 'labels']].to_csv(
    'submission.zip',
    index=False,
    compression=dict(method='zip', archive_name='submission.csv'),
)
print(f"Wrote submission.zip ({len(test)} predictions)")
