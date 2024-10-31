#' @name 10_lesson.R
#' @title Physical Acceleration Models
#' In this lesson, let's learn Weibull Acceleration modeling
#' and MLE for acceleration modeling!

# Packages
library(dplyr) # for data wrangling
library(broom) # for tidying model objects
library(ggplot2) # for visualization


# LINEAR REGRESSION FOR WEIBULL ACCELERATION MODELING ##############################


library(dplyr) # for data wrangling
library(broom) # for tidying model objects

# Let's make a data.frame matching Example 1 from the lesson slides
data = tibble(t = c(24, 72,168,300, 500, 750, 1000, 1250, 1500),
       r85 = c(1, 0, 0, 1, 0, 3, 0, 1, 2),
       r105 = c(2, 1, 3, 2, 2, 4, 5, 1, 4),
       r125 = c(5, 10, 13, 2, 3, 2, 2, 1, 0) )
n = 40

# Calculate probability of failure at time t under 85 degrees 
data = data %>%
  mutate(f85 = cumsum(r85) / n) %>%
  # Convert to this formula
  mutate(y85 = log(-log(1 - f85)))

m = data %>%  lm(formula = y85 ~ log(t) )

intercept = m$coefficients[1] # intercept
slope = m$coefficients[2] # slope

# These are our estimates for m and c at stress level 85
tibble(mhat =  slope,  chat = exp(-intercept/slope) )


# What!!!?

# Let's streamline this.

#' @param t [numeric] vector of times to failure. Same length as vector r.
#' @param r [integer] failures at time t. Same length as vector t.
#' @param n [integer] number of total units under test. Length 1.
graphical_estimates = function(t, r, n = 40){

  # Testing values
  # t = data$t; r = data$r85; n = 40
  
  # Make data.frame
  df = tibble(t = t, r = r, n = n)

  # Calculate probability of failure
  df = df %>% mutate(f = cumsum(r) / n)
  
  # Calculate transformation variable y
  df = df %>% mutate(y = log(-log(1 - f)))
  
  # Get model m
  m = df %>% lm(formula = y ~ log(t)) 
  
  # Get coefficiennts
  intercept = m$coefficients[1]
  slope = m$coefficients[2]
  
  # Calculate estimates for m and c
  output = tibble(mhat = slope, chat = exp(-intercept/slope))
  
  return(output)
}
  
# Let's try it!
graphical_estimates(t = data$t, r = data$r85, n = 40)

# Get parameters at different levels of stress
p85 = graphical_estimates(t = data$t, r = data$r85, n = 40)
p105 = graphical_estimates(t = data$t, r = data$r105, n = 40) 
p125 = graphical_estimates(t = data$t, r = data$r125, n = 40)

# We know c_u = AF x c_s,
# so AF = c_s / c_u

# AF from 85 to 105 degrees
p85$chat / p105$chat
# AF from 105 to 125 degrees
p105$chat / p125$chat
# AF from 85 to 125 degrees
p85$chat / p125$chat


# 85 C cell   m-hat = 0.57  c-hat 40222  Acceleration to 105 C = 18.2
# 105 C cell   m-hat = 0.70  c-hat 2208  Acceleration to 105 C = 9.1
# 125 C cell   m-hat = 0.71  c-hat 242  Acceleration to 105 C = 166.2


rm(list = ls())



# MLE WITH FIXED M FOR WEIBULL ACCELERATION MODELING #####################


library(dplyr) # for data wrangling
library(broom) # for tidying model objects

# Let's make a data.frame matching Example 1 from the lesson slides
data = tibble(t = c(24, 72,168,300, 500, 750, 1000, 1250, 1500),
              r85 = c(1, 0, 0, 1, 0, 3, 0, 1, 2),
              r105 = c(2, 1, 3, 2, 2, 4, 5, 1, 4),
              r125 = c(5, 10, 13, 2, 3, 2, 2, 1, 0) )
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
d = function(t, m, c){  (m / t) * (t / c)^m * exp(-1*(t/c)^m)  }
r = function(t, m, c){  exp(-(t/c)^m) }

