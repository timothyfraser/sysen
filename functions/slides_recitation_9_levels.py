# slides_recitation_9_levels.py
# Crops the grey scanner strip off the bottom of the 2025 "levels" figure,
# writing a generated copy and keeping the original untouched.
# Run from the repo root: python3 functions/slides_recitation_9_levels.py
from PIL import Image

src = "docs-v3/images/slides/recitation-9/07_levels.png"
out = "docs-v3/images/slides/recitation-9/gen_levels_cropped.png"
im = Image.open(src)
im.crop((0, 0, im.width, 182)).save(out)
print(out, im.width, 182)
