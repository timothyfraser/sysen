# Recitation 9 (Fault Tree Analysis) slide code, run from the repo root.
# Every chunk here is shown on a slide in docs-v3/slides/23_slides_recitation_9.html.
library(dplyr)

# -- Slide: the tree as data ---------------------------------------------------
edges = tibble(from = c("T", "G1", "G1", "G2", "G2", "G3", "G3"),
               to   = c("G1", "G2", "G3", "1", "2", "1", "3"))
print(edges)

# -- Slide: data to Mermaid text -----------------------------------------------
cat(paste(edges$from, "---", edges$to), sep = "\n")

# -- Slide: the z multiplier ---------------------------------------------------
ci = 0.95
z = qnorm(1 - (1 - ci) / 2, mean = 0, sd = 1)
print(round(z, 2))

# -- Slide: z table values (rendered as an HTML table) --------------------------
zs = c(1.28, 1.645, 1.96, 2.33, 2.58)
print(tibble(z = zs, phi = round(pnorm(zs), 4)))

# -- Slide: simulate uncertain lambda --------------------------------------------
set.seed(1)
lambdas = rnorm(1000, mean = 0.001, sd = 0.0001)   # CV = 10%
simprobs = pexp(100, rate = lambdas)                # P(fail by t = 100)
mu = mean(simprobs)
sigma = sd(simprobs)
print(round(c(mu = mu, sigma = sigma), 4))

# -- Slide: confidence interval ---------------------------------------------------
n = length(simprobs)
ci_mean = mu + c(-1, 1) * qnorm(0.975) * sigma / sqrt(n)
print(round(ci_mean, 4))
