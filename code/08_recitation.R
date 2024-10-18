#' @name 08_recitation
#' @title Maximum Likelihood Estimation in R [part 2]
#' @author Tim Fraser, PhD
#' @description Multi-Parameter MLE 


# Using optim() for MLE with 1 parameter ##############################################

# Load packages
library(dplyr)
library(readr)
library(ggplot2)

# Load data.frame of crops by time to failure metric `days`
crops = read_csv("workshops/crops.csv")


# Failure Function CDF F(t)
f = function(t, lambda){ 1 - exp(-1*t*lambda) }

# PDF function  f(t)
d = function(t, lambda){lambda * exp(-t*lambda) }

# Calculate Log-Likelihood, by summing the log
ll = function(t, lambda){
  d(t = t, lambda) %>% log() %>% sum()
}


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




# Using optim() for MLE with 2+ parameters ##############################################


# Load packages
library(dplyr)
library(readr)
library(ggplot2)

# Load data.frame of crops by time to failure metric `days`
crops = read_csv("workshops/crops.csv")



## uniform ##############################################################

# We could also write MULTI-PARAMETER loglikelihood functions!
ll = function(t, par){
  dunif(t, min = par[1], max = par[2]) %>% log() %>% sum()
}

crops$days %>% range()
# Let's try it!
optim(fn = ll, par = c(4, 197), 
      t = crops$days, control = list(fnscale = -1))




## normal ##############################################################

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
# Why doesn't it work?

# Well, we're giving it super weird starting parameters. (0,1)
# What densities would they produce?
dnorm(crops$days, mean = 0, sd = 1)
# What loglikelihood would they produce?
dnorm(crops$days, mean = 0, sd = 1) %>% log() %>% sum()

# Let's look at our real values...
crops$days


# What if we picked more representative starting parameters?
q2 = optim(par = c(90, 15), t = crops$days, fn = ll, control = list(fnscale = -1))
q2$par
# Yay! It works!


pnorm(1:10, mean = q2$par[1], sd = q2$par[2])



## weibull ##############################################################


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



## fitdistr ###########################################################

# Feeling accomplished, but like this should be easier?
# That's what the fitdistr function does.

MASS::fitdistr(x = crops$days, densfun = "normal")
MASS::fitdistr(x = crops$days, densfun = "exponential")
MASS::fitdistr(x = crops$days, densfun = "weibull")


# Interested? Learn more here!
# https://timothyfraser.com/sigma/appendix-using-fitdistr-to-fitting-distribution-parameters.html



