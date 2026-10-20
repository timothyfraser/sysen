# slides_recitation_7_lambda.py ----------------------------------------------
# Python twin of slides_recitation_7_lambda.R (Recitation 11, "Choosing the percentile").
# Run from the repo root:  python functions/slides_recitation_7_lambda.py
# Output: docs-v3/images/slides/recitation-7/gen_sampling_ci_py.png
import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2
from plotnine import *
sys.path.append('functions')
from functions_kfactors import qk

r = 20
lambda_hat = 0.002
# k factors: lower uses r, upper uses r + 1 (Table 2, time-censored)
k = np.array(qk(p = [0.025, 0.975], r = r, time = True))
bounds = k * lambda_hat   # 0.00122, 0.00309

# Sampling distribution of lambda: lambda-hat x chi-square(2r) / 2r
lam = np.linspace(0, 0.0055, 400)
curve = pd.DataFrame({"lambda_": lam,
    "density": chi2.pdf(lam * 2 * r / lambda_hat, df = 2 * r) * 2 * r / lambda_hat})
top = curve["density"].max()

marks = pd.DataFrame({"lambda_": [bounds[0], lambda_hat, bounds[1]],
    "label": ["$\\lambda_{2.5}$", "$\\hat{\\lambda}$", "$\\lambda_{97.5}$"]})
inside = curve[(curve["lambda_"] >= bounds[0]) & (curve["lambda_"] <= bounds[1])]

mychart = (ggplot(curve, aes(x = "lambda_", y = "density")) +
  geom_area(data = inside, fill = "#fbecec") +
  geom_line(color = "#B31B1B", size = 1.2) +
  geom_segment(data = marks, mapping = aes(x = "lambda_", xend = "lambda_", y = 0, yend = top * 1.08),
               inherit_aes = False, color = "#2a1414") +
  geom_text(data = marks, mapping = aes(x = "lambda_", y = top * 1.18, label = "label"),
            inherit_aes = False, size = 18) +
  scale_x_continuous(breaks = [bounds[0], lambda_hat, bounds[1]], labels = ["0.0012", "0.002", "0.0031"]) +
  theme_classic(base_size = 18) +
  theme(axis_text_y = element_blank(), axis_ticks_major_y = element_blank(), axis_line_y = element_blank(),
        figure_size = (7, 4.2)) +
  labs(x = "Failure rate per hour", y = "",
       caption = "r = 20 failures, alpha = 0.05, Type I (time) censoring"))
mychart.save("docs-v3/images/slides/recitation-7/gen_sampling_ci_py.png", dpi = 150, verbose = False)
print(bounds.round(5))
