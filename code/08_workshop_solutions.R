#' @name workshop_8
#' @title Maximum Likelihood Estimation in R
#' @author Tim Fraser, PhD

# Load packages
library(dplyr)
library(readr)
library(ggplot2)

# Load data.frame of crops by time to failure metric `days`
crops = read_csv("workshops/crops.csv")
# View empirical distribution of days
crops$days %>% hist()
# Calculate (empirically) lambda
mylambda = 1 / mean(crops$days)
mylambda

# PROBLEM: What if we can't calculate our parameters empirically? 
# Applicable when multiple parameters, parameters are interdependent, trick distributions, etc. 
# We need some other way to estimate our parameters.
# Maximum Likelihood Estimation! (MLE)

# 1 parameter = labmda 
# lambda = 1 / mean(t)
# Failure Function CDF F(t)
f = function(t, lambda){ 1 - exp(-1*t*lambda) }

# PDF function  f(t)
d = function(t, lambda){lambda * exp(-t*lambda) }

# Let's look at our first 3 observations
crops$days[1:3]
# This is the probability of a lifespan of 72, given this particular lambda value
d(t = 72, lambda = mylambda)
# This is the JOINT probability of a lifespan of 72 AND another lifespan of 119, given this particular lambda value
d(t = 72, lambda = mylambda) * d(t = 119, lambda = mylambda)

# This is the JOINT probability of ALL these lifespans, given this lambda value
# prod() is product
# JOINT probability also called LIKELIHOOD
d(t = crops$days, lambda = 0.014) %>% prod()

# But tiny decimals are hard for R to compute. So we often want to log them.
d(t = crops$days, lambda = 0.014) %>% prod() %>% log()
# Excitingly the log of the product of probabilities is equal to the sum of logged probabilities
d(t = crops$days, lambda = 0.014) %>% log() %>% sum()
# So we often find ourselves calculating:
# **log-likelihood**


# Calculate Log-Likelihood, by summing the log
ll = function(t, lambda){
  d(t = t, lambda) %>% log() %>% sum()
}
# Suppose lambda is 0.014.
# Then the log likelihood of this observed data t is...
# aka the probability of getting all of these values simultaneously in one sample...
ll(t = crops$days, lambda = 0.014)



# Let's hack this manually!
# We're going to make a sequence of parameters from 0.00001 to 1
# and get the log likelihood of the crops$days vector given each of these parameters.
manyll = tibble(parameter = seq(from = 0.00001, to = 1, by = 0.001)) %>%
  # For each of these parameters
  group_by(parameter) %>%
  # Calculate a different loglik statistic
  summarize(loglik = ll(t = crops$days, lambda = parameter))

# Check it out! Some parameters are more or less likely.
manyll %>% head(3)

# Let's find the maximum loglikelihood!
# That loglikelihood will pair with the parameter that is therefore MOST likely to match this observed distribution.
output <- manyll %>%
  filter(loglik == max(loglik))

output
# PRETTY DARN CLOSE TO OUR ORIGINAL LAMBDA!!!!! HOLY SMOKES!
mylambda



# We can visualize this process like so!
ggplot() +
  geom_line(data = manyll, mapping = aes(x = parameter, y = loglik), color = "steelblue") +
  geom_vline(xintercept = output$parameter, linetype = "dashed")  +
  theme_classic(base_size = 14) +
  labs(x = "parameter (lambda)", y = "loglik (Log-Likelihood)",
       subtitle = "Maximizing the Log-Likelihood (Visually)") +
  # We can actually adust the x-axis to work better with log-scales here
  scale_x_log10() +
  # We can also annnotate our visuals like so.
  annotate("text", x = 0.1, y = -2000, label = output$parameter)



# We did it manually, but how do we do it automatically?

# We use an OPTIMIZER, with the optim() function.
# It uses gradient descent to ascend/descend the curve/plane we visualized above.

# Optimize and collect the quantities of interest
q = optim(par = c(0.01), t = crops$days, fn = ll, 
          # -1 means MAXIMIZE; 1 means MINIMIZE
          control = list(fnscale = -1))

q = optim(fn = ll, par = c(0.01), t = crops$days, control = list(fnscale = -1))

# q is a list object. We've learned several types of objects
data.frame()
tibble()
c()
# Here's a list example
mylist = list(df = tibble(1:10),
              par = 0.234)
# You can query the par vector in the list like this. 
mylist$par

q
# Once we have our optimized parameters, we can pipe it into functions like this!
f(t = 1:100, lambda = q$par)


# We could also write MULTI-PARAMETER loglikelihood functions!
ll = function(t, par){
  dunif(t, min = par[1], max = par[2]) %>% log() %>% sum()
}

# Let's try it!
optim(fn = ll, par = c(5, 150), 
      t = crops$days, control = list(fnscale = -1))
# It hates the uniform! Booo!!!

# What about other distributions?

# Let's write a new function
ll = function(t, par){
  # Our parameters input is now going to be vector of 2 values
  # par[1] gives the first value, the mean
  # par[2] gives the second value, the standard deviation
  dnorm(t, mean = par[1], sd = par[2]) %>% log() %>% sum()
}
# Let's try it out!
optim(par = c(0, 1), t = crops$days, fn = ll, control = list(fnscale = -1))
dnorm(crops$days, mean = 0, sd = 1)
dnorm(crops$days, mean = 0, sd = 1) %>% log() %>% sum()

crops$days

q2 = optim(par = c(90, 15), t = crops$days, fn = ll, control = list(fnscale = -1))
q2$par


pnorm(1:10, mean = q2$par[1], sd = q2$par[2])

# Let's try a weibull!
pweibull(q = 1, shape = 2, scale = 1)


llweibull = function(t, par){
  dweibull(t, shape = par[1], scale = par[2]) %>% log() %>% sum()
}

q3 = optim(par = c(1, 1000), fn = llweibull, t = crops$days, control = list(fnscale = -1))

q3$par

# You might want to hang on to this
# Chunk of helper code
# control = list(fnscale = -1)
# d = function(t,lambda){ lambda * exp(-1*t *lambda)    }

# All done!

