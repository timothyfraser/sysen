#’ @name lesson_12

# Load packages, to get our dplyr, ggplot, tibble, and readr functions
library(dplyr)
library(broom) # get our tidy() function

# Read data!
donuts = read_csv("workshops/donuts.csv")


# Having trouble reading in your data?
# You can also use this code:
donuts = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Convert type to factor, where treatment group b is first
donuts2 = donuts %>%
  mutate(type = factor(type, levels = c("b", "a")))




donuts %>% glimpse()

donuts %>% group_by(baker) %>% count()

m = donuts %>% lm(formula = tastiness ~ baker)

m %>% broom::tidy()
m$coefficients

m %>%
  broom::tidy() %>%
  mutate(t = (estimate - 0) / std.error)

# pt(q = 7.20, df = 47, lower.tail = FALSE)  / 2
m %>% summary()


m %>% 
  broom::tidy(conf.int = 0.95) %>%
  ggplot(mapping = aes(x = term, y = estimate,
                       ymin = conf.low, ymax = conf.high)) +
  geom_linerange() +
  geom_point()


# Let's see a t distribution with 47 degrees of freedom
rt(n = 1000, df = 47) %>% hist()


# Let's get confidence intervals...
m  %>% broom::tidy(conf.int = TRUE) %>%
  filter(term == "bakerMelanie") %>%
  select(term, conf.low)

bind_rows(
  donuts %>% 
    lm(formula = tastiness ~ baker) %>% 
    tidy() %>%
    mutate(model = 1),
  donuts %>%
    lm(formula = tastiness ~ baker + weight) %>% 
    tidy() %>% 
    mutate(model = 2)
) %>%
  group_by(model) %>%
  filter(term == "bakerMelanie")



donuts %>% 
  mutate(weight = scale(weight),
         lifespan = scale(lifespan)) %>%
  lm(formula = tastiness ~ weight + lifespan + baker)

# As weight increased by 1 standard deviation, 
# tastiness changes by 0.26

# As lifespan increases by 1 standard deviation,
# tastiness changes by -0.06








# 

donuts = read_csv("workshops/donuts.csv")

donuts %>% glimpse()


# Tidy long format
long = donuts %>% 
  group_by(type) %>%
  summarize(xbar = mean(tastiness)) %>%
  mutate(testid = 1)


# Wide matrix
wide = tibble(xbar_a = 2.84, xbar_b = 4.16) %>%
  mutate(dbar = xbar_b - xbar_a)


long %>%
  pivot_wider(id_cols = testid, names_from = type, values_from = xbar) %>%
  mutate(dbar = b - a)

library(tidyr)


long2 = donuts %>% 
  group_by(baker, type) %>%
  summarize(xbar = mean(tastiness)) %>%
  ungroup() %>%
  mutate(testid = c(1,1, 2,2, 3,3)) 

long2 %>%
  pivot_wider(id_cols = c(baker, testid), names_from = type, values_from = xbar) %>%
  mutate(dbar = b - a)


donuts %>%
  select(type, tastiness) %>%
  mutate(tastiness = sample(tastiness, replace = FALSE)) %>%
  group_by(type) %>%
  summarize(xbar = mean(tastiness)) %>%
  summarize(dbar = xbar[type == "b"] - xbar[type == "a"])


mydbar = tibble(reps = 1:1000) %>%
  # Get 1000 identical dataset
  group_by(reps) %>%
  reframe(donuts %>% select(type, tastiness)) %>%
  # We shuffle the quality metric within each dataset
  group_by(reps) %>%
  mutate(tastiness = sample(tastiness, replace = FALSE))  %>%
  # For each rep and type, get mean
  group_by(reps, type) %>%
  summarize(xbar = mean(tastiness)) %>%
  # Get 1000 random differences of means.
  group_by(reps) %>%
  summarize(dbar = xbar[type == "b"] - xbar[type == "a"])


mydbar %>%
  ggplot(mapping = aes(x = dbar)) +
  geom_histogram()

rt(n = 1000, df = 98) %>% hist()


####################################################


