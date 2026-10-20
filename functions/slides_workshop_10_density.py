# slides_workshop_10_density.py ---------------------------------------------
# Python twin of slides_workshop_10_density.R (pandas + plotnine).
# Run from the top of the repo:
#   python -X utf8 -P functions/slides_workshop_10_density.py
# Writes: docs-v3/images/slides/workshop-10/gen_density_stress_py.png
import numpy as np
import pandas as pd
from scipy.stats import weibull_min
from plotnine import *

af = 3
def f_s(t):
    return weibull_min.pdf(t, c=1.2, scale=4500)   # density under stress
def f_u(t):
    return (1 / af) * f_s(t / af)                  # density under normal use

t = np.linspace(1, 12500, 400)
data = pd.concat([
    pd.DataFrame({"t": t, "density": f_s(t), "Conditions": "Stress"}),
    pd.DataFrame({"t": t, "density": f_u(t), "Conditions": "Normal Usage"})])

print(data.groupby("Conditions").apply(lambda d: pd.Series({"peak": d.density.max(), "at_t": d.t.iloc[d.density.argmax()]})))

g = (ggplot(data, aes(x="t", y="density", color="Conditions", linetype="Conditions"))
     + geom_line(size=1.6)
     + scale_color_manual(values={"Stress": "#3880c0", "Normal Usage": "#B31B1B"})
     + scale_linetype_manual(values={"Stress": "solid", "Normal Usage": "dashed"})
     + labs(x="Airbag lifespan in hours (t)", y="Density, f(t)")
     + theme_minimal(base_size=20)
     + theme(legend_position="bottom", plot_margin=0.01))   # tight margins: shown ~540 px wide
g.save("docs-v3/images/slides/workshop-10/gen_density_stress_py.png", width=7, height=4.6, dpi=200, verbose=False)
