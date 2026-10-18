# functions/crack_packs.py
#
# Build the resized concrete-crack image packs that the course website serves
# same-origin from docs-v3/data/cracks/v1/, plus the manifest that tells the pages where everything is.
#
# Source: Ozgenel, C. F. & Gonenc Sorguc, A. (2018). Concrete Crack Images for
# Classification. Mendeley Data, v2. doi 10.17632/5y9wdsg2zt.2. CC BY 4.0.
# 40,000 RGB images, 227 x 227 px: Positive/ (cracked) and Negative/ (sound).
#
# What it writes into --out:
#   s16/ s32/ s64/   sprite sheets of the same 8,000 sampled panels
#                    (train 6,000 / valid 1,000 / test 1,000)
#   f32/             sprite sheets of 38,000 train panels at 32 px
#                    (the 6,000 s32 train panels first, same order)
#                    s32's train split writes no files of its own: its sheet
#                    names point at f32/train-000..005 (same pixels; the browser
#                    reads only the first n tiles of the last sheet)
#   cracks64.zip     only with --zip: the 8,000 sample at 64 px as PNGs, one
#                    folder per split/class (it is served as a GitHub release
#                    asset, ZIP_URL, never from the site)
#   manifest.json    sheet names, labels, byte counts, attribution
#   index.json       sample panel -> split, label, source file
# A sheet is 32 x 32 tiles (1,024 panels), row-major; unused cells are black.
# Labels: "0" = sound, "1" = cracked, one character per tile in tile order.
# index.json "order" is the tile position inside that split.
#
# Sheets are lossy WebP, quality 90, method 6 (about 18 MB for every pack).
# --lossless writes the old lossless sheets instead (PNG or WebP, whichever is
# smaller per pack; about 47 MB without the s32 duplicates).
#
# Run:  python -X utf8 -P functions/crack_packs.py --src C:/Users/tmf77/Downloads/cracks
#
# Plain-network table (small, ships in the repo; writes nothing else):
#   python -X utf8 -P functions/crack_packs.py --src C:/Users/tmf77/Downloads/cracks --plain16 workshops/cracks16.csv
# cracks16.csv = the first 600 train, 200 valid and 200 test tiles of the s16
# pack, in sheet order, one row per panel: split, label, p001..p256 (greyscale
# 0-255, row-major 16 x 16). Same sampling and same LANCZOS resize as s16.
#
# Deterministic: same source + seed = same sampling and order. Re-running
# rewrites every file. Only needs Pillow.

import argparse
import io
import json
import math
import random
import zipfile
from pathlib import Path

from PIL import Image

SEED = 5300
COLS = 32
TILES = COLS * COLS
N_PER_CLASS = 4000
SPLIT_PER_CLASS = {"train": 3000, "valid": 500, "test": 500}
CLASSES = ["sound", "cracked"]  # label 0, 1
# Relative to the page that reads the manifest (docs-v3/ml-lab/, docs-v3/chapters/).
BASE_URL = "../data/cracks/v1/"
ZIP_URL = "https://github.com/timothyfraser/sysen/releases/download/cracks-v1/cracks64.zip"
SITE_OUT = Path(__file__).resolve().parent.parent / "docs-v3" / "data" / "cracks" / "v1"

DATASET = {
    "title": "Concrete Crack Images for Classification",
    "authors": "Özgenel, Ç. F. & Gönenç Sorguç, A.",
    "year": 2018,
    "publisher": "Mendeley Data, v2",
    "doi": "10.17632/5y9wdsg2zt.2",
    "license": "CC BY 4.0",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "changes": "Converted to greyscale, resized from 227 px to 16, 32 or 64 px, "
               "sampled, and packed into sprite sheets by SIGMA.",
}
ZIP_BYTES = 21124439  # the published cracks64.zip (rebuild with --zip to re-measure)
ZIP_LAYOUT = "train/cracked, train/sound, valid/cracked, valid/sound, test/cracked, test/sound"


def list_class(src, folder):
    return sorted(p.name for p in (Path(src) / folder).glob("*.jpg"))


def balanced(rng, cracked, sound):
    """Alternate classes; the order inside each pair is a coin flip.
    Any prefix of N panels is within one of half cracked."""
    out = []
    for c, s in zip(cracked, sound):
        pair = [(c, 1), (s, 0)]
        rng.shuffle(pair)
        out.extend(pair)
    return out  # list of (filename, label)


