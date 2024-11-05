# Workshop_11_exercise.R
# Tim Fraser



# 0. Getting Started ######################################################

library(dplyr)
library(readr)
library(broom)
library(texreg)

cities = read_csv("workshops/jp_matching_experiment.csv") %>% 
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")))

cities %>% glimpse()



# 0.1 Importing Data #########################################################


# You can download the data from github, upload it to RStudio Cloud, and then read it in like this
read_csv("workshops/jp_matching_experiment.csv") %>%
  head()

# Or you could just load in the data like this:
# cities = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/jp_matching_experiment.csv") 

cities = read_csv("workshops/jp_matching_experiment.csv") %>% 
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")))

# Think that's way easier? We can make a little function to make it easier to get this data.
# I'll add in some defaults like author, repository, and branch to make it easy to download data from our repository
github_csv = function(file, author = "timothyfraser", repository = "sysen", branch = "main"){
  paste("https://raw.githubusercontent.com/", 
        author, "/", repository, "/", branch, "/", file, sep = "")
}

# Boom!
"workshops/jp_matching_experiment.csv" %>%
  github_csv() %>% # get csv from github
  read_csv() %>% # read it in
  head() # see first few lines!


# Check it out!
cities %>% head()

# Each row in this dataset is a city-year, in a prefecture,
# covering city-years in the Tohoku region, 
# the region affected by the 2011 earthquake, tsunami, and nuclear disaster in Japan
cities %>%
  filter(pref == "Fukushima") %>%
  filter(year == 2012)

# I prefer using glimpse from the dplyr package
# to see the structure of my data
cities %>%
  glimpse()

# 1. Modeling #########################################################

# We can make a simple regression model 'm'
m = cities %>%
  lm(formula = social_capital ~ damage_rate)

# View the equation
m
# Write the equation!
# Y (social_capital) = 0.39 + 0.07485 * damage_rate

# We can write a function of our model equation, if we want
sc = function(x){ 0.394 + 0.0749 * x }

# We should first calculate our goodness of fit statistics, which I call 'gof'
gof = m %>% 
  glance() %>%
  select(r.squared, sigma, statistic, p.value)
# View it!
gof

# R2 = % of variation explained --> get to 1
# sigma = residual standard error --> error of our model predictions
# statistic (F) = ratio. how much better is my model than an intercept model
# p-value = p-value of the f-statistic = how extreme is my f statistic?
# p < 0.10. p < 0.05. p < 0.01 = great indicators that F is extreme (model is good / better than nothing)

# We can view model coefficients.
m %>% 
  tidy()

# (Or if you like underscores, use my tidier() function from the workshop)

# Finally, what's the general range of our main predictor damage_rate?
cities$damage_rate %>% hist()

# Let's predict, as the damage rate in a city increases, how does its social capital change?
tibble(
  damage_rate =  seq(from = 0, to = 0.6, by = 0.01),
  # We can predict it using our hand-made function sc()
  yhat = sc(damage_rate)) %>%
  # See first few
  head()


# 2. Prediction ########################################################

# Or (preferrably, we can use predict() to do make predictions straight from the model object
dat_sim = tibble(
  damage_rate = seq(from = 0, to = 0.6, by = 0.01),
  # Get predictions
  yhat = predict(m, newdata = tibble(damage_rate)),
  # get sigma
  sigma = glance(m)$sigma
) %>%
  group_by(damage_rate) %>%
  reframe(
    ysim = rnorm(n = 1000, mean = yhat, sd = sigma)
  ) %>%
  group_by(damage_rate) %>%
  summarize(median = median(ysim),
            lower = quantile(ysim, prob = 0.025),
            upper = quantile(ysim, prob = 0.975))


dat_sim %>%
  ggplot(mapping = aes(x = damage_rate, y = median, ymin = lower, ymax = upper)) +
  geom_ribbon() +
  labs(x = "Damage Rate", y = "Predicted Social Capital (Simulated 95% CIs)")


# What IS the residual standard error sigma?
# Well, we can approximate it pretty decently by taking the standard deviation of our models' residuals.
# A residual is the observed minus predicted value for each data point
tibble(residuals = m %>% with(residuals)) %>%
  # Get the standard deviation of residuals
  summarize(sd = sd(residuals),
            # Return the model's residual standard error (which is calculated with just one or two extra steps)
            se = m %>% glance() %>% with(sigma))


# Let's get the 6-sigma range
dat_se = tibble(
  damage_rate = seq(from = 0, to = 0.6, by = 0.01),
  # Get predictions
  yhat = predict(m, newdata = tibble(damage_rate)),
  # get sigma
  sigma = glance(m)$sigma,
  
  lower = yhat - 3*sigma,
  upper = yhat + 3*sigma
)
# They are almost identical!

dat_se %>%
  ggplot(mapping = aes(x = damage_rate, y= yhat)) +
  geom_ribbon(mapping = aes(x = damage_rate, 
                            ymin = lower, ymax = upper),
              fill = "steelblue", alpha = 0.5) +
  geom_line(linetype = "dashed") +
  theme_classic() +
  labs(x = "Damage Rate", y = "Predicted Social Capital (6 sigmas)")


