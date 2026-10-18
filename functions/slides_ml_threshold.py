# slides_ml_threshold.py
# Draws the threshold trade-off figure for the machine learning lesson deck:
#   docs-v3/images/slides/lesson-ml/15_threshold_trade.png
# Escape rate (cracked panels passed) and false-alarm rate (sound panels flagged)
# as the decision threshold moves, from the reference CNN's validation scores in
# workshops/crack_scores_reference.csv. Sized for a projector (large text).
#
# Usage (from the repo root):
#   python -X utf8 functions/slides_ml_threshold.py
import os
import numpy as np
import pandas as pd
from plotnine import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs-v3", "images", "slides", "lesson-ml")
os.makedirs(OUT, exist_ok = True)

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
     + geom_line(size = 1.6) + geom_point(size = 2.5)
     + geom_vline(xintercept = 0.5, linetype = "dashed")
     + scale_color_manual(values = ["#B31B1B", "#2c6e9b"])
     + scale_y_continuous(labels = lambda v: [f"{x:.1%}" for x in v])
     + labs(x = "Threshold", y = "Rate (validation panels)", color = "")
     + theme_bw(base_size = 18)
     + theme(legend_position = "bottom"))
p.save(os.path.join(OUT, "15_threshold_trade.png"), width = 7, height = 5, dpi = 150, verbose = False)
