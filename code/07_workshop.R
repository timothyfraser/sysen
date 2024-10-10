
library(dplyr)
library(ggplot2)

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


# try this bin size
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
