# slides_lesson_6_ci.py -----------------------------------------------------
#
# Python twin of functions/slides_lesson_6_ci.R. Bootstraps Cp for the onsen
# bathwater as the slides' Python code does (1000 resamples,
# np.random.seed(1), spec limits 42-50 C, sigma_short from subgroups by time)
# and draws the bootstrap distribution, its 2.5th-97.5th percentile interval
# and the observed Cp.
# Run from the top of the repo:
#   python functions/slides_lesson_6_ci.py
# Reads:  workshops/onsen.csv
# Writes: docs-v3/images/slides/lesson-6/gen_boot_ci_py.png

import numpy as np
import pandas as pd
from plotnine import *

red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-6"

def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)

water = pd.read_csv("workshops/onsen.csv")

np.random.seed(1)
boots = []
for r in range(1000):
    b = water.sample(n=len(water), replace=True)
    boots.append(b.assign(rep=r + 1))
myboot = pd.concat(boots, ignore_index=True)

s_w = myboot.groupby(['rep', 'time'])['temp'].std()
sigma_s = (s_w**2).groupby('rep').mean()**0.5
estimate = cp(sigma_s, upper=50, lower=42)
sw = water.groupby('time')['temp'].std()
cp0 = cp((sw**2).mean()**0.5, upper=50, lower=42)
myqi = pd.DataFrame({'cp': [cp0],
                     'lower': [estimate.quantile(0.025)],
                     'upper': [estimate.quantile(0.975)],
                     'se': [estimate.std()]})
print(myqi)

lo, hi = myqi['lower'][0], myqi['upper'][0]
boot = pd.DataFrame({'estimate': estimate.values})
labs_df = pd.DataFrame({'x': [lo, hi], 'y': [np.inf, np.inf],
                        'label': [f"2.5th\n{lo:.3f}", f"97.5th\n{hi:.3f}"]})
obs_df = pd.DataFrame({'x': [cp0], 'y': [np.inf],
                       'label': [f"observed\nCp = {cp0:.3f}"]})

g = (ggplot(boot, aes(x='estimate'))
     + annotate('rect', xmin=lo, xmax=hi, ymin=-np.inf, ymax=np.inf, fill='#d9d9d9')
     + geom_histogram(bins=40, fill='#8c8c8c', color='white', size=0.2)
     + geom_vline(xintercept=[lo, hi], color='#333333', linetype='dashed', size=0.9)
     + geom_vline(xintercept=cp0, color=red, size=2)
     + geom_label(data=labs_df, mapping=aes(x='x', y='y', label='label'),
                  va='top', size=16, label_size=0, inherit_aes=False)
     + geom_label(data=obs_df, mapping=aes(x='x', y='y', label='label'),
                  va='top', nudge_y=0, size=17, color=red, fontweight='bold',
                  label_size=0, inherit_aes=False)
     + scale_y_continuous(expand=(0, 0, 0.75, 0))
     + labs(x='Bootstrapped Cp (1,000 reps)', y='Count')
     + theme_classic(base_size=20))
g.save(f"{outdir}/gen_boot_ci_py.png", width=5, height=4.4, dpi=150, verbose=False)
print("Wrote", f"{outdir}/gen_boot_ci_py.png")
