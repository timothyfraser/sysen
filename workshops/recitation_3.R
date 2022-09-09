# Find the prob that someone visits more than 5 stalls

# Normal Distribution

# rnorm()

# mean
# sd 

# Simulated 5 points on the distribution
rnorm(n = 5, mean = 5.5, sd = 2.5)

# Cumulative Prob
x <- pnorm(5, mean = 5.5, sd = 2.5)

# More than 5?
1 - x



obs <- c(1, 5, 3, 4, 3, 2, 3)

library(dplyr)
library(broom)
library(ggplot2)

dat <- obs %>% density() %>% tidy()

ggplot(data = dat, mapping = aes(x = x, y = y)) +
  geom_area()

ggplot(data = dat, mapping = aes(x = x, y = y)) +
  geom_area(fill = "steelblue") +
  geom_line(color = "pink", size = 10)


dobs <- dat %>% approxfun()

dobs(3)
dobs(0)

c(0,1,2,3,4,5,6) %>% dobs()

0:6 %>% dobs()

dat  %>%
  mutate(ycum = cumsum(y),
         p = ycum / sum(y))

pobs <- dat %>%
  mutate(y = cumsum(y) / sum(y)) %>%
  approxfun()

0:5%>% pobs()

dat %>%
  mutate(y = cumsum(y) / sum(y)) %>%
  ggplot(mapping = aes(x = x , y =y)) +
  geom_area()


# How to check colors
colors







# Questions for Recitation 3


# The cost of a component varies depending on market conditions.
# Over the last year, analysts report is cost on average $50, 
# with a standard deviation of $5.

# What is the probability the component will cost exactly $60?


# What is the probability the component costs less than $60?


# What is the probability that the component costs more than $60?

# What price is greater than 75% of all sales?


# What is the probability it costs between $45 and $55?



# Q2. You're developing a new medical device for measuring blood sugar. You might test "High" (T = 1) vs. "Fine" (0), and you might *actually* be "High" (R = 1) or "Fine" (0) 

# Given that you tested "High", what's the probability that your blood sugar is *actually* "High"?
# Fortunately, you collected the crosstable.
# Here's your data.

# 4 people really were "High" when they tested "High".
# 6 people really were "High" when they tested "Fine".
# 5 people really were "Fine" when they tested "Fine".
# 3 people really were "Fine" when they tested "High".

# Find the probability P(R=1|T=1), and use this empirical data to PROVE that Bayes Rule works.
