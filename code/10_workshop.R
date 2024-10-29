#' @name workshop_10.R
#' @title Physical Acceleration Models


# Packages
library(dplyr)
library(broom)

# STEP 1: FIND THIS DATA
# STEP 2: LOAD THIS DATA
# STEP 3: MODEL THIS DATA
# STEP 4: PREDICT WITH THIS DATA


alt <- tibble(
  # Characteristic life in hours
  c = c(1400, 1450, 1500, 1550, 1650),
  # Temperature in Celsius
  temp = c(160, 155, 152, 147, 144),
  # Temperature Factor (a standardized unit)
  tf = 1 / (1 / 11605 * (temp + 273.15)),
  # Voltage, in volts
  volts = c(17, 16.5, 14.5, 14, 13),
  # Hours of life spent by time of test
  time = c(1200, 1000, 950, 600, 500),
  # Performance Rating, in Amps
  rating = c(60, 70, 80, 90, 100))

# Line of best fit in ggplot
ggplot() +
  geom_point(data = alt, mapping = aes(x = temp, y = c )) +
  geom_smooth(data = alt, mapping = aes(x = temp, y = c),
              method = "lm", se = FALSE)


m1 = alt %>% lm(formula = c ~ temp)
m1
m1 %>% glance() %>% select(r.squared)
# r.squared

m2 = alt %>% lm(formula = log(c) ~ temp)
m2
exp(8.794759)
m2 %>% glance()


tibble(
  temp = seq(from = 0, to = 200, by = 10),
  chat = predict(m2, newdata = tibble(temp)) %>% exp()
)


chat = function(temp){ exp(8.794759 + -0.009739*temp) }
chat(temp = 32)

# rexp(n = 1000, rate = 0.001) %>% log() %>% hist()

# y = e^(a + beta*x)
# ln(y) = a + beta*x

# [y = alpha + beta*x]
# alpha = intercept
# beta = slope of temperature






# Let's write ourselves a speedy weibull density function 'd()'
d = function(t, m, c){
  (m / t) * (t / c)^m * exp(-1*(t/c)^m)
  # or dweibull(t, scale = c, shape = m)
}

# Suppose the lifespans under normal usage are just off by a factor of ~2.5
# then we could project the PDF under normal usage like:

airbags <- data.frame(t = seq(1, 12000, by = 20)) %>%
  mutate(d_stress = d(t, c = 4100, m = 1.25)) %>%
  mutate(d_usage = d(t = t / 2.5, c = 4100, m = 1.25) / 2.5)


ggplot() +
  # Plot the PDF under stress conditions 
  geom_line(data = airbags, mapping = aes(x = t, y = d_stress, color = "Stress"), 
            linewidth = 1.5) +
  # Plot the PDF under normal usage conditions
  geom_line(data = airbags, mapping = aes(x = t, y = d_usage, color = "Normal Usage"), 
            linewidth = 1, linetype = "dashed") +
  # Add a nice theme and clear labels
  theme_classic(base_size = 14) +
  labs(x = "Airbag Lifespan in hours (t)", y = "Probability Density d(t)",
       color = "Conditions", 
       subtitle = "We want Lifespan under Normal Usage,\nbut can only get Lifespan under Stress")


# Let's write a weibull quantile function
q = function(p, c, m){  qweibull(p, scale = c, shape = m)  }

# Get median under stress
median_s <- q(0.5, c = 4100, m = 1.25)
# Get median under normal conditions
median_u <- q(0.5, c = 4500, m = 1.5)

# Calculate it!
af = median_u / median_s
# Check the Acceleration Factor!
af




alt <- tibble(
  # Characteristic life in hours
  c = c(1400, 1450, 1500, 1550, 1650),
  # Temperature in Celsius
  temp = c(160, 155, 152, 147, 144),
  # Temperature Factor (a standardized unit)
  tf = 1 / (1 / 11605 * (temp + 273.15)),
  # Voltage, in volts
  volts = c(17, 16.5, 14.5, 14, 13),
  # Hours of life spent by time of test
  time = c(1200, 1000, 950, 600, 500),
  # Performance Rating, in Amps
  rating = c(60, 70, 80, 90, 100))

alt

g <- alt %>%
  ggplot(mapping = aes(x = tf, y = log(c) )) +
  geom_point(size = 5) + # Add scatterplot points
  geom_smooth(method = "lm", se = FALSE) +
  # Make line of best fit, using lm() - a linear model
  # we can write 'se = FALSE' (standard error = FALSE) to get rid of the confidence interval
  # Add theme
  theme_classic(base_size = 14) +
  # Add labels
  labs(title = "Arrhenius Model, Visualized",
       subtitle = "Model Equation:  log(c) = 3.1701 + 0.1518 TF    \nModel Fit: 96%",
       # We can add a line-break in the subtitle by writing \n
       x = "Temperature Factor (TF)", y = "Characteristic Lifespan log(c)")
