# cnn_sweep.py
# An offline reference sweep of the course's torch CNN on the crack panels.
# It trains the small chapter network at four data amounts and three picture
# sizes (12 cells), plus three tuning runs (3 cells), and writes what the
# reference got on the validation panels to docs-v3/data/nn/cnn_sweep.json.
# The ML Lab trainer draws that file as a faint overlay behind your own runs.
#
# Run it from the repo root (needs the 64 px panels, see cnn_torch_py.py):
#   pip install torch numpy pillow
#   python -X utf8 functions/cnn_sweep.py --src workshops/cracks64
#   python -X utf8 functions/cnn_sweep.py --src workshops/cracks64 --resume   # finish a partial file
#
# The 16 and 32 px cells shrink the 64 px panels in memory (LANCZOS), so no
# photos are written anywhere. Every random choice starts from seed 5300.

import argparse, json, os, time
import numpy as np
import torch
from torch import nn
from PIL import Image

SEED = 5300
THRESHOLDS = [round(0.05 * i, 2) for i in range(1, 20)]
HIST_BINS = 20
N_GRID = [100, 500, 2000, 6000]
PX_GRID = [16, 32, 64]
# The reference network is 2 conv layers with 8 filters in the first, doubling after.
REFERENCE = {"conv_layers": 2, "filters": 8, "learning_rate": 0.001, "epochs": 10,
             "flips": True, "batch_size": 32}
# The three tuning runs, all at 2,000 panels and 32 px.
TUNING = [("lr0.0001", {"learning_rate": 0.0001}),
          ("lr0.01", {"learning_rate": 0.01}),
          ("conv1", {"conv_layers": 1})]


def read_split(root, px):
    """All panels of one split as (x, y): x is n x 1 x px x px in 0..1, y is 1 if cracked.
    Rows are interleaved cracked/sound, in a seed-5300 order, so any prefix is balanced."""
    rng = np.random.default_rng(SEED)
    per_class = []
    for c in ("cracked", "sound"):
        d = os.path.join(root, c)
        names = sorted(os.listdir(d))
        per_class.append([os.path.join(d, n) for n in rng.permutation(names)])
    paths = [p for pair in zip(*per_class) for p in pair]
    ys = [1, 0] * (len(paths) // 2)
    xs = []
    for p in paths:
        im = Image.open(p).convert("L")
        if px != im.size[0]:
            im = im.resize((px, px), Image.LANCZOS)
        xs.append(np.asarray(im, dtype=np.float32) / 255)
    x = torch.from_numpy(np.stack(xs)).unsqueeze(1)
    return x, torch.tensor(ys, dtype=torch.float32)


def make_net(px, conv_layers, filters):
    layers, ch, side = [], 1, px
    for i in range(conv_layers):
        f = filters * 2 ** i
        layers += [nn.Conv2d(ch, f, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2)]
        ch, side = f, side // 2
    layers += [nn.Flatten(), nn.Linear(ch * side * side, 64), nn.ReLU(), nn.Linear(64, 1)]
    return nn.Sequential(*layers)


def predict(model, x):
    model.eval()
    with torch.no_grad():
        return torch.sigmoid(model(x)).flatten().numpy()


def rates_at(probs, y):
    cracked, sound = probs[y == 1], probs[y == 0]
    esc = [float(np.mean(cracked < t)) for t in THRESHOLDS]      # cracked scored below t
    fa = [float(np.mean(sound >= t)) for t in THRESHOLDS]        # sound scored at or above t
    return esc, fa


def hist(probs, y):
    out = {}
    for name, v in (("sound", 0), ("cracked", 1)):
        b = np.minimum(HIST_BINS - 1, np.floor(probs[y == v] * HIST_BINS).astype(int))
        out[name] = np.bincount(b, minlength=HIST_BINS).tolist()
    return out


def run_cell(data, cell_id, kind, n, px, conv_layers, filters, lr, epochs, batch):
    t0 = time.time()
    torch.manual_seed(SEED)
    gen = torch.Generator().manual_seed(SEED)
    xtr, ytr = data["train"][px]
    xtr, ytr = xtr[:n], ytr[:n]
    model = make_net(px, conv_layers, filters)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.0001)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        model.train()
        order = torch.randperm(len(xtr), generator=gen)
        for i in range(0, len(xtr), batch):
            idx = order[i:i + batch]
            xb = xtr[idx]
            if torch.rand(1, generator=gen).item() < 0.5:        # flips, as in the chapter
                xb = torch.flip(xb, dims=[3])
            if torch.rand(1, generator=gen).item() < 0.5:
                xb = torch.flip(xb, dims=[2])
            opt.zero_grad()
            loss_fn(model(xb), ytr[idx].unsqueeze(1)).backward()
            opt.step()
    xv, yv = data["valid"][px]
    xt, yt = data["test"][px]
    pv = predict(model, xv)
    esc, fa = rates_at(pv, yv.numpy())
    pt, ytn = predict(model, xt), yt.numpy()
    called = pt >= 0.5
    conf = {"tn": int(np.sum(~called & (ytn == 0))), "fp": int(np.sum(called & (ytn == 0))),
            "fn": int(np.sum(~called & (ytn == 1))), "tp": int(np.sum(called & (ytn == 1)))}
    return {
        "id": cell_id, "kind": kind, "n_train": n, "px": px,
        "conv_layers": conv_layers, "filters": filters, "learning_rate": lr, "epochs": epochs,
        "valid": {"escape_rate": esc, "false_alarm_rate": fa},
        "hist": hist(pv, yv.numpy()),
        "test_confusion_at_0.5": conf,
        "seconds": round(time.time() - t0, 1),
    }


