
# When using MLE

library(readr)
crops = read_csv("workshops/crops.csv")
d = function(t, lambda){lambda * exp(-t*lambda) }
# EXPONENTIAL
ll = function(par, t){
  # Testing values
  # t = crops$days; par = 0.001
  dexp(t, rate = par[1]) %>% log() %>% sum()
}
optim(par = c(0.001), fn = ll, t = crops$days, control = list(fnscale = -1))
# Translation:
# Our data crops$days, if exponentially distributed, is most likely to have a 
# failure rate lambda of 0.014.


# WEIBULL
ll = function(par, t){
  # Testing values
  dweibull(t, shape = par[1], scale = par[2]) %>% log() %>% sum()
}
optim(par = c(1, 10000), fn = ll, t = crops$days, control = list(fnscale = -1))
# Translation:
# Our data crops$days, if weibull distributed, is most likely to have a 
# shape parameter m of 1.49 and a characteristic life c of 77.2 days









# Loglikelihood - do you need a vector for it to work? --> YES! Good point.

crops$days %>% hist()

# https://timothyfraser.com/sigma/useful-life-distributions-weibull-gamma-lognormal.html#multi-parameter-optimization
n = 75
r = 50
tmax = 200
crops$days

t = crops$days
par = 0.001
c(1,2,3) %>% prod()

# What's the joint probability that the first 50 did fail?
prob_d = dexp(t, rate = par[1]) %>% prod()
# What's the joint probability that the other 25 didn't fail?
prob_r = (1 - pexp(tmax, rate = par[1]))^(n - r)

# What's the joint probability that BOTH things occurred?
loglik = log(prob_d * prob_r)


ll = function(par, t){
  n = 75
  r = 50
  tmax = 200
  
  # What's the joint probability that the first 50 did fail?
  prob_d = dexp(t, rate = par[1]) %>% prod()
  # What's the joint probability that the other 25 didn't fail?
  prob_r = (1 - pexp(tmax, rate = par[1]))^(n - r)
  
  # What's the joint probability that BOTH things occurred?
  log(prob_d * prob_r)
  
}
optim(par = c(0.001), fn = ll, t = crops$days, control = list(fnscale = -1))









