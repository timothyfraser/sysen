# slides_lesson_6_examples.py -- Python twin of slides_lesson_6_examples.R
#
# Feeds: Lesson 6 slides 28-35 (Examples 1-2, min-Cpk table, design table, index chart).
# Run from the top of the repo:  python3 functions/slides_lesson_6_examples.py
# Reads:  workshops/product_weights.csv, capability_example2.csv, capability_index_chart.csv
# Writes: docs-v3/images/slides/lesson-6/gen_ex2_xbar_r_py.png, gen_ex_index_plot_py.png
#         and prints Example 1 / Example 2 results and the two computed tables.
import pandas as pd
import numpy as np
from scipy.stats import norm
from plotnine import *

np.random.seed(12345)
red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-6"
d2, c4, A2, D3, D4 = 2.326, 0.94, 0.577, 0, 2.114

def subgroup_stats(df):
    return df.groupby('subgroup')['x'].agg(xbar='mean', r=lambda v: v.max() - v.min(),
                                            s='std', s2='var').reset_index()

# Example 1: x = weight - 250; LSL = 250 g (x = 0), one-sided
w = pd.read_csv("workshops/product_weights.csv")
ws = subgroup_stats(w)
mu = 250 + ws.xbar.mean(); ss = ws.r.mean() / d2; st = w.x.std()
print("==== Example 1 ====")
print(f"mu = {mu:.4f} [253.66]  Rbar = {ws.r.mean():.4f}  sigma_short = {ss:.4f} [1.074]  sigma_total = {st:.4f} [1.098]")
print(f"Cpk = {(mu - 250) / (3 * ss):.4f}  Ppk = {(mu - 250) / (3 * st):.4f}")

# Example 2
e = pd.read_csv("workshops/capability_example2.csv")
es = subgroup_stats(e)
lo, up = 0.5, 0.9
xb, rb, sb = es.xbar.mean(), es.r.mean(), es.s.mean()
ss2, st2 = rb / d2, e.x.std()
print("==== Example 2 ====")
print(f"xbbar = {xb:.4f} [0.7375]  Rbar = {rb:.4f} [0.1906]  sbar = {sb:.8f} [0.07627613]  sbar/c4 = {sb / c4:.4f} [0.0811]")
print(f"sigma_short = {ss2:.4f} [0.0819]  sigma_total = {st2:.6f} [0.081716]")
print(f"Cp = {(up - lo) / (6 * ss2):.4f} [0.8136]  Cpk = {min(up - xb, xb - lo) / (3 * ss2):.4f}")
print(f"Pp = {(up - lo) / (6 * st2):.4f} [0.8159]  Ppk = min({(up - xb) / (3 * st2):.4f}, {(xb - lo) / (3 * st2):.4f}) [0.6629, 0.9688]")

# Tables (the R script writes the CSVs; this prints the same numbers)
P = np.array([0.90, 0.95, 0.99, 0.997, 0.999])
print(pd.DataFrame({'enclosed': P, 'two_sided': norm.ppf(1 - (1 - P) / 2) / 3, 'one_sided': norm.ppf(P) / 3}).round(2))
k = np.array([3, 4, 5, 5.5, 6])
ppm = 1e6 * (norm.cdf(-(k - 1.5)) + norm.cdf(-(k + 1.5)))
print(pd.DataFrame({'sigma_level': k, 'cp': k / 3, 'cpk': k / 3 - 0.5, 'ppm': ppm,
                    'pct_conforming': 100 - ppm / 1e4,
                    'n_99': np.floor(np.log(0.99) / np.log(1 - ppm / 1e6)),
                    'n_999': np.floor(np.log(0.999) / np.log(1 - ppm / 1e6))}))

# X-bar and R chart pair
lab = {'xbar': 'Average (X-bar) chart', 'r': 'Range (R) chart'}
long = es.melt(id_vars='subgroup', value_vars=['xbar', 'r'], var_name='chart')
long['chart'] = pd.Categorical(long.chart.map(lab), categories=list(lab.values()))
lim = pd.DataFrame({'chart': pd.Categorical(list(lab.values()), categories=list(lab.values())),
                    'center': [xb, rb], 'lcl': [xb - A2 * rb, D3 * rb], 'ucl': [xb + A2 * rb, D4 * rb]})
g1 = (ggplot(long, aes('subgroup', 'value'))
      + geom_hline(lim, aes(yintercept='center'), color='grey')
      + geom_hline(lim, aes(yintercept='lcl'), color=red, linetype='dashed')
      + geom_hline(lim, aes(yintercept='ucl'), color=red, linetype='dashed')
      + geom_line() + geom_point(size=3, color=red)
      + facet_wrap('~chart', ncol=1, scales='free_y')
      + labs(x='Subgroup', y='') + theme_classic(base_size=20))
g1.save(f"{outdir}/gen_ex2_xbar_r_py.png", width=9, height=7, dpi=150, verbose=False)

# Index chart
idx = pd.read_csv("workshops/capability_index_chart.csv")
idx['index'] = pd.Categorical(idx['index'], categories=['Cp', 'Cpk', 'Pp', 'Ppk'])
spans = idx.groupby('characteristic')['value'].agg(lo='min', hi='max').reset_index()
g2 = (ggplot()
      + geom_hline(yintercept=[1, 1.5, 2], linetype='dashed', color='grey')
      + geom_linerange(spans, aes(x='characteristic', ymin='lo', ymax='hi'))
      + geom_point(idx, aes('characteristic', 'value', shape='index', fill='index'), size=4,
                   position=position_dodge(width=0.5))
      + scale_shape_manual(values=['o', 'o', '^', '^'])
      + scale_fill_manual(values=[red, 'white', '#4d4d4d', 'white'])
      + scale_y_continuous(limits=(0, 3), breaks=np.arange(0, 3.01, 0.5))
      + labs(x='Characteristic', y='Capability / performance index', shape='', fill='')
      + theme_classic(base_size=20) + theme(legend_position='top'))
g2.save(f"{outdir}/gen_ex_index_plot_py.png", width=10, height=6.5, dpi=150, verbose=False)
print("Wrote gen_ex2_xbar_r_py.png, gen_ex_index_plot_py.png")
