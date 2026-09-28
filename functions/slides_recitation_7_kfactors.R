# Recitation 7 -- k-factor tables and every worked example, recomputed.
# Run from the top of the repo:  source("functions/slides_recitation_7_kfactors.R")
library(dplyr)
library(tidyr)
source("functions/functions_k.R")

# Confidence levels (columns of Tables 3 and 4)
ci = c(0.60, 0.80, 0.90, 0.95, 0.975, 0.99, 0.999)
rs = 1:41

# Table 3: one-sided UPPER k-factors, time-censored rule (chi-square, 2(r+1) df)
table3 = expand.grid(r = rs, ci = ci) %>%
  mutate(k = mapply(function(r, p) qk(p = p, r = r, .time = TRUE), r, ci)) %>%
  mutate(k = round(k, 2), ci = paste0(ci * 100, "%")) %>%
  pivot_wider(names_from = ci, values_from = k)
# Table 4: one-sided LOWER k-factors (chi-square, 2r df)
table4 = expand.grid(r = rs, ci = 1 - ci) %>%
  mutate(k = mapply(function(r, p) qk(p = p, r = r), r, ci)) %>%
  mutate(k = round(k, 2), ci = paste0(round((1 - ci) * 100, 1), "%")) %>%
  pivot_wider(names_from = ci, values_from = k)
# Table 2 rules, and zero-failure factors (Table 3.7: -ln(alpha))
zero = data.frame(percentile = c(50, 60, 80, 90, 95, 97.5, 99)) %>%
  mutate(k0 = round(-log(1 - percentile / 100), 4))
write.csv(table3, "workshops/recitation7_k_upper.csv", row.names = FALSE)
write.csv(table4, "workshops/recitation7_k_lower.csv", row.names = FALSE)
write.csv(zero, "workshops/recitation7_zero_failure.csv", row.names = FALSE)

# ---- Worked examples -------------------------------------------------------
cat("Ex1 r=20 time, 2-sided 95%, lambda-hat=0.002\n")
k1 = qk(c(0.025, 0.975), r = 20, .time = TRUE); print(round(k1, 4)); print(round(k1 * 0.002, 6))
cat("Ex2 r=20 time, upper 95%\n")
k2 = qk(0.95, r = 20, .time = TRUE); print(round(k2, 4)); print(round(k2 * 0.002, 6))
cat("Ex3 r=15 failure-censored, upper 95%, lambda-hat=0.004\n")
k3_tab = qchisq(0.95, 2 * 15) / (2 * 14); k3 = k3_tab * 14 / 15
print(round(c(table = k3_tab, adjusted = k3, qk = qk(0.95, r = 15, .failure = TRUE)), 4)); print(round(k3 * 0.004, 6))
cat("Ex4 r=15 failure-censored, two-sided 95%\n")
k4 = c(qk(0.025, r = 15, .failure = TRUE), qk(0.975, r = 15, .failure = TRUE)); print(round(k4, 4)); print(round(k4 * 0.004, 6))
cat("Ex1-4 slide values: table-lookup 1.68 x 14/15 =", round(1.68 * 14 / 15, 4), "\n")
cat("Exercise 1 r=13 failure, upper 80%, 0.0015\n"); e1 = qk(0.80, r = 13, .failure = TRUE); print(round(c(e1, e1 * 0.0015), 6))
cat("Exercise 2 r=25 time, 90% 2-sided, 0.01\n"); e2 = qk(c(0.05, 0.95), r = 25, .time = TRUE); print(round(c(e2, e2 * 0.01), 6))
cat("Exercise 3 r=3, 200 FITs, 95% 2-sided; Type I then Type II\n")
e3a = qk(c(0.025, 0.975), r = 3, .time = TRUE); print(round(c(e3a, e3a * 200), 2))
e3b = qk(c(0.025, 0.975), r = 3, .failure = TRUE); print(round(c(e3b, e3b * 200), 2))
cat("Ex5 zero failures\n")
nT = 200 * 5000 + 200 * 3000; print(nT)
print(round(-log(c(0.5, 0.05, 0.30)) / nT * 1e9, 1))
cat("Ex6 min n: 5 failures, T=5000, 90%, lambda_obj = 1/500000\n")
k6 = qk(0.90, r = 5, .time = TRUE); print(round(k6, 3)); print(5 * k6 / (5000 * 2e-6))
print(round(5 * qk(0.90, r = 5) / (5000 * 2e-6), 2)); print(round(qk(0.90, r = 5, .time = TRUE) / 5 * 5, 3))
cat("Ex7 min test time: n=100, r=10, 95%, MTTF 20000\n")
for (rr in c(10, 11)) { k = qk(0.95, r = rr, .time = TRUE); cat(rr, round(k, 3), round(10 * k / (100 * 5e-5), 1), "\n") }
k7 = qk(0.95, r = 10, .time = TRUE); print(round(10 * k7 / (100 * 5e-5)))
cat("Ex8 max failures: n=50, T=2000, 80%, lambda_obj=5e-5\n")
tab8 = sapply(1:4, function(r) r * qk(0.80, r = r, .time = TRUE)); print(round(tab8, 3))
tab8b = sapply(1:4, function(r) r * qk(0.80, r = r)); print(round(tab8b, 3)); cat("target r*k =", 5e-5 * 50 * 2000, "\n")
cat("Ex9 n zero failures\n"); print(-log(0.10) * 40000 / 8000)
cat("Ex10 T zero failures\n"); print(-log(0.20) / (10000 * 10e-9))
