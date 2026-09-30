# ZZ_financial_analysis.py
# Tim Fraser
# Extra: financial impact analysis of a process improvement
# Chapter: Indices and Confidence Intervals for Statistical Process Control in Python

# A script to help you do financial impact analysis!
# It mirrors ZZ_financial_analysis.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Load packages!
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)

# NOTE: the R version calls get_stat_s() from functions_process_control.R.
# functions/functions_process_control.py has the same get_stat_s(), but it is
# slow enough that 4,000 bootstrap calls take minutes. So ggxbar2() below
# writes out the same subgroup statistics in a few lean lines (it gives
# identical control limits), and the group-by bootstrap is fully vectorized.


# Get my data
data = pd.read_csv("workshops/onsen.csv")
cost = 50 # cost of refund per visit that is too cold

data.info()  # glimpse() in R


# Create some function that will perform an analysis and return a data.frame....

def ggxbar2(x, y, xlab="Time (Subgroups)", ylab="Average"):
    """
    Modified Average Control Chart
    x: vector of subgroup values (usually time). Must be same length as `y`.
    y: vector of metric values (eg. performance). Must be same length as `x`.
    Same statistics as get_stat_s() in functions_process_control.py
    """
    # Testing values
    # water = pd.read_csv("workshops/onsen.csv")
    # x = water["time"]; y = water["temp"]; xlab = "Time (Subgroups)"; ylab = "Average"
    data = pd.DataFrame({"x": np.asarray(x), "y": np.asarray(y)})

    # Get statistics for each subgroup
    stat_s = (data.groupby("x", as_index=False)
              .agg(xbar=("y", "mean"), s=("y", "std"), nw=("y", "count")))
    stat_s["df"] = stat_s["nw"] - 1
    # grand mean, pooled within-group sigma_s, and standard error per subgroup
    stat_s["xbbar"] = stat_s["xbar"].mean()
    stat_s["sigma_s"] = np.sqrt((stat_s["df"] * stat_s["s"]**2).sum() / stat_s["df"].sum())
    stat_s["se"] = stat_s["sigma_s"] / np.sqrt(stat_s["nw"])
    stat_s["upper"] = stat_s["xbbar"] + 3 * stat_s["se"]
    stat_s["lower"] = stat_s["xbbar"] - 3 * stat_s["se"]

    return stat_s

# STEP 2: Write a jumbo function f that calculates an n-failures statistic
# or some single statistic of interest for your dataset

# averages plot of temperature, focusing on lower control limit
def f(data):
    stat = ggxbar2(x=data["time"], y=data["temp"], xlab="Stuff", ylab="More Stuff")[["x", "lower"]]

    # If they are all the same...
    # lcl = stat["lower"].iloc[0]
    # match each row to its subgroup's lower limit (left_join in R)
    lower = data["time"].map(stat.set_index("x")["lower"])
    fail = data["temp"] < lower
    result = pd.DataFrame({"n_fail": [fail.sum()]})

    return result

# STEP 3: Test it! Does bootstrapping (sampling with replacement) change it?
print(f(data))
print(f(data.sample(n=len(data), replace=True)))

# STEP 4: ITERATE WITH for-loop

# STEP 4A: for-loop version
holder = []
for i in range(1, 1001):
    data_i = f(data.sample(n=len(data), replace=True))
    holder.append(data_i)
holder = pd.concat(holder, ignore_index=True)
boot = holder

# STEP 4B: ITERATE WITH groupby
# Alternatively, stack 1000 copies of the data with a rep id,
# resample within each rep, and let groupby do f() for every rep at once.

# f(), vectorized over reps: same steps, grouped by rep (and rep + time)
def f_reps(boot):
    stat = (boot.groupby(["rep", "time"], as_index=False)
            .agg(xbar=("temp", "mean"), s=("temp", "std"), nw=("temp", "count")))
    stat["df"] = stat["nw"] - 1
    stat["ss"] = stat["df"] * stat["s"]**2
    # per rep: grand mean and pooled sigma_s
    stat["xbbar"] = stat.groupby("rep")["xbar"].transform("mean")
    stat["sigma_s"] = np.sqrt(stat.groupby("rep")["ss"].transform("sum") /
                              stat.groupby("rep")["df"].transform("sum"))
    stat["lower"] = stat["xbbar"] - 3 * stat["sigma_s"] / np.sqrt(stat["nw"])
    boot = boot.merge(stat[["rep", "time", "lower"]], on=["rep", "time"], how="left")
    boot["fail"] = boot["temp"] < boot["lower"]
    return boot.groupby("rep", as_index=False).agg(n_fail=("fail", "sum"))

boot = (pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True)
        .groupby("rep")
        .sample(frac=1, replace=True))
boot = f_reps(boot[["rep", "time", "temp"]])

# STEP 5: COST & CONFIDENCE INTERVALS
# Calculate cost and uncertainty
total_cost = boot["n_fail"] * cost
print(pd.DataFrame({
    "estimate": [total_cost.quantile(0.50)],
    "se": [total_cost.std()],
    "lower": [total_cost.quantile(0.025)],
    "upper": [total_cost.quantile(0.975)]}))


# STEP 6: FUNCTIONIFY IT!
# Write a qi() function to return your quantities of interest
# any time your input dataframe data changes!
def qi(data):

    # Alternatively, stack copies with a rep id and use groupby
    boot = (pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True)
            .groupby("rep")
            .sample(frac=1, replace=True))
    boot = f_reps(boot[["rep", "time", "temp"]])

    # Calculate cost and uncertainty
    total_cost = boot["n_fail"] * cost
    df = pd.DataFrame({
        "estimate": [total_cost.quantile(0.50)],
        "se": [total_cost.std()],
        "lower": [total_cost.quantile(0.025)],
        "upper": [total_cost.quantile(0.975)]})

    return df


# STEP 7: COMPARE SCENARIOS!

# Baseline scenario
s1 = qi(data)

# Suppose you made a specific change to the system
s2 = data.copy()
# eg. you modify the ph, driving up the temperature
s2["temp"] = np.where(s2["ph"] > 6, s2["temp"] * 1.6, s2["temp"])
# Recompute the cost.
s2 = qi(s2)

# Compare the result!
print(pd.concat([s1, s2], ignore_index=True))