def plan(epochs):
    """The 15 cells in the order they run: small and quick first, so a partial file is useful."""
    ref = REFERENCE
    cells = []
    for n in N_GRID:
        for px in PX_GRID:
            cells.append((f"n{n}-px{px}", "grid", n, px, ref["conv_layers"], ref["filters"], ref["learning_rate"]))
    for tag, change in TUNING:
        cells.append((f"n2000-px32-{tag}", "tuning", 2000, 32,
                      change.get("conv_layers", ref["conv_layers"]), ref["filters"],
                      change.get("learning_rate", ref["learning_rate"])))
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="workshops/cracks64", help="folder with train/valid/test, cracked/sound PNGs (64 px)")
    ap.add_argument("--out", default="docs-v3/data/nn/cnn_sweep.json")
    ap.add_argument("--manifest", default="docs-v3/data/nn/packs-manifest.json")
    ap.add_argument("--epochs", type=int, default=REFERENCE["epochs"])
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--resume", action="store_true", help="keep cells already in --out and run the rest")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)

    manifest_version = json.load(open(a.manifest, encoding="utf-8"))["version"]
    ref = dict(REFERENCE, epochs=a.epochs)
    done = {}
    if a.resume and os.path.exists(a.out):
        old = json.load(open(a.out, encoding="utf-8"))
        if old.get("reference") == ref:
            done = {c["id"]: c for c in old["cells"]}

    data = {s: {px: read_split(os.path.join(a.src, s), px) for px in PX_GRID}
            for s in ("train", "valid", "test")}
    # one shared order across sizes: the 16 and 32 px tensors are the same panels as the 64 px ones
    # (read_split is seeded, so the permutation is identical for each size)

    cells = plan(a.epochs)
    results = []

    def save(partial):
        doc = {"version": 1, "manifest_version": manifest_version, "seed": SEED,
               "thresholds": THRESHOLDS, "hist_bins": HIST_BINS, "reference": ref,
               "source": "functions/cnn_sweep.py: the course torch CNN, trained offline on the 64 px "
                         "panels (16 and 32 px shrunk from them), AdamW, final-epoch weights, "
                         "scored on the 1,000 validation panels",
               "cells": results}
        if partial:
            doc["partial"] = True
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(doc, f, separators=(",", ":"))

    for (cid, kind, n, px, cl, fl, lr) in cells:
        if cid in done:
            results.append(done[cid])
            print("kept", cid, flush=True)
        else:
            c = run_cell(data, cid, kind, n, px, cl, fl, lr, a.epochs, ref["batch_size"])
            results.append(c)
            print(f"{cid}: escape@0.5 {c['valid']['escape_rate'][9]:.3f} "
                  f"false alarm {c['valid']['false_alarm_rate'][9]:.3f} {c['seconds']}s", flush=True)
        save(partial=len(results) < len(cells))
    save(partial=False)
    print("wrote", a.out, len(results), "cells")


if __name__ == "__main__":
    main()
