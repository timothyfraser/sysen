# 00_p_charts.R
# Tim Fraser
# Extra: fraction-defective (p) charts - the short version of 00_attribute_charts.R
# Chapter: Statistical Process Control in R

library(dplyr)

# Fraction defection (p) chart
# # of defective items
# has a binomial distribution
# each of the n itmes being tests is being classified
# into 2 categories: defective or not defective
# the probability p of a defective item is constant for every item.

# If X represents the # of defective items in n items,
# then the probability of finding x defective in n items is:
data = tibble(
  t = seq(from = 1, to = 1000, by = 1),
  t2 =  floor(t / 10)+1,
  n = rpois(n = 1000, lambda = 100),
  x = rpois(n = 1000, lambda = 5),
  p = x / n
)


p = function(x,n,p){factorial(n) / (factorial(x)*factorial(n - x)) * p^(x)*(1 - p)^(n-x) }


# data %>%
#   summarize(prob_p = sum(x) / n())

# data %>%
#   mutate(prob_p = sum(x) / n()) %>%
#   summarize(prob = p(x = 1, n = n(), p = prob_p[1]))

p(x = 5, n = 150, p = 0.50)

data %>%
  group_by(t2) %>%
  summarize(
    n = sum(n),
    x = sum(x),
    p = x / n)
stat_s = data %>%
  group_by(t) %>%
  summarize(
    prob = p(x = x, n = n, p = p),
    mu = n * p,
    sigma = sqrt(n*p*(1-p))
  )

stat_t = data %>%
  summarize(
    xsum = sum(x),
    nsum = sum(n),
    pbar = xsum / nsum,
    se = sqrt(pbar * (1 - pbar) / nsum),
    lower = pbar - 3*se,
    upper = pbar + 3*se
  )

library(ggplot2)
ggplot() +
  geom_line(data = stat_s, mapping = aes(x = t, y = mu)) +
  geom_point(data = stat_s, mapping = aes(x = t, y = mu))