g


m1 = alt %>% lm(formula = log(c) ~ tf)
m1 %>% glance() %>% select(r.squared)
m1
# Interpreting our model
# If the temperature factor tf = 0, we predict log(c) = 3.1701
# If temperature factor tf +1, we predict log(c) increases by beta = deltaH = 0.1518


c_hat = function(tf){ exp( 3.1701 + 0.1518*tf) }
c_hat(tf = 2)
# Or better yet, let's calculate temperature factor 'tf' too,
# so we only have to supply a temperature in Celsius
tf = function(temp){
  k = 1 / 11605   # Get Boltzmann's constant
  1 / (k * (temp + 273.15)) # Get TF!
}
# Now predict c_hat for 30, 60, and 90 degrees celsius!
c_hat = function(temp){  exp( 3.1701 + 0.1518*tf(temp))  }

c(30, 60, 90) %>% c_hat()



fakedata = tibble(
  temp = seq(0, 200, by = 10),
  tf = tf(temp)
)

m1 %>% predict(newdata = fakedata)

m1 %>% predict(newdata = fakedata) %>% exp()


# Or do it all at once!
tibble(
  temp = seq(0, 200, by = 10),
  tf = tf(temp),
  c_hat = predict(m1, newdata = tibble(tf)) %>% exp())



m2 <- alt %>%
  lm(formula = log(c) ~ tf + log(volts) )

fakedata <- tibble(
  # Hold temperature constant
  temp = 30,
  tf = tf(temp),
  # But vary volts
  volts = seq(from = 1, to = 30, by = 1),
  # Predict c_hat
  c_hat = predict(m2, newdata = tibble(tf, volts)) %>% exp())

fakedata %>%
  ggplot(mapping = aes(x = volts, y = c_hat)) +
  geom_line() +
  geom_point() +
  theme_classic(base_size = 14) +
  labs(title = "Eyring Model of Effect of Voltage on Lifespan (30 Deg. Celsius)",
       subtitle = "Equation: c = e^(5.0086 + 0.1027 TF - 0.1837 * log(volts))",
       x = "Voltage (volts)", y = "Predicted Characteristic Life (c-hat)")


alt %>%
  lm(formula = log(rating) ~ time)


alt %>%
  lm(formula = log(rating) ~ I(volts * time) )



m3 <- alt %>%
  lm(formula = log(c) ~ tf + log(volts) + I(volts * time))
# Really good fit!
m3 %>%  glance()





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



dplyr::tribble(
  ~var, ~value,
  "a",  123123,
  "b",  234234
)

dat = dplyr::tribble(
  ~t, ~r1, ~r2, ~r3,
  5,  32,   34,  50,
  15, 27,   17,  34,
  25, 30,   22,  15
)




# Let's write our crosstable's likelihood function
ll = function(t, x1, x2, x3, par){
  # Get total failures
  r1 = sum(x1)  
  r2 = sum(x2)  
  r3 = sum(x3)  
  # Record total sample size in each
  n1 = 200       
  n2 = 175
  n3 = 300
  tmax = max(t) # Record last time step
  
  # Get the product of the log-densities at each time step, for all failures then
  prob_d1 = ((d(t, c = par[1], m = par[4]) %>% log()) * x1) %>% sum()
  prob_d2 = ((d(t, c = par[2], m = par[4]) %>% log()) * x2) %>% sum()
  prob_d3 = ((d(t, c = par[3], m = par[4]) %>% log()) * x3) %>% sum()
  
  # For the last time step, get the probability of each remaining unit surviving 
  prob_r1 = r(t = tmax, c = par[1], m = par[4])^(n1 - r1) %>% log()
  prob_r2 = r(t = tmax, c = par[2], m = par[4])^(n2 - r2) %>% log()
  prob_r3 = r(t = tmax, c = par[3], m = par[4])^(n3 - r3) %>% log()
  
  # Get joint log-likelihood, across ALL vectors
  prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3
}

# And let's run MLE!
mle <- optim(par = c(1000, 1000, 1000, 1), t = wheels$t,  
             x1 = wheels$temp_100,  
             x2 = wheels$temp_150,  
             x3 = wheels$temp_200,  
             fn = ll,  control = list(fnscale = -1))
# Check out our 3 characteristic life parameters, 
# for temp_100, temp_150, and temp_200, and our shared shape parameter!
mle$par



# Remember our function to calculate temperature factors
tf = function(temp){  1 / ((1 / 11605) * (temp + 273.15)) }

# Let's collect our parameter estimates
param <- tibble(
  # For each temperature
  temp = c(100, 150, 200),
  # report the MLE c estimates
  c = mle$par[1:3],
  # and the shared MLE m estimate
  m = mle$par[4],
  # and Calculate TF (for each temperature...)
  # This will be our independent variable
  tf = tf(temp))

# Check it!
param

