#’ @name workshop_9_solutions.R
#’ @author Tim Fraser, PhD
#’ @note pairs with: https://timothyfraser.com/sigma/workshop-fault-tree-analysis-in-r.html 

library(dplyr)
library(ggplot2)
library(readr)

# PART 1: Using Raw Probabilities #################################
f1 = function(m, c, d, k){
  top = m + c * d * k 
  return(top)
}
# For example... given these probabilities, the chance Superman turns evil is highly contigent on event m - the success of superman movies at the box office.
probs1 = f1(m = 0.50, c = 0.99, d = 0.25, k = 0.01)
# view it!
probs1 


# PART 2: Using Failure Rates at Time t ############################

# But if we knew the failure rate of each event, 
# we could calculate the probability of the top event at any time t!


f2 = function(t, lambda_m, lambda_c, lambda_d, lambda_k){
  # Get probability at time t...
  prob_m = pexp(t, rate = lambda_m)
  prob_c = pexp(t, rate = lambda_c)
  prob_d = pexp(t, rate = lambda_d)
  prob_k = pexp(t, rate = lambda_k)
  # Use boolean equation to calculate top event
  prob_top = prob_m + (prob_c * prob_d * prob_k)
  return(prob_top)
}

# Then we could simulate the probability of the top event over time!
probs2 = tibble(t = 1:100) %>%
  mutate(prob = f2(t = t, lambda_m = 0.01, lambda_c = 0.001, 
                   lambda_d = 0.025, lambda_k = 0.00005))
# Check out the first few rows!
probs2 %>% head(3)


# PART 3: Simulating Uncertainty in Probabilities ###################
probs3 = tibble(
  n = 1000,
  prob_m = rbinom(n = n, size = 1, prob = 0.50),
  prob_c = rbinom(n = n, size = 1, prob = 0.99),
  prob_d = rbinom(n = n, size = 1, prob = 0.25),
  prob_k = rbinom(n = n, size = 1, prob = 0.01),
  # Calculate probability of top event for each simulation  
  prob_top = f1(m = prob_m, c = prob_c, d = prob_d, k = prob_k)
)
# Let's get some descriptive statistics - 
# the average will be particularly informative
probs3 %>% 
  summarize(
    mu_top = mean(prob_top),
    sigma_top = sd(prob_top))



# PART 4: Simulating Uncertainty in Failure Rates ##############################
# Suppose each failure rate has a specific standard error:
# for m, 0.0001; for c, 0.00001, for d and k, 0.000002.


f4 = function(t, lambda_m, lambda_c, lambda_d, lambda_k){
  sim_lambda_m = rnorm(n = 1, mean = lambda_m, sd = 0.0001)
  sim_lambda_c = rnorm(n = 1, mean = lambda_c, sd = 0.00001)
  sim_lambda_d = rnorm(n = 1, mean = lambda_d, sd = 0.000002)
  sim_lambda_k = rnorm(n = 1, mean = lambda_k, sd = 0.000002)
  
  # Get probability at time t...
  sim_prob_m = pexp(t, rate = sim_lambda_m)
  sim_prob_c = pexp(t, rate = sim_lambda_c)
  sim_prob_d = pexp(t, rate = sim_lambda_d)
  sim_prob_k = pexp(t, rate = sim_lambda_k)
  # Use boolean equation to calculate top event
  prob_top = sim_prob_m + (sim_prob_c * sim_prob_d * sim_prob_k)
  return(prob_top)
}

# Then we could simulate the probability of the top event over time,
probs4 = tibble(t = 1:100) %>%
  # This would give us 1 random simulation per time period  
  mutate(prob = f4(t = 1:100, lambda_m = 0.01, lambda_c = 0.001, 
                   lambda_d = 0.025, lambda_k = 0.00005))


# But we really probably want MANY random simulations per time period.
probs5 = tibble(reps = 1:1000) %>%
  group_by(reps) %>%
  # We can use `reframe()`, a version of summarize()
  # used when you want to return MANY rows per group
  reframe(
    t = 1:100,
    prob = f4(t = t, lambda_m = 0.01, lambda_c = 0.001, 
              lambda_d = 0.025, lambda_k = 0.00005))

probs5 %>% head(3)


# And then we could get quantities of interest for each time period!
probs6 = probs5 %>%
  group_by(t) %>%
  summarize(
    mu = mean(prob), 
    sigma = sd(prob),
    # Exact lower and upper 95% simulated confidence intervals
    lower = quantile(prob, probs = 0.025),
    upper = quantile(prob, probs = 0.975),
    # Approximated lower and upper 95% confidence intervals
    lower_approx = mu - qnorm(0.025) * sigma,
    upper_approx = mu + qnorm(0.975) * sigma)

probs6 %>% head(3)



