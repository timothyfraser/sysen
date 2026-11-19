# slides_workshop_9_planning.R ----------------------------------------------
#
# Feeds: Workshop 9 slide "Planning a Life Test: when it is not exponential",
# the Exponential and Weibull tabs. Fits the chips data (200 chips on test,
# stopped at 1500 hours), then plans a 250-hour test allowing 5 failures at
# 90% confidence. Run from the sigma repo root:
#   Rscript functions/slides_workshop_9_planning.R
# Prints the numbers the slide shows; writes nothing.

library(dplyr)
library(readr)
source("functions/functions_mle.R")
source("functions/functions_planning.R")

chips = read_csv("workshops/chips.csv", show_col_types = FALSE)

# 1. Fit each family to the chips -------------------------------------------
fit_exp = get_mle(data = chips, n_total = 200, tmax = 1500, dist = "exponential")
fit_wei = get_mle(data = chips, n_total = 200, tmax = 1500, dist = "weibull")
print(fit_exp)
print(fit_wei)

lambda = fit_exp$lambda
m_fit = fit_wei$m
c_fit = fit_wei$c

# 2. Exponential plan: one number, no shape to assume ------------------------
p_exp = plan_test("exponential", t = 250, r = 5, ci = 0.90, lambda = lambda)
cat("\nExponential plan: lambda =", signif(lambda, 4), " n_up =", p_exp$n_up, "\n")

# 3. Weibull plan: the shape must be assumed, so try a grid around the fit ---
grid = round(c(m_fit - 0.5, m_fit - 0.25, m_fit, m_fit + 0.25, m_fit + 0.5), 2)
p_wei = bind_rows(lapply(grid, function(m){
  plan_test("weibull", t = 250, r = 5, ci = 0.90, c = c_fit, m = m)
}))
cat("Weibull plan: c =", signif(c_fit, 4), " fitted m =", round(m_fit, 2), "\n")
print(as.data.frame(p_wei %>% select(m, c, n_up)))
