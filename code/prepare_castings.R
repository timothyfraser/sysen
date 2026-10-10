# prepare_castings.R
# Shrinks the Kaggle casting photos to 64 x 64 grayscale PNGs and sorts them into
# train / valid / test folders, following the course's split list (castings_split.csv).
# The split list already leaves out 65 test photos that duplicate training photos.
#
# RESIZE METHOD (identical in the Python twin, code/prepare_castings.py):
#   1. Convert to 8-bit grayscale with the ITU-R 601 luma weights
#      (0.299 R + 0.587 G + 0.114 B), rounded to the nearest integer.
#   2. Shrink to 64 x 64 with an antialiased bilinear ("triangle") filter,
#      horizontal pass then vertical pass, rounding to 8 bits after each pass.
#   This is what Pillow's Image.BILINEAR does when shrinking. The functions
#   below re-implement that filter, so R and Python write the same pixels
#   (to within one gray level).
#
# 1. Download the dataset from Kaggle (free account needed) and unzip it:
#    https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
# 2. Tell the script where the unzipped "casting_data/casting_data" folder is,
#    either by setting the KAGGLE_DIR environment variable (Sys.setenv(KAGGLE_DIR = "...")
#    before you run this) or by editing the default below.
# 3. Run this script from the top of the course repo. It takes about a minute.
#
# If the Kaggle folder is not there, the script says so and stops without error.

KAGGLE_DIR = Sys.getenv("KAGGLE_DIR", "~/Downloads/casting_archive/casting_data/casting_data")   # folder containing train/ and test/
KAGGLE_DIR = path.expand(KAGGLE_DIR)
OUT_DIR    = "workshops/castings"
KAGGLE_URL = "https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product"

if(!(dir.exists(file.path(KAGGLE_DIR, "train")) && dir.exists(file.path(KAGGLE_DIR, "test")))){
  cat("Download the Kaggle casting dataset first:", KAGGLE_URL, "\n")
  cat("Unzip it, then point this script at the casting_data/casting_data folder\n")
  cat("(set the KAGGLE_DIR environment variable, or edit KAGGLE_DIR above).\n")
  cat("Looked in:", KAGGLE_DIR, "\n")
} else {

library(dplyr)
library(readr)

split_list = read_csv("workshops/castings_split.csv", show_col_types = FALSE)

# Weights of an antialiased bilinear (triangle) filter that shrinks n_in pixels to n_out
# (the same weights Pillow uses). Returns an n_out x n_in matrix; each row sums to 1.
shrink_weights = function(n_in, n_out){
  scale = n_in / n_out
  width = max(scale, 1)                       # filter widens when shrinking = antialiasing
  w = matrix(0, nrow = n_out, ncol = n_in)
  for(i in seq_len(n_out)){
    center = (i - 0.5) * scale                # center of output pixel i, in input coordinates
    lo = max(floor(center - width + 0.5), 0)
    hi = min(floor(center + width + 0.5), n_in)
    x = (seq(lo, hi - 1) + 0.5 - center) / width
    k = pmax(1 - abs(x), 0)                   # triangle filter
    w[i, (lo + 1):hi] = k / sum(k)
  }
  w
}

shrink = function(path, size = 64){
  img = jpeg::readJPEG(path)                                         # values in 0-1
  if(length(dim(img)) == 3){                                         # color -> 8-bit luma
    r = round(255 * img[, , 1]); g = round(255 * img[, , 2]); b = round(255 * img[, , 3])
    img = floor((r * 19595 + g * 38470 + b * 7471 + 32768) / 65536)
  } else { img = round(255 * img) }
  wy = shrink_weights(nrow(img), size)
  wx = shrink_weights(ncol(img), size)
  tmp = pmin(pmax(round(img %*% t(wx)), 0), 255)                     # horizontal pass, back to 8 bits
  out = pmin(pmax(round(wy %*% tmp), 0), 255)                        # vertical pass
  out / 255
}

for(i in seq_len(nrow(split_list))){
  row = split_list[i, ]
  dest = file.path(OUT_DIR, row$split, row$label)
  dir.create(dest, recursive = TRUE, showWarnings = FALSE)
  png::writePNG(shrink(file.path(KAGGLE_DIR, row$file)),
                file.path(dest, sub("\\.jpeg$", ".png", basename(row$file))))
}

print(split_list %>% count(split, label))

}
