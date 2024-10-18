#' @name 08_lesson
#' @title Maximum Likelihood Estimation in R
#' @author Tim Fraser, PhD
#' @description Single Parameter MLE 

# Load packages
library(dplyr)
library(readr)
library(ggplot2)

# Load data.frame of crops by time to failure metric `days`
crops = read_csv("workshops/crops.csv")

crops

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
d(t = 72, lambda = 0.014359)
d(t = 72, lambda = 0.015)







# This is the JOINT probability of a lifespan of 72 
# AND another lifespan of 119, given this particular lambda value
d(t = 72, lambda = mylambda) * d(t = 119, lambda = mylambda)










# This is the JOINT probability of ALL these lifespans, given this lambda value
# prod() is product
# JOINT probability also called LIKELIHOOD
d(t = crops$days, lambda = 0.014) %>% prod()










# But tiny decimals are hard for R to compute. So we often want to log them.
d(t = crops$days, lambda = 0.014) %>% prod() %>% log()












# Excitingly the log of the product of probabilities
# is equal to the sum of logged probabilities
d(t = crops$days, lambda = 0.014) %>% log() %>% sum()
d(t = crops$days, lambda = 0.014) %>% prod() %>% log()







# So we often find ourselves calculating:
# **log-likelihood**





# Calculate Log-Likelihood, by summing the log
ll = function(t, lambda){
  d(t = t, lambda) %>% log() %>% sum()
}







# Suppose lambda is 0.014.
# Then the log likelihood of this observed data t is...
# aka the probability of getting all 
# of these values simultaneously in one sample...
ll(t = crops$days, lambda = 0.014)




tibble(lambda = seq(from = 0.00001, to = 1, by = 0.001)) %>%
  group_by(lambda) %>%
  summarize(loglik = ll(t = crops$days, lambda = lambda)) %>%
  plot()




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