def plan(src):
    """Return (sample splits, f32 train order) as lists of (filename, label)."""
    rng = random.Random(SEED)
    pos = list_class(src, "Positive")
    neg = list_class(src, "Negative")
    if len(pos) < 20000 or len(neg) < 20000:
        raise SystemExit(f"expected 20,000 images per class, found {len(pos)} / {len(neg)}")
    pick_pos = rng.sample(pos, N_PER_CLASS)
    pick_neg = rng.sample(neg, N_PER_CLASS)
    splits, a = {}, 0
    for name, k in SPLIT_PER_CLASS.items():
        splits[name] = balanced(rng, pick_pos[a:a + k], pick_neg[a:a + k])
        a += k
    held = splits["valid"] + splits["test"]
    train = splits["train"]
    taken_pos = {f for f, l in held + train if l == 1}
    taken_neg = {f for f, l in held + train if l == 0}
    rest_pos = [f for f in pos if f not in taken_pos]
    rest_neg = [f for f in neg if f not in taken_neg]
    rng.shuffle(rest_pos)
    rng.shuffle(rest_neg)
    f32 = list(train) + balanced(rng, rest_pos, rest_neg)
    return splits, f32


def src_path(src, fname, label):
    return Path(src) / ("Positive" if label == 1 else "Negative") / fname


def load_tiles(src, items, sizes):
    """items: [(fname, label)]. Returns {size: [PIL L image]} (greyscale, LANCZOS)."""
    out = {s: [] for s in sizes}
    for fname, label in items:
        with Image.open(src_path(src, fname, label)) as im:
            g = im.convert("L")
            for s in sizes:
                out[s].append(g.resize((s, s), Image.LANCZOS))
    return out


