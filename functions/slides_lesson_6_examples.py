# slides_lesson_6_examples.py -- Python twin of slides_lesson_6_examples.R
#
# Feeds: Lesson 6 slides 23-29 (Examples 1-2, min-Cpk table, design table, index chart).
# Run from the top of the repo:  python3 functions/slides_lesson_6_examples.py
# Reads:  workshops/product_weights.csv, capability_example2.csv, capability_index_chart.csv
# Writes: docs-v3/images/slides/lesson-6/gen_ex2_xbar_r_py.png, gen_ex_index_plot_py.png,
#         gen_ex1_dist_vs_spec_py.png, gen_ex2_dist_vs_spec_py.png
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
      # one filled circle (shape 21 in R) per index, told apart by fill only
      + geom_point(idx, aes('characteristic', 'value', fill='index'), shape='o', size=5,
                   stroke=0.6, color='#262626', position=position_dodge(width=0.5))
      + scale_fill_manual(values=[red, '#1F4E79', '#E0A526', '#6B8E7F'])
      + scale_y_continuous(limits=(0, 3), breaks=np.arange(0, 3.01, 0.5))
      + labs(x='Characteristic', y='Capability / performance index', fill='')
      + theme_classic(base_size=20) + theme(legend_position='top'))
g2.save(f"{outdir}/gen_ex_index_plot_py.png", width=7.5, height=5.5, dpi=150, verbose=False)

# Example 1: observed distribution vs the one-sided spec limit (LSL 250 g)
w['weight'] = 250 + w['x']
lab1 = pd.DataFrame({'x': [250, mu], 'y': [np.inf, np.inf],
                     'label': ['LSL 250', f'mean {mu:.2f}'], 'col': [red, '#262626']})
g3 = (ggplot(w, aes(x='weight'))
      + annotate('rect', xmin=-np.inf, xmax=250, ymin=-np.inf, ymax=np.inf, fill=red, alpha=0.12)
      + geom_histogram(binwidth=0.5, boundary=250, fill='#999999', color='white')
      + geom_vline(xintercept=250, color=red, size=1.6)
      + geom_vline(xintercept=mu, color='#262626', linetype='dashed', size=1.1)
      + geom_label(lab1, aes(x='x', y='y', label='label', color='col'), va='top',
                   size=17, label_size=0, inherit_aes=False)
      + scale_color_identity()
      + scale_x_continuous(limits=(248.5, 257), breaks=np.arange(248, 257.1, 1))
      + scale_y_continuous(expand=(0, 0, 0.2, 0))
      + labs(x='Weight (g), 110 units', y='Count')
      + theme_classic(base_size=20))
g3.save(f"{outdir}/gen_ex1_dist_vs_spec_py.png", width=6, height=4.4, dpi=150, verbose=False)

# Example 2: observed distribution vs LSL 0.5 and USL 0.9, out-of-spec shaded
lab2 = pd.DataFrame({'x': [lo, up, xb], 'y': [np.inf] * 3,
                     'label': ['LSL 0.5', 'USL 0.9', f'mean {xb:.3f}'],
                     'col': [red, red, '#262626']})
g4 = (ggplot(e, aes(x='x'))
      + annotate('rect', xmin=-np.inf, xmax=lo, ymin=-np.inf, ymax=np.inf, fill=red, alpha=0.12)
      + annotate('rect', xmin=up, xmax=np.inf, ymin=-np.inf, ymax=np.inf, fill=red, alpha=0.12)
      + geom_histogram(binwidth=0.05, center=0.5, fill='#999999', color='white')
      + geom_vline(xintercept=[lo, up], color=red, size=1.6)
      + geom_vline(xintercept=xb, color='#262626', linetype='dashed', size=1.1)
      + geom_label(lab2, aes(x='x', y='y', label='label', color='col'), va='top',
                   size=17, label_size=0, inherit_aes=False)
      + scale_color_identity()
      + scale_x_continuous(limits=(0.4, 1.0), breaks=np.arange(0.4, 1.01, 0.1))
      + scale_y_continuous(expand=(0, 0, 0.2, 0))
      + labs(x=f'Measurement, {len(e)} units', y='Count')
      + theme_classic(base_size=20))
g4.save(f"{outdir}/gen_ex2_dist_vs_spec_py.png", width=6, height=3.9, dpi=150, verbose=False)
print("Wrote gen_ex2_xbar_r_py.png, gen_ex_index_plot_py.png, gen_ex1_dist_vs_spec_py.png, gen_ex2_dist_vs_spec_py.png")
