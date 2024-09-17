#' @name workshop_5
#' @author Tim Fraser

# Let's demo some statistical process control!

library(dplyr)
library(readr)
library(ggplot2)
#install.packages("ggpubr")
library(ggpubr)

# Read in our data
water = read_csv("workshops/onsen.csv")

# Let’s measure the range of each subgroup, and make a nice rounded label
stat = water %>%
  group_by(time) %>%
  summarize(r = temp %>% range() %>% diff() %>% abs(),
            label = round(r, 2)) 

# Suppose we calculated an upper and lower specification limit, which were 11 and 3
# for simplicity, I’m just writing these in so we can demo the geom_hline function in ggplot()
line = stat %>%
  summarize(upper = 11, lower = 3)

# We can add horizontal lines too!
ggplot() +
  geom_hline(data = line, mapping = aes(yintercept = upper), linetype = "dashed") +
  geom_hline(data = line, mapping = aes(yintercept = lower), linetype = "dashed") +
  geom_line(data = stat, mapping = aes(x = time, y = r)) +
  geom_point(data = stat, mapping = aes(x = time, y = r),
             size = 5, shape = 21, fill = "white", color = "black") +
  #geom_text(data = stat, mapping = aes(x = time, y = r + 0.5, label = label))
  geom_label(data = stat, mapping = aes(x = time, y = r, label = label)) 
  
  
# Or, we can visualize the whole process in g1 and g2
g1 = ggplot() +
  # geom_point(data = water, mapping = aes(x = time, y = temp))
  geom_jitter(data = water, mapping = aes(x = time, y = temp),
              width = 0.25)

g2 = ggplot() +
  geom_histogram(data = water, mapping = aes(x = temp)) +
  coord_flip() +
  labs(x = NULL)

# Combine them!
ggarrange(g1, g2)
2


# Let’s calculate sigma_s and sigma_t!
water %>%
  group_by(time) %>%
  summarize(xbar = mean(temp),
            r = max(temp) - min(temp),
            sd = sd(temp),
            nw = n(),
            df = nw - 1) %>%
  # How to get sigma-short!
  #   we're trying to pool the standard deviation from all these different subgroups
  #   to approximate the average standard deviation
  ungroup() %>%
  mutate(
    sigma_s = sqrt(sum(df * sd^2) / sum(df) ),
  #    sigma_s = sqrt(mean(sd^2))
    sigma_t = sd(water$temp),
    se = sigma_s / sqrt(nw),
    upper = mean(xbar) + 3*se,
    lower = mean(xbar) - 3*se
    )


# How do we approximate sigma-short?
dn = function(n = 12, reps = 1e4){
    # For 10,0000 reps
  tibble(rep = 1:reps) %>%
    # For each rep,
    group_by(rep) %>%
    # Simulate the ranges of n values
    summarize(r = rnorm(n = n, mean = 0, sd = 1) %>% range() %>% diff() %>% abs()) %>%
    ungroup() %>%
    # And calculate...
    summarize(
      # Mean range
      d2 = mean(r),
      # standard deviation of ranges
      d3 = sd(r),
      # and constants for obtaining lower and upper ci for rbar
      D3 = 1 - 3*(d3/d2), # sometimes written D3
      D4 = 1 + 3*(d3/d2), # sometimes written D4
      # Sometimes D3 goes negative; we need to bound it at zero
      D3 = if_else(D3 < 0, true = 0, false = D3) ) %>%
    return()
}


dn(n = 12)


#Let's write a function bn() to calculate our B3 and B4 statistics for any subgroup size n
bn = function(n, reps = 1e4){
  tibble(rep = 1:reps) %>%
    group_by(rep) %>%
    summarize(s = rnorm(n, mean = 0, sd = 1) %>% sd()) %>%
    summarize(b2 = mean(s), 
              b3 = sd(s),
              C4 = b2, # this is sometimes called C4
              A3 = 3 / (b2 * sqrt( n  )),
              B3 = 1 - 3 * b3/b2,
              B4 = 1 + 3 * b3/b2,
              # bound B3 at 0, since we can't have a standard deviation below 0
              B3 = if_else(B3 < 0, true = 0, false = B3)) %>%
  return()
}

# For a subgroup of size 12
stat = bn(n = 12)
# Statistic of interest
sbar = 2.5 
# Lower Control Limit
sbar * stat$B3
# Upper control limit
sbar * stat$B4

