

library(dplyr)
library(readr)
library(broom)
library(texreg)
library(gtools)

cities = read_csv("workshops/jp_matching_experiment.csv") %>% 
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")))

cities %>% glimpse()



# Let's write a little tidier function..
tidier = function(model, ci = 0.95, digits = 3){
  model %>% # for a model object
    # get data.frame of coefficients
    # ask for a confidence interval matching the 'ci' above! 
    broom::tidy(conf.int = TRUE, conf.level = ci) %>% 
    # And round and relabel them
    reframe(
      term = term,  
      # Round numbers to a certain number of 'digits'
      estimate = estimate %>% round(digits),
      se = statistic %>% round(digits),
      statistic = statistic %>% round(digits),
      p_value = p.value %>% round(digits),
      # Get stars to show statistical significance
      stars = p.value %>% gtools::stars.pval(),
      # Get better names
      upper = conf.high %>% round(digits),
      lower = conf.low %>% round(digits))
}




# 1. Estimate the effect of being hit by the tsunami on income per capita, 
# controlling for damage rates.
m = cities %>% lm(formula = income_per_capita ~  damage_rate + by_tsunami)
tidier(m)

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].



# 2. Estimate the effect of being hit by the tsunami on 
# the natural log of income per capita, 
# controlling for damage rates.
# Compare this against a model without the natural log.
m1 = cities %>% lm(formula = income_per_capita ~  damage_rate + by_tsunami)
m2 = cities %>% lm(formula = log(income_per_capita) ~  damage_rate + by_tsunami)

screenreg(l = list(m1,m2))
# Do your slopes change? Do your units change?
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].






# 3. Model the effect of time on income per capita, 
# controlling for relevant traits.
m1 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + factor(year) )
m2 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + as.numeric(year) )

# View the resulting statistical table. 
# How does the information change when we control for year vs. each year? 
screenreg(l = list(m1, m2))





# 4. Estimate a model of income per capita, predicted by 
#     population density, unemployment, damage rates, and tsunami status.
m = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                damage_rate + by_tsunami + year)

# Now predict the level of income per capita as damage rates increase 
# from their min to their max.
# Choose MEANINGFUL levels to set other predictors to. Here's starter values.
tibble(
  pop_density = 10,
  unemployment = 20,
  damage_rate = 1,
  by_tsunami = "Hit",
  year = "2012"
) %>%
  mutate(yhat = predict(m, newdata = .))




# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Now model them. 
cities %>%
  mutate(pop_density = scale(pop_density),
         unemployment = scale(unemployment),
         damage_rate = scale(damage_rate)) %>%
  lm(formula = income_per_capita ~ pop_density + unemployment + 
       damage_rate + by_tsunami + year)

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?


# 6. Compare these 5 models, which each add extra covariates.
m1 = cities %>% lm(formula = income_per_capita ~ damage_rate + by_tsunami) 
m2 = cities %>% lm(formula = income_per_capita ~ damage_rate + by_tsunami + 
                     year) 
m3 = cities %>% lm(formula = income_per_capita ~ damage_rate + by_tsunami + 
                     year + 
                     pop_density + unemployment)
m4 = cities %>% lm(formula = income_per_capita ~ damage_rate + by_tsunami + 
                     year + 
                     pop_density + unemployment +
                     exp_dis_relief_per_capita + pop_women + pop_over_age_65)
m5 = cities %>% lm(formula = income_per_capita ~ damage_rate + by_tsunami +
                     year + 
                     pop_density + unemployment +
                     exp_dis_relief_per_capita + pop_women + pop_over_age_65 +
                     pref)
# Show models but omit vars that contain year or prefecture, for clearer viewing
screenreg(l = list(m1,m2,m3,m4,m5), omit.coef = c("pref|year"))

# How does the explanatory power change by model? (R2)
# Which covariates add the **most** explanatory power?





# 7. Which Year can we model best? Which has the Highest Explanatory Power?
# For each year, make a model and return a data.frame glance()-ing the model
cities %>% 
  group_by(year) %>%
  reframe(lm(formula = income_per_capita ~ damage_rate + by_tsunami + 
               pop_density + pref) %>% glance())
# Hint: look at r.squared.



# 8. In which prefecture (region) did the damage_rate have the worst effect?
# Get the model effects
data = cities %>%
  group_by(pref) %>%
  reframe(lm(formula = income_per_capita ~ damage_rate + pop_density + year) %>%
            tidier())
# Filter the model effects
data %>% filter(term == "damage_rate")

# Report the effects.
# Disaster damage had the most negative effect [BETA] on wealth in [XXX] (p < VALUE),
# but the least negative effect [BETA] on wealth in [YYY] (p < VALUE)





# 9. Compare these two data.frames. 
# What does it mean to estimate an intercept-only model?

# Intercept-only model
cities %>% lm(formula = income_per_capita ~ 1)
# Descriptive Stats
cities %>% summarize(mean = mean(income_per_capita))



# 10. Model the effect of each year on income. 
# Which year is not represented? The intercept represents that baseline category.
cities$year %>% unique()
m = cities %>% lm(formula = income_per_capita ~ year)
m 
# Calculate the predicted income per capita from 2011 to 2017.

