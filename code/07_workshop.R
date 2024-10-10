# 07_workshop.R

# Load packages
library(dplyr)
library(ggplot2)

# Product Times to Failure
hours = c(1,2,2,3,4,5,7,8,9,10,
          11,13,15,16,17,17,18,18,18,20,
          20,21,21,24,27,29,30,37,40,40,
          40,41,46,47,48,52,54,54, 55,55,
          64,65,65,65,67,76,76,79,80,80,
          82,86,87,89,94,96,100,101,102,104,
          105,109,109,120,123,141,150,156,156,161,
          164,167,170,178,181,191,193,206,211,212,
          214,236,238,240,265,304,317,328,355,363,
          365,369,389,404,427,435,500,522,547,889)


hours

# Use ggplot2's cut_interval() to recode values as categories
cut_interval(hours, length = 55)

as.numeric(hours)
as.character(hours)
as.factor(hours)


factor(c("cats", "birds", "birds", "dogs"))

factor(c("cats", "birds", "birds", "dogs"),
       levels = c("cats", "birds", "dogs"))


tibble(t = hours) %>%
  mutate(interval = cut_interval(hours, length = 55)) %>%
  arrange(desc(interval))

tmax = 1000

# Three equivalent ways to tally up observations

tibble(t = hours) %>%
  mutate(interval = cut_interval(hours, length = 55))  %>%
  group_by(interval) %>%
  summarize(r_obs = length(t))


tibble(t = hours) %>%
  mutate(interval = cut_interval(hours, length = 55))  %>%
  group_by(interval) %>%
  summarize(r_obs = n())

tibble(t = hours) %>%
  mutate(interval = cut_interval(hours, length = 55))  %>%
  group_by(interval) %>%
  summarize(r_obs = sum(t < tmax))



# But if we ant to hold onto the categories with zero observations, 
# we need .drop = FALSE
tibble(t = hours) %>%
  mutate(interval = cut_interval(hours, length = 55))  %>%
  group_by(interval, .drop = FALSE) %>%
  summarize(r_obs = n())




# We can write ourselves a crosstab() function to do it for us
crosstab = function(x, binsize = 55){
  
  tibble(t = x) %>%
    mutate(interval = cut_interval(hours, length = binsize))  %>%
    group_by(interval, .drop = FALSE) %>%
    summarize(r_obs = n())
}

# Yay!
tab = crosstab(hours, binsize = 100)

tab

# But hang on = some intervals have fewer than 5 failures per interval.

# We could recode the intervals
# and then aggregate the number of failures using the new intervals

# Do do so, we can use case_when() --> a conditional operator, like ifelse
tab2 = tab %>%
  mutate(interval = case_when(
    interval == "(500,600]" ~ "(400,500]",
    interval == "(600,700]" ~ "(400,500]",
    interval == "(700,800]" ~ "(400,500]",
    interval == "(800,900]" ~ "(400,500]",
    # otherwise, return this thing after the tilda
    TRUE ~ interval
  ),
  # But it needs to be remade into a
  # factor again to remember interval order
  interval = factor(
    interval,
    levels = c("[0,100]", "(100,200]",
               "(200,300]", "(300,400]", "(400,500]",
               "(500,600]", "(600,700]",
               "(700,800]", "(800,900]"))
  
  )

# Then, we can aggregate to the revised intervals
tab3 = tab2 %>% 
  group_by(interval) %>%
  summarize(r_obs = sum(r_obs))

# We could finish up like this
binsize = 100
tab3 %>%
  mutate(bin = as.numeric(interval)) %>%
  mutate(lower = (bin - 1) * binsize,
         upper = (bin * binsize),
         midpoint = (lower + upper) / 2) 



