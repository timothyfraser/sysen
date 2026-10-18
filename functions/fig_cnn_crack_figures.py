# fig_cnn_crack_figures.py
# Draws the three figures of the CNN chapters (R and Python pages):
#   images/cnnr/panels_strip.png       4 cracked + 4 sound panels at 64 px
#   images/cnnr/cnn_loss_curves.png    torch run's training and validation loss
#   images/cnnr/threshold_tradeoff.png escape and false-alarm rates by threshold
# and copies each into images/cnnpy/ for the Python page.
#
# Usage (from the repo root):
#   python -X utf8 functions/fig_cnn_crack_figures.py PATH/TO/cracks64
# where PATH/TO/cracks64 is the unzipped 64 px pack (folders train/, valid/, test/,
# each with cracked/ and sound/). The scores come from workshops/crack_scores_reference.csv.
import os, sys, shutil
import numpy as np
import pandas as pd
from PIL import Image
from plotnine import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_R = os.path.join(ROOT, "docs-v3", "images", "cnnr")
OUT_PY = os.path.join(ROOT, "docs-v3", "images", "cnnpy")
pack = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "workshops", "cracks64")

# ---- 1. A strip of 8 panels: 4 cracked, then 4 sound (validation split, seeded draw) ----
rng = np.random.default_rng(5300)
tiles = []
for label in ["cracked", "sound"]:
    files = sorted(os.listdir(os.path.join(pack, "valid", label)))
    for f in rng.choice(files, size = 4, replace = False):
        tiles.append(np.array(Image.open(os.path.join(pack, "valid", label, f)).convert("L")))
gap = 6
scale = 2                                  # draw each 64 px panel at 128 px so it is visible
w = 8 * 64 * scale + 9 * gap
strip = np.full((64 * scale + 2 * gap, w), 255, dtype = np.uint8)
for i, t in enumerate(tiles):
    big = np.kron(t, np.ones((scale, scale), dtype = np.uint8))
    x0 = gap + i * (64 * scale + gap)
    strip[gap:gap + 64 * scale, x0:x0 + 64 * scale] = big
Image.fromarray(strip).save(os.path.join(OUT_R, "panels_strip.png"), optimize = True)

# ---- 2. Loss curves of the torch run (Python, CPU, 30 epochs) ----
loss = pd.DataFrame({
    "epoch": range(1, 31),
    "train": [0.266, 0.070, 0.053, 0.064, 0.035, 0.031, 0.029, 0.026, 0.030, 0.020,
              0.021, 0.019, 0.023, 0.023, 0.019, 0.020, 0.016, 0.017, 0.015, 0.012,
              0.012, 0.013, 0.011, 0.011, 0.010, 0.011, 0.012, 0.010, 0.010, 0.010],
    "valid": [0.087, 0.056, 0.061, 0.057, 0.033, 0.037, 0.029, 0.046, 0.031, 0.025,
              0.022, 0.020, 0.021, 0.020, 0.014, 0.019, 0.015, 0.012, 0.012, 0.011,
              0.012, 0.011, 0.011, 0.012, 0.012, 0.015, 0.010, 0.013, 0.013, 0.008]})
long = loss.melt(id_vars = "epoch", var_name = "set", value_name = "loss")
long["set"] = long["set"].map({"train": "Training", "valid": "Validation"})
p = (ggplot(long, aes(x = "epoch", y = "loss", color = "set"))
     + geom_line(size = 1)
     + labs(x = "Epoch", y = "Loss (binary cross entropy)", color = "")
     + theme_bw(base_size = 12)
     + theme(legend_position = "bottom"))
p.save(os.path.join(OUT_R, "cnn_loss_curves.png"), width = 6.5, height = 4.2, dpi = 150, verbose = False)

# ---- 3. Escape and false-alarm rates by threshold, validation panels only ----
scores = pd.read_csv(os.path.join(ROOT, "workshops", "crack_scores_reference.csv"))
valid = scores[scores["split"] == "valid"]
rows = []
for t in np.round(np.arange(0.05, 0.951, 0.05), 2):
    rows.append({"threshold": t,
                 "Escape rate": np.mean(valid.loc[valid["label"] == 1, "prob"] <= t),
                 "False alarm rate": np.mean(valid.loc[valid["label"] == 0, "prob"] > t)})
trade = pd.DataFrame(rows)
print(trade.to_string(index = False))
tl = trade.melt(id_vars = "threshold", var_name = "rate", value_name = "value")
p = (ggplot(tl, aes(x = "threshold", y = "value", color = "rate"))
     + geom_line(size = 1) + geom_point(size = 1.5)
     + geom_vline(xintercept = 0.5, linetype = "dashed")
     + scale_y_continuous(labels = lambda v: [f"{x:.1%}" for x in v])
     + labs(x = "Threshold", y = "Rate (validation set)", color = "")
     + theme_bw(base_size = 12)
     + theme(legend_position = "bottom"))
p.save(os.path.join(OUT_R, "threshold_tradeoff.png"), width = 6.5, height = 4.2, dpi = 150, verbose = False)

# ---- the Python page uses its own folder ----
for f in ["panels_strip.png", "cnn_loss_curves.png", "threshold_tradeoff.png"]:
    shutil.copy2(os.path.join(OUT_R, f), os.path.join(OUT_PY, f))
    print("wrote", f, Image.open(os.path.join(OUT_R, f)).size)
