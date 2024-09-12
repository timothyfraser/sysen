# workshop_3_solutions.R
# Workshop 3: PDFs and CDFs in R
# Dr. Fraser


# Below, please find the following content for our recitation class from Friday.
library(dplyr) # data wrangling
library(ggplot2) # visuals
# install.packages("mosaicCalc")
library(mosaicCalc) # derivatives and integrals


# Exercise 1: Class teaches Dr. Fraser to analyze PDFs and CDFs

### How to make a function!
addtwo = function(x){  x + 2 }
addtwo(x = 2)
remove(addtwo)

### When the PDF is provided ###################################

# the function that produces the line, 
# or the probability for every x value

# probability density function --> probability distribution

d = function(x){  (x + 2*x)/1000  }

d(x = 1)
# There is a 0.3% chance that we would get a value of 1
# from this particular distribution / density function.

# EXACTLY 1. --> probability densities
# More than or Less than 1 --> cumulative probabilities


# toaster - time (hours) to failure 
d(x = 50)
x = c(0, 50, 100, 150, 200, 250, 300)
d(x)
remove(x)


# Make our own `tibble` (an empowered data.frame from dplyr)
toasters = tibble(
  hours = c(0:1000),
  # you can run functions within them on their component vectors
  dprob = d(hours)
)

toasters %>% plot()


gg = toasters %>% 
  ggplot(mapping = aes(x = hours, y = dprob)) +
  geom_area(fill = "steelblue", color = "black", size = 1.2, alpha = 0.5) +
  labs(x = "Hours to Failure", y = "Probability (Density)",
       title = "Toaster Failure",
       subtitle = "Probability Density Function")  +
  theme_classic()



gg

gg + theme(plot.title = element_text(hjust = 0.5),
           plot.subtitle = element_text(hjust = 0.5))


ggsave(plot = gg, 
       filename = "myplot.png", 
       height = 4, width = 4)






### Simulated Distributions ###################################

# Archetypal Distributions, normal, poisson
rpois()
dpois()
ppois()
qpois()


# mean of 50 hours to failure
mu = 50

dat = tibble(
  sim = rpois(n = 10, lambda = 50)
)

dat$sim %>% hist()

dat %>%
  ggplot(mapping = aes(x = sim)) +
  geom_density()



toasters2 = tibble(
  hours = 1:100,
  # probability densities
  dprob = dpois(hours, lambda = 50),
  # cumulative probabilities
  cprob = ppois(hours, lambda = 50),
  cprob2 = cumsum(dprob) / sum(dprob),
  # get back raw values
  q = qpois(cprob, lambda = 50)
)
toasters2 %>% head()

toasters2 %>%
  ggplot(mapping = aes(x = hours, y = cprob2)) +
  geom_area()



# Empirical Hours to Failure for Some Toasters
obs = c(10,50, 20, 30, 40, 50, 30, 20, 90)
obs %>% hist()
obs %>% density() %>% plot()
dobs = obs %>% density() %>% approxfun()

# empirical probability density function
dobs(20)

# empirical cumulative probability function for d()
pobs = mosaicCalc::antiD(tilde = d(x) ~ x)
pobs(x = c(1,2,3))

# Can't really easily do that for our approxfun()
dobs


# probabilities densities
dreal(c(1,2,3,4))


toasters3 = tibble(
  hours = seq(from = 0, to = 100, length.out = 9),
  dprob = dobs(hours),
  cprob = cumsum(dprob) / sum(dprob)
)

pobs = approxfun(x = toasters3$hours, y = toasters3$cprob) 
pobs(10)




toasters3 %>%
  ggplot(mapping = aes(x = hours, y = dprob)) +
  geom_area()


toasters3 %>%
  ggplot(mapping = aes(x = hours, y = cprob)) +
  geom_area()




# The cost of a component varies depending on market conditions.
# Over the last year, analysts report is cost on average $50, 
# with a standard deviation of $5.
# Assume normal distribution - so dnorm, etc.

# Pick 2!

# Q1. What is the probability the component will cost exactly $60?
dnorm(60, mean = 50, sd = 5)

# Q2. What is the probability the component costs less than $60?
pnorm(60, mean = 50, sd = 5)

# Q3. What is the probability that the component costs more than $60?
1 - pnorm(60, mean = 50, sd = 5)

# Q4. What price is greater than 75% of all sales?
qnorm(0.75, mean = 50, sd = 5)

# Q5. What is the probability it costs between $45 and $55?
pnorm(55, mean = 50, sd = 5) - pnorm(45, mean = 50, sd = 5)