# Let's write our crosstable's likelihood function
ll = function(t, x1, x2, x3, n1, n2, n3, par){
  # Get total failures
  r1 = sum(x1)  
  r2 = sum(x2)  
  r3 = sum(x3)  
  tmax = max(t) # Record last time step
  
  # Get product of log-densities at each time step, for all failures then
  prob_d1 = ((d(t, c = par[1], m = par[4]) %>% log()) * x1) %>% sum()
  prob_d2 = ((d(t, c = par[2], m = par[4]) %>% log()) * x2) %>% sum()
  prob_d3 = ((d(t, c = par[3], m = par[4]) %>% log()) * x3) %>% sum()
  
  # For last time step, get probability of each remaining unit surviving 
  prob_r1 = r(t = tmax, c = par[1], m = par[4])^(n1 - r1) %>% log()
  prob_r2 = r(t = tmax, c = par[2], m = par[4])^(n2 - r2) %>% log()
  prob_r3 = r(t = tmax, c = par[3], m = par[4])^(n3 - r3) %>% log()
  
  # Get joint log-likelihood, across ALL vectors
  prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3
}


# And let's run MLE!
mle = optim(
  par = c(1000, 1000, 1000, 1), 
  t = data$t,  
  x1 = data$r85,
  n1 = n85,  
  x2 = data$r105,  
  n2 = n105,
  x3 = data$r125,  
  n3 = n125,
  fn = ll,  
  control = list(fnscale = -1))


# Extract parameters into a dataframe
p = tibble(
  c85 = mle$par[1],
  c105 = mle$par[2],
  c125 = mle$par[3],
  m = mle$par[4])

# Acceleration Factor from 85 C to 105 C
p$c85 / p$c105
# Acceleration Factor from 105 to 125 C
p$c105 / p$c125
# Acceleration Factor from 85 to 125 C
p$c85 / p$c125


rm(list = ls())



# 3. MLE WITH VARYING M ################################################


library(dplyr) # for data wrangling
library(broom) # for tidying model objects

# Let's make a data.frame matching Example 1 from the lesson slides
data = tibble(t = c(24, 72,168,300, 500, 750, 1000, 1250, 1500),
              r85 = c(1, 0, 0, 1, 0, 3, 0, 1, 2),
              r105 = c(2, 1, 3, 2, 2, 4, 5, 1, 4),
              r125 = c(5, 10, 13, 2, 3, 2, 2, 1, 0) )
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
d = function(t, m, c){  (m / t) * (t / c)^m * exp(-1*(t/c)^m)  }
r = function(t, m, c){  exp(-(t/c)^m) }

# Let's write our crosstable's likelihood function
ll = function(t, x1, x2, x3, n1, n2, n3, par){
  # Get total failures
  r1 = sum(x1)  
  r2 = sum(x2)  
  r3 = sum(x3)  
  tmax = max(t) # Record last time step
  
  # Get product of log-densities at each time step, for all failures then
  prob_d1 = ((d(t, c = par[1], m = par[4]) %>% log()) * x1) %>% sum()
  prob_d2 = ((d(t, c = par[2], m = par[5]) %>% log()) * x2) %>% sum()
  prob_d3 = ((d(t, c = par[3], m = par[6]) %>% log()) * x3) %>% sum()
  
  # For last time step, get probability of each remaining unit surviving 
  prob_r1 = r(t = tmax, c = par[1], m = par[4])^(n1 - r1) %>% log()
  prob_r2 = r(t = tmax, c = par[2], m = par[5])^(n2 - r2) %>% log()
  prob_r3 = r(t = tmax, c = par[3], m = par[6])^(n3 - r3) %>% log()
  
  # Get joint log-likelihood, across ALL vectors
  prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3
}