# We could try to make our own function to do it all...
crosstab2 = function(x, binsize = 100, .midpoint = 450, .interval = "(400,500]", .binid = 5){
  # Testing Values
  # x = hours
  # binsize = 100
  # .midpoint = 450
  # .interval = "(400,500]"
  # .binid = 5
  
  data = tibble(t = x) %>%
    mutate(interval = cut_interval(hours, length = binsize))  %>%
    group_by(interval, .drop = FALSE) %>%
    summarize(r_obs = n())
  
  
  data = data %>%
    mutate(bin = as.numeric(interval)) %>%
    mutate(lower = (bin - 1) * binsize,
           upper = (bin * binsize),
           midpoint = (lower + upper) / 2) 
  
  
  data = data %>%
    mutate(interval = case_when(
      midpoint >= .midpoint ~ .interval,
      TRUE ~ interval
    ),
    bin = case_when(
      midpoint >= .midpoint ~ .binid, 
      TRUE ~ bin)) 
  
  output = data %>%
    group_by(bin, interval) %>%
    summarize(r_obs = sum(r_obs))
  
  output = output %>%  
    mutate(lower = (bin - 1) * binsize,
           upper = (bin * binsize),
           midpoint = (lower + upper) / 2) %>%
    select(bin,interval, midpoint,  r_obs)
  
  return(output)
}

# It works so-so.
crosstab2(x = hours, binsize = 100,
          .midpoint = 450, .interval = "(400,500]", .binid = 5)




# I went on to update this and have provided a helper function under
# functions/function_crosstab.R
# Try it out!
source("functions/functions_crosstab.R")


# Product Times to Failure
hours = c(1,2,2,3,4,5,7,8,9,10,
          11,13,15,16,17,17,18,18,18,20,
          20,21,21,24,27,29,30,37,40,40,
          40,41,46,47,48,52,54,54, 55,55,
          64,65,65,65,67,76,76,79,80,80,
          82,86,87,89,94,96,100,101,102,104,
          105,109,109,120,123,141,150,156,156,161,
          164,167,170,178,181,191,193,206,211,212,
          214,236,238,240,265,304,317,328,355,363,
          365,369,389,404,427,435,500,522,547,889)

# By default, it applies no cutoff.
crosstab(x = hours, binsize = 100)
# But if you add a cutoff, it will aggregate categories past that cutoff
crosstab(x = hours, binsize = 100, cutoff = 450)





# Extra Examples ##############################################


# Try starting bin size of 55
data.frame(
  t = hours
) %>%
  mutate(label = cut_interval(t, length = 55)) %>%
  group_by(label, .drop = FALSE) %>%
  summarize(r_obs = n()) %>%
  mutate(bin = as.numeric(label),
         lower = (bin - 1) * 55,
         upper = (bin * 55),
         midpoint = (lower + upper) / 2) %>%
  select(bin,label, midpoint,  r_obs)


# Let's functionify this...

crosstab = function(x, binsize = 55){
  data.frame(
    t = x
  ) %>%
    mutate(label = cut_interval(t, length = binsize)) %>%
    group_by(label, .drop = FALSE) %>%
    summarize(r_obs = n()) %>%
    mutate(bin = as.numeric(label),
           lower = (bin - 1) * binsize,
           upper = (bin * binsize),
           midpoint = (lower + upper) / 2) %>%
    select(bin,label, midpoint,lower,upper, r_obs)
}



tab = crosstab(hours, binsize = 100) 

# Edit your categories

tab = tab %>%
  mutate(label = case_when(
    midpoint >= 450 ~ "(400,900]",
    TRUE ~ label
  ), bin = case_when(midpoint >= 450 ~ 5, TRUE ~ bin)) 

tab
tab = tab %>%
  group_by(bin, label) %>%
  summarize(r_obs = sum(r_obs)) %>%
  mutate(lower = (bin - 1) * 100,
         upper = (bin * 100),
         midpoint = (lower + upper) / 2) %>%
  select(bin,label, midpoint,lower,upper, r_obs)


lambda_hat = 0.00725
n = 100
tab$r_obs %>% sum()
f = function(t,lambda){ 1 - exp(-lambda*t)}
ingredients = tab %>%
  mutate(f2 = f(upper, lambda_hat),
         f1 = f(lower, lambda_hat),
         prob = f2 - f1,
         r_exp = prob * n) 

ingredients %>%
  select(label, f2, f1, prob, r_exp)

# Try bin size of 100
data.frame(
  t = hours
) %>%
  mutate(label = cut_interval(t, length = 100)) %>%
  group_by(label, .drop = FALSE) %>%
  summarize(r_obs = n())

# Try bin size of...
data.frame(
  t = hours
) %>%
  mutate(label = cut_interval(t, length = 150)) %>%
  group_by(label, .drop = FALSE) %>%
  summarize(r_obs = n())
