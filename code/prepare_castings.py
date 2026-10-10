# prepare_castings.py
# Shrinks the Kaggle casting photos to 64 x 64 grayscale PNGs and sorts them into
# train / valid / test folders, following the course's split list (castings_split.csv).
# The split list already leaves out 65 test photos that duplicate training photos.
#
# RESIZE METHOD (identical in the R twin, code/prepare_castings.R):
#   1. Convert to 8-bit grayscale with the ITU-R 601 luma weights
#      (0.299 R + 0.587 G + 0.114 B), rounded to the nearest integer.
#   2. Shrink to 64 x 64 with an antialiased bilinear ("triangle") filter,
#      horizontal pass then vertical pass, rounding to 8 bits after each pass.
#   This is exactly what Pillow's Image.BILINEAR does when shrinking. The R twin
#   re-implements the same filter, so both languages write the same pixels
#   (to within one gray level).
#
# 1. Download the dataset from Kaggle (free account needed) and unzip it:
#    https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
# 2. Tell the script where the unzipped "casting_data/casting_data" folder is,
#    either by setting the KAGGLE_DIR environment variable or by passing the
#    folder as the first argument:   python code/prepare_castings.py path/to/casting_data
#    (If you do neither, it looks in ~/Downloads/casting_archive/casting_data/casting_data.)
# 3. Run this script from the top of the course repo. It takes about a minute.
#
# If the Kaggle folder is not there, the script says so and stops without error.

import os
import sys

KAGGLE_DIR = os.path.expanduser(
    sys.argv[1] if len(sys.argv) > 1
    else os.environ.get("KAGGLE_DIR", "~/Downloads/casting_archive/casting_data/casting_data")
)   # folder containing train/ and test/
OUT_DIR = "workshops/castings"
KAGGLE_URL = "https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product"

if not (os.path.isdir(os.path.join(KAGGLE_DIR, "train")) and os.path.isdir(os.path.join(KAGGLE_DIR, "test"))):
    print("Download the Kaggle casting dataset first: " + KAGGLE_URL)
    print("Unzip it, then point this script at the casting_data/casting_data folder")
    print("(set the KAGGLE_DIR environment variable, or pass the folder as an argument).")
    print("Looked in: " + KAGGLE_DIR)
    sys.exit(0)

import pandas as pd
from PIL import Image

split_list = pd.read_csv("workshops/castings_split.csv")

for row in split_list.itertuples():
    dest = os.path.join(OUT_DIR, row.split, row.label)
    os.makedirs(dest, exist_ok = True)
    img = Image.open(os.path.join(KAGGLE_DIR, row.file)).convert("L")    # grayscale (luma)
    img = img.resize((64, 64), Image.BILINEAR)                           # antialiased bilinear
    img.save(os.path.join(dest, os.path.basename(row.file).replace(".jpeg", ".png")))

print(split_list.groupby(["split", "label"]).size())
