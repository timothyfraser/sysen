# Recitation 9 (Fault Tree Analysis) slide code, run from the repo root.
# Every chunk here is shown on a slide in docs-v3/slides/23_slides_recitation_9.html.
import os, sys
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath('functions'))
from functions_distributions import *

# -- Slide: the tree as data
edges = pd.DataFrame({'from': ["T", "G1", "G1", "G2", "G2", "G3", "G3"],
                      'to':   ["G1", "G2", "G3", "1", "2", "1", "3"]})
print(edges)

# -- Slide: data to Mermaid text
print("\n".join(edges['from'] + " --- " + edges['to']))

# -- Slide: the z multiplier
ci = 0.95
z = qnorm(1 - (1 - ci) / 2, mean=0, sd=1)
print(round(float(z), 2))

# -- Slide: z table values
zs = [1.28, 1.645, 1.96, 2.33, 2.58]
print(pd.DataFrame({'z': zs, 'phi': pnorm(zs).round(4)}))

# -- Slide: simulate uncertain lambda
np.random.seed(1)
lambdas = rnorm(1000, mean=0.001, sd=0.0001)   # CV = 10%
simprobs = pexp(100, rate=lambdas)              # P(fail by t = 100)
mu = simprobs.mean()
sigma = simprobs.std(ddof=1)
print(round(mu, 4), round(sigma, 4))

# -- Slide: confidence interval
n = len(simprobs)
ci_mean = mu + np.array([-1, 1]) * qnorm(0.975) * sigma / np.sqrt(n)
print(ci_mean.round(4))
