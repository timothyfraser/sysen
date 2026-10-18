# functions/crack_scores_reference.py
# Rebuild docs-v3/data/nn/crack_scores_reference.csv: train the course's torch CNN
# (functions/cnn_torch_py.py, run unchanged) and write its probability of "cracked"
# for every validation and test panel, keyed to the pack's index.json.
#
# Usage (from the repository root):
#   python -X utf8 -P functions/crack_scores_reference.py --index <path to index.json>
# index.json comes with the image packs (built by functions/crack_packs.py).
import argparse
import json
import os
import runpy

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--index", required=True, help="the packs' index.json")
ap.add_argument("--out", default=os.path.join("docs-v3", "data", "nn", "crack_scores_reference.csv"))
args = ap.parse_args()

g = runpy.run_path(os.path.join("functions", "cnn_torch_py.py"), run_name="__main__")
idx = json.load(open(args.index, encoding="utf-8"))
predict_probs = g["predict_probs"]

rows = []
for split in ["valid", "test"]:
    ds = g[split + "_data"]
    res = predict_probs(g[split + "_loader"])
    # the validation and test loaders are not shuffled, so res rows follow ds.samples
    key = {}
    for (path, lab), p in zip(ds.samples, res["prob"]):
        name = os.path.splitext(os.path.basename(path))[0]
        key[(name[0], name[1:])] = (lab, p)
    for e in idx:
        if e["split"] != split:
            continue
        base = os.path.splitext(os.path.basename(e["source"]))[0]
        pre = "p" if e["source"].startswith("Positive") else "n"
        lab, p = key[(pre, base)]
        # folders sort alphabetically, so class 0 = cracked; index.json uses 1 = cracked
        assert (lab == 0) == (e["label"] == 1), e
        rows.append((split, e["order"], e["source"], e["label"], round(float(p), 4)))

out = pd.DataFrame(rows, columns=["split", "order", "source", "label", "prob"])
out.to_csv(args.out, index=False, float_format="%.4f")
print("wrote", len(out), "rows to", args.out)
