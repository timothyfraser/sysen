# slides_factorial_replicates.py --------------------------------------------
# Python twin of slides_factorial_replicates.R (standard error of an effect,
#   BHH pilot plant 2^3 with two yields per run, BHH Table 5.3).
# Run from the top of the repo:  python3 functions/slides_factorial_replicates.py
# Reads:  workshops/pilot_plant_replicates.csv (run, t, c, k, y1, y2)
# Writes: nothing; prints d, d^2/2, s^2, Var(effect) and SE(effect).
import pandas as pd

reps = pd.read_csv("workshops/pilot_plant_replicates.csv")

# Each run's two yields give a 1-df variance estimate: s_i^2 = d^2 / 2
reps = reps.assign(ybar=(reps.y1 + reps.y2) / 2, d=reps.y1 - reps.y2)
reps["d2_half"] = reps.d ** 2 / 2
print(reps.to_string(index=False))

# Pool the eight estimates; an effect is a difference of two means of 8 runs
s2 = reps.d2_half.sum() / len(reps)
var_effect = (1 / 8 + 1 / 8) * s2
se_effect = round(var_effect ** 0.5, 2)
print(pd.DataFrame({"s2": [s2], "var_effect": [var_effect], "se_effect": [se_effect]}).to_string(index=False))
