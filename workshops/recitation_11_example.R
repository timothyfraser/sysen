# recitation_11_example.R
# Tim Fraser, Fall 2022

# Load packages
library(tidyverse)
library(broom)

# Step 1
bg = "https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/boston_block_groups.csv" %>%
  read_csv()

# Step 2
bg %>%
  lm(formula = heat ~ area) %>%
  tidier()

bg %>%
  lm(formula = heat ~ bike_rate) %>%
  tidy(conf.int = TRUE)



# Step 4 for tidier function (find it in Workshop 11A)
install.packages("gtools")



github_csv = function(file){
  paste("https://raw.githubusercontent.com/", 
        "timothyfraser/sysen/main",   "/", file, sep = "")
}

"workshops/boston_block_groups.csv" %>%
  github_csv() %>%
  read_csv() %>%
  head()

bg = "workshops/boston_block_groups.csv" %>%
  github_csv() %>%
  read_csv()

bg %>% glimpse()


bg %>%
  lm(formula = heat ~ 1)


bg %>%
  lm(formula = heat ~ tree_rate)



bg %>%
  lm(formula = heat ~ tree_rate + pop)

bg %>% glimpse()


bg %>%
  lm(formula = heat ~ tree_rate + pop) %>%
  tidier()



m = bg %>%
  lm(formula = heat ~ tree_rate + pop)   


m %>%
  tidy() %>%
  mutate(t = estimate / std.error) %>%
  select(term, statistic, t)


# Let's write a little tidier function..
tidier = function(model, ci = 0.95, digits = 3){
  model %>% # for a model object
    # get data.frame of coefficients
    # ask for a confidence interval matching the 'ci' above! 
    broom::tidy(conf.int = TRUE, conf.level = ci) %>% 
    # And round and relabel them
    summarize(
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



m %>%
  tidier() %>%
  head()


# Let's visualize our confidence intervals using bootstrapping.

# Get 1000 sets of our dataset
boot = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  summarize(bg) %>%
  # For each set/replicate of our dataset,
  # Take a random sample with replacement
  group_by(rep) %>%
  sample_n(size = n(), replace = TRUE) %>%
  # Now for each set, get the model
  group_by(rep) %>%
  summarize(
    lm(formula = heat ~ bike_rate + tree_rate) %>%
      tidy()
  )

# Many many models,
# but each one has slightly different coefficients
boot %>% head()


boot %>%
  filter(term != "(Intercept)") %>%
  ggplot(mapping = aes(x = term, y = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_jitter() +
  coord_flip()

# What percentage of these points cross 0?
# THAT's the p-value
