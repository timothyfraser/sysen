# cnn_plain_net.py: a plain (non-convolutional) network on the 16 x 16 crack panels.
# Reads workshops/cracks16.csv; prints validation accuracy, escape rate, weights.
# (A numpy-only version may replace scikit-learn here for speed in the browser.)
import warnings
import pandas as pd
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")                               # 200 steps is a cap, not a goal

cracks = pd.read_csv("workshops/cracks16.csv")
pix = [c for c in cracks.columns if c.startswith("p")]
train = cracks[cracks["split"] == "train"]
valid = cracks[cracks["split"] == "valid"]

net = MLPClassifier(hidden_layer_sizes=(8,), alpha=0.01,
                    solver="lbfgs", max_iter=200, random_state=5300)
net.fit(train[pix] / 255, train["label"])                       # scale to 0-1

prob = net.predict_proba(valid[pix] / 255)[:, 1]
guess = (prob > 0.5).astype(int)                                # threshold 0.5
accuracy = (guess == valid["label"]).mean()
escape = (guess[valid["label"] == 1] == 0).mean()              # cracked, called sound
weights = sum(w.size for w in net.coefs_) + sum(b.size for b in net.intercepts_)
print("validation accuracy:", round(accuracy, 3))
print("escape rate:", round(escape, 3))
print("weights:", weights)