# We can also compute confidence intervals for our predictions
# for any specified percentile.
dat_q = tibble(
  damage_rate =  seq(from = 0, to = 0.6, by = 0.01),
  yhat = predict(m, newdata = tibble(damage_rate)),
  # Get residual standard error 'se'
  se = m %>% glance() %>% with(sigma),
  # Calculate the z-score on a normal distribution for the 97.5th percentile
  z = qnorm(0.975),
  # Give me an upper 95% confidence interval at the 97.5th percentile
  upper = yhat + se * z,
  # Give me a lower 95% confidence interval at the 2.5th percentile
  lower = yhat - se * z
)


dat_q %>%
  ggplot(mapping = aes(x = damage_rate, y= yhat)) +
  geom_ribbon(mapping = aes(x = damage_rate, 
                            ymin = lower, ymax = upper),
              fill = "steelblue", alpha = 0.5) +
  geom_line(linetype = "dashed") +
  theme_classic() +
  labs(x = "Damage Rate", y = "Predicted Social Capital (95% CI)")




# Let's compare all three!

ggplot() +
  geom_ribbon(
    data = dat_se, 
    mapping = aes(x = damage_rate, ymin = lower, ymax = upper, 
                  fill = "6 sigma"), alpha = 0.5) +
  geom_ribbon(
    data = dat_q, 
    mapping = aes(x = damage_rate, ymin = lower, ymax = upper, 
                  fill = "95% CI"), alpha = 0.5) +
  geom_ribbon(
    data = dat_sim, 
    mapping = aes(x = damage_rate, ymin = lower, ymax = upper, 
                  fill = "Simulated 95% CI"), alpha = 0.5) +
  geom_line(
    data = dat_se, 
    mapping = aes(x = damage_rate, y = yhat), linetype = "dashed") +
  scale_fill_manual(values = c("steelblue", "goldenrod", "firebrick")) +
  theme_classic() +
  labs(x = "Damage Rate", y = "Predicted Social Capital", fill = "CI Type") +
  theme(legend.position = "bottom")



# 3. Key Stats of Interest #########################

m = cities %>%
  lm(formula = income_per_capita ~ damage_rate)

get_stat = function(m){
  m %>% broom::glance() %>%
    select(r.squared, sigma, statistic, p.value)
}

get_stat(m)



m$coefficients
m$fitted.values



d = tibble(
  # predicted or expected
  yhat = m$fitted.values,
  # observed
  y = m$model$income_per_capita,
  # calculate the difference between the observed and expected...
  residuals = y - yhat
)


d %>%
  summarize(
    # all the variation in your data
    tss = sum( (y - mean(y))^2 ),
    # sum of squared deviations
    rss = sum( (y - yhat)^2 ),
    # EXPLAINED SUM OF SQUARES
    ess = tss - rss,
    # PERCENTAGE OF VARIATION EXPLAINED, out of TOTAL VARIATION
    rsq = ess / tss,
    rsq = 1 - rss / tss
  )


# F-statistic







d %>%
  summarize(
    tss = sum( (y - mean(y))^2),
    rss = sum( (y - yhat)^2  ),
    rsq = 1 - rss / tss
  )


d %>%
  summarize(
    # Calculate residual sum of squares
    residual_sum_of_squares = sum( (y - yhat) ^2),
    # Calculate total sum of squares
    total_sum_of_squares = sum( (y - mean(y))^2 ),
    # Get sample size
    n = n(),
    # Calculate number of variables in your model
    p = 2,
    # Calculate explained sum of squares
    ess = total_sum_of_squares - residual_sum_of_squares
  ) %>%
  mutate(
    # Mean Squares due to Regression, given the no. of predictors
    mean_squares_due_to_regression = ess / (p - 1),
    # Mean Squared Error
    # How much variation was NOT explained, given the sample size and no. of variables
    mean_squared_error = residual_sum_of_squares / (n - p),
    # sigma-squared
    # RMSE = sigma
    sigma = sqrt(mean_squared_error) 
  )  %>%
  
  # Compute the F-statistic, which is a ratio of explained vs. unexplained variation
  mutate(f_statistic = mean_squares_due_to_regression / mean_squared_error) %>%
  # Finally, throw it into this pf function,
  # which plots a theoretical null distribution 
  # based on the number of variables and sample size,
  # and identifies how extreme our F-statistic is compared to one we'd get by chance
  # Computes p-value
  mutate(p_value = pf(f_statistic, df1 = p - 1, df2 = n - p, lower.tail = FALSE))  %>%
  glimpse()

# IF our p-value is less than 5%, 
# that's often a good indication
# that our model fits better than a simple intercept (mean) would.
# a good f-statistic
pf(15, df1 = 2 - 1, df2 = 1057 - 2, lower.tail = FALSE)

d %>% glimpse()

m %>% broom::glance()


glance(m)$sigma
m$residuals %>% sd()