def make_sheet(tiles, px):
    sheet = Image.new("L", (COLS * px, COLS * px), 0)
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % COLS) * px, (i // COLS) * px))
    return sheet


def encode(sheet, fmt):
    buf = io.BytesIO()
    if fmt == "png":
        sheet.save(buf, "PNG", optimize=True, compress_level=9)
    elif fmt == "webp":
        sheet.save(buf, "WEBP", lossless=True, quality=100, method=4)
    elif fmt == "webp90":
        sheet.save(buf, "WEBP", quality=90, method=6)
    return buf.getvalue()


def pick_format(sheet, report, key):
    """Smallest of lossless PNG and lossless WebP on a pack's first sheet."""
    sizes = {f: len(encode(sheet, f)) for f in ("png", "webp")}
    report[key] = sizes
    return min(sizes, key=sizes.get)


def ext(fmt):
    return "webp" if fmt.startswith("webp") else fmt


def write_pack(out, key, px, split_items, tiles_by_split, fmt, alias=None):
    """Write sheets for one pack. Returns the manifest entry.
    alias: {split: pack} names that pack's sheets instead of writing files
    (s32 train -> f32 train, whose first 6,000 tiles are the same panels)."""
    alias = alias or {}
    entry = {"px": px, "format": ext(fmt), "tiles_per_sheet": TILES, "cols": COLS, "splits": {}}
    total = 0
    (Path(out) / key).mkdir(parents=True, exist_ok=True)
    for split, items in split_items.items():
        tiles = tiles_by_split[split]
        names = []
        for k in range(math.ceil(len(items) / TILES)):
            if split in alias:
                names.append(f"{alias[split]}/{split}-{k:03d}.{ext(fmt)}")
                continue
            name = f"{key}/{split}-{k:03d}.{ext(fmt)}"
            data = encode(make_sheet(tiles[k * TILES:(k + 1) * TILES], px), fmt)
            (Path(out) / name).write_bytes(data)
            total += len(data)
            names.append(name)
        entry["splits"][split] = {
            "n": len(items),
            "sheets": names,
            "labels": "".join(str(l) for _, l in items),
        }
    entry["bytes"] = total
    return entry


def write_zip(out, splits, tiles64):
    Path(out).mkdir(parents=True, exist_ok=True)
    path = Path(out) / "cracks64.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        for split, items in splits.items():
            for (fname, label), tile in zip(items, tiles64[split]):
                cls = "cracked" if label == 1 else "sound"
                stem = ("p" if label == 1 else "n") + Path(fname).stem
                buf = io.BytesIO()
                tile.save(buf, "PNG", optimize=True, compress_level=9)
                info = zipfile.ZipInfo(f"{split}/{cls}/{stem}.png", (2018, 1, 1, 0, 0, 0))
                z.writestr(info, buf.getvalue())
    return path.stat().st_size


PLAIN16_N = {"train": 600, "valid": 200, "test": 200}


def write_plain16(src, path):
    """One CSV row per panel: the first PLAIN16_N[split] tiles of each s16 split."""
    splits, _ = plan(src)
    lines = ["split,label," + ",".join(f"p{i:03d}" for i in range(1, 257))]
    for split, k in PLAIN16_N.items():
        items = splits[split][:k]
        tiles = load_tiles(src, items, (16,))[16]
        for (_, label), tile in zip(items, tiles):
            lines.append(f"{split},{label}," + ",".join(str(v) for v in tile.getdata()))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + "\n"
    Path(path).write_text(text, encoding="utf-8", newline="\n")
    size = Path(path).stat().st_size
    print(f"wrote {path}: {len(lines) - 1} panels x 256 pixels, {size:,} bytes")


def main():
    ap = argparse.ArgumentParser(description="Build the concrete-crack image packs.")
    ap.add_argument("--src", default="C:/Users/tmf77/Downloads/cracks")
    ap.add_argument("--out", default=str(SITE_OUT))
    ap.add_argument("--lossless", action="store_true",
                    help="write lossless sheets (smallest of PNG / WebP) instead of WebP q90")
    ap.add_argument("--zip", default="",
                    help="also write cracks64.zip to this folder (it is published as a release asset)")
    ap.add_argument("--site-manifest",
                    default=str(Path(__file__).resolve().parent.parent / "docs-v3" / "data" / "nn" / "packs-manifest.json"),
                    help="where to put a byte-identical copy of manifest.json ('' to skip)")
    ap.add_argument("--plain16", default="",
                    help="write only the 1,000-panel 16 px pixel table (cracks16.csv) to this path and stop")
    args = ap.parse_args()
    if args.plain16:
        write_plain16(args.src, args.plain16)
        return
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    splits, f32_train = plan(args.src)

    print("loading the 8,000 sampled panels at 16, 32 and 64 px ...")
    tiles = {s: {} for s in (16, 32, 64)}
    for split, items in splits.items():
        got = load_tiles(args.src, items, (16, 32, 64))
        for s in (16, 32, 64):
            tiles[s][split] = got[s]

    fmt_report, fmt_chosen = {}, {}
    for s in (16, 32, 64):
        first = make_sheet(tiles[s]["train"][:TILES], s)
        lossless = pick_format(first, fmt_report, f"s{s}")
        fmt_report[f"s{s}"]["webp_q90"] = len(encode(first, "webp90"))
        fmt_chosen[s] = lossless if args.lossless else "webp90"

    packs = {}
    for s in (16, 32, 64):
        key = f"s{s}"
        print(f"writing {key} ({fmt_chosen[s]}) ...")
        alias = {"train": "f32"} if s == 32 else None
        packs[key] = write_pack(out, key, s, splits, tiles[s], fmt_chosen[s], alias)

    print("loading the extra 32,000 panels at 32 px for f32 ...")
    f32_tiles = list(tiles[32]["train"])
    f32_tiles += load_tiles(args.src, f32_train[len(splits["train"]):], (32,))[32]
    f32_fmt = pick_format(make_sheet(f32_tiles[:TILES], 32), fmt_report, "f32")
    f32_fmt = f32_fmt if args.lossless else "webp90"
    if ext(f32_fmt) != packs["s32"]["format"]:
        raise SystemExit("s32 train aliases f32 sheets, so both packs need the same format")
    print(f"writing f32 ({f32_fmt}) ...")
    packs["f32"] = write_pack(out, "f32", 32, {"train": f32_train}, {"train": f32_tiles}, f32_fmt)

    if args.zip:
        print("writing cracks64.zip ...")
        zbytes = write_zip(args.zip, splits, tiles[64])
    else:
        zbytes = ZIP_BYTES

    index = []
    for split, items in splits.items():
        for i, (fname, label) in enumerate(items):
            index.append({"order": i, "split": split, "label": label,
                          "source": f"{'Positive' if label == 1 else 'Negative'}/{fname}"})
    (out / "index.json").write_text(json.dumps(index, separators=(",", ":")) + "\n",
                                    encoding="utf-8", newline="\n")

    manifest = {
        "version": 1,
        "dataset": DATASET,
        "base_url": BASE_URL,
        "classes": CLASSES,
        "seed": SEED,
        "packs": packs,
        "zip": {"file": ZIP_URL, "bytes": zbytes, "layout": ZIP_LAYOUT},
        "index": "index.json",
    }
    text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    (out / "manifest.json").write_text(text, encoding="utf-8", newline="\n")
    if args.site_manifest:
        dest = Path(args.site_manifest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
        print(f"manifest copy: {dest}")

    print("\nformat comparison (first train sheet, bytes):")
    for k, v in fmt_report.items():
        print(f"  {k}: " + ", ".join(f"{a}={b:,}" for a, b in v.items()))
    print("\n pack   format  px   sheets   bytes")
    for k, p in packs.items():
        n = sum(len(s["sheets"]) for s in p["splits"].values())
        print(f" {k:<5}  {p['format']:<6} {p['px']:>3}  {n:>6}  {p['bytes']:>12,}  ({p['bytes'] / 1e6:.1f} MB)")
    print(f" zip    zip      64         1  {zbytes:>12,}  ({zbytes / 1e6:.1f} MB, release asset)")


if __name__ == "__main__":
    main()
