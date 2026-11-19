# 13_workshop_which_fits_solutions.py
# Title: Which Distribution Fits? Worked Solutions
# Author: Tim Fraser

# For each lifespan data set, fit the exponential, Weibull, gamma and lognormal
# with get_mle(), and compare the four log-likelihoods.
# Run from the top of the project folder.

import sys
import pandas as pd
sys.path.append("functions")
from functions_mle import get_mle

dists = ["exponential", "weibull", "gamma", "lognormal"]

# One function: fit all four distributions to a vector of failure times.
# Give n_total and tmax if some units had not failed when the test stopped.
def compare(t, n_total = None, tmax = None):
  rows = pd.DataFrame({"dist": dists})
  rows["loglik"] = [float(get_mle(t = list(t), n_total = n_total, tmax = tmax, dist = d)["loglik"].iloc[0]) for d in dists]
  rows = rows.sort_values("loglik", ascending = False).reset_index(drop = True)
  rows["gap"] = rows["loglik"] - rows["loglik"].shift(-1)
  return rows

# Read in the data ##################################################
crops = pd.read_csv("workshops/crops.csv")
bulbs = pd.read_csv("workshops/bulb_lifetimes.csv")
masks = pd.read_csv("workshops/masks.csv")
batteries = pd.read_csv("workshops/batteries.csv")
drones = pd.read_csv("workshops/drones.csv")
capacitors = pd.read_csv("workshops/workshop9_capacitors.csv")
pumps = pd.read_csv("workshops/pumps.csv")
fans = pd.read_csv("workshops/fans.csv")
valves = pd.read_csv("workshops/valves.csv")

# Fit all four, one data set at a time ###############################
sets = {
  "crops": compare(crops["days"]),
  "bulb lifetimes": compare(bulbs["days"]),
  "masks, left earloop": compare(masks["left_earloop"]),
  "masks, fabric": compare(masks["fabric"]),
  "alkaline batteries": compare(batteries.query("battery_type == 'alkaline'")["life_hours"]),
  "lithium batteries": compare(batteries.query("battery_type == 'lithium'")["life_hours"]),
  "drones": compare(drones["flight_time"]),
  # 50 on test, 25 failed, test stopped at the last failure
  "capacitors": compare(capacitors["t"], n_total = 50, tmax = capacitors["t"].max()),
  "pumps": compare(pumps["hours"]),
  "fans": compare(fans["hours"]),
  "valves": compare(valves["hours"]),
}

# Print the four log-likelihoods per data set, best first
results = pd.concat(sets, names = ["data"]).reset_index(level = 0)
summary = results.groupby("data", sort = False).apply(lambda g: pd.Series({
  "best": g["dist"].iloc[0],
  "gap": round(g["gap"].iloc[0], 1),
  "verdict": "clear win" if g["gap"].iloc[0] >= 2 else "tie: prefer the simpler model",
  "loglik": ", ".join(g["dist"] + " " + g["loglik"].round(1).astype(str)),
}))
print(summary.to_string())