# And let's run MLE!
mle = optim(
  par = c(1000, 1000, 1000, 1, 1,1), 
  t = data$t,  
  x1 = data$r85,
  n1 = n85,  
  x2 = data$r105,  
  n2 = n105,
  x3 = data$r125,  
  n3 = n125,
  fn = ll,  
  control = list(fnscale = -1))


# Extract parameters into a dataframe
p = tibble(
  c85 = mle$par[1],
  c105 = mle$par[2],
  c125 = mle$par[3],
  m85 = mle$par[4],
  m105 = mle$par[5],
  m125 = mle$par[6])

# Acceleration Factor from 85 C to 105 C
p$c85 / p$c105
# Acceleration Factor from 105 to 125 C
p$c105 / p$c125
# Acceleration Factor from 85 to 125 C
p$c85 / p$c125

rm(list = ls())




# 4. MLE 3 times FOR WEIBULL ACCELERATION MODELING #####################
# Not really recommended -- just an extra example to show the distinction


library(dplyr) # for data wrangling
library(broom) # for tidying model objects

# Let's make a data.frame matching Example 1 from the lesson slides
data = tibble(t = c(24, 72,168,300, 500, 750, 1000, 1250, 1500),
              r85 = c(1, 0, 0, 1, 0, 3, 0, 1, 2),
              r105 = c(2, 1, 3, 2, 2, 4, 5, 1, 4),
              r125 = c(5, 10, 13, 2, 3, 2, 2, 1, 0) )
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
d = function(t, m, c){  (m / t) * (t / c)^m * exp(-1*(t/c)^m)  }
r = function(t, m, c){  exp(-(t/c)^m) }

# Let's write our crosstable's likelihood function
ll = function(t, x1, n1, par){
  # Get total failures
  r1 = sum(x1)  
  tmax = max(t) # Record last time step
  
  # Get product of log-densities at each time step, for all failures then
  prob_d1 = ((d(t, c = par[1], m = par[2]) %>% log()) * x1) %>% sum()

  # For last time step, get probability of each remaining unit surviving 
  prob_r1 = r(t = tmax, c = par[1], m = par[2])^(n1 - r1) %>% log()

  # Get joint log-likelihood, across ALL vectors
  prob_d1 + prob_r1
}


# And let's run MLE!
mle85 = optim(par = c(1000, 1),  t = data$t,   x1 = data$r85, n1 = n85, fn = ll,  control = list(fnscale = -1))

mle105 = optim(par = c(1000, 1),  t = data$t,   x1 = data$r105, n1 = n105, fn = ll,  control = list(fnscale = -1))

mle125 = optim(par = c(1000, 1),  t = data$t,   x1 = data$r125, n1 = n125, fn = ll,  control = list(fnscale = -1))


# Extract parameters into a dataframe
p = tibble(
  c85 = mle85$par[1],
  c105 = mle105$par[1],
  c125 = mle125$par[1],
  m85 = mle85$par[2],
  m105 = mle105$par[2],
  m125 = mle125$par[2])

p
# Acceleration Factor from 85 C to 105 C
p$c85 / p$c105
# Acceleration Factor from 105 to 125 C
p$c105 / p$c125
# Acceleration Factor from 85 to 125 C
p$c85 / p$c125


rm(list = ls())



# 5. Conditional Probability of Failure given Burn-In #############################

# Let's write the Weibull density and failure function, as always...
d = function(t, c, m){  (m / t) * (t / c)^m * exp(-1*(t/c)^m)   }
f = function(t, c, m){ 1 - exp(-1*((t/c)^m)) }

fb = function(t, tb, a, c, m){ 
  # Change in probability of failure
  delta_failure <- f(t = t + a*tb, c, m) - f(t = a*tb, c, m)  
  # Reliability after burn-in period
  reliability <- 1 - f(t = a*tb, c, m)
  # conditional probability of failure
  delta_failure / reliability
}

# 1000 hours after burn-in
# with a burn-in period of 100 hours
# an acceleration factor of 20
# characteristic life c = 2000 hours
# and
# shape parameter m = 1.5
fb(t = 1000, tb = 100, a = 20, c = 2000, m = 1.5)


