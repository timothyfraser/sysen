#’ @name lesson_12

# Load packages, to get our dplyr, ggplot, tibble, and readr functions
library(dplyr)
library(broom) # get our tidy() function

# Read data!
donuts = read_csv("workshops/donuts.csv")

donuts %>% glimpse()
# Having trouble reading in your data?
# You can also use this code:
donuts = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")


donuts

aov(tastiness ~ baker, data = donuts)

oneway.test(tastiness ~ baker, data = donuts, var.equal = TRUE)
# tastiness varies significantly between bakers

lm(formula = tastiness ~ baker, data = donuts) %>%
  glance()



donuts3 = donuts %>%
  filter(baker %in% c("Craig", "Melanie"))


t.test(tastiness ~ baker, data = donuts3, var.equal = TRUE) %>%
  tidy()



donuts3 = donuts3 %>%
  mutate(baker = factor(baker, levels = c("Melanie", "Craig")))

t.test(tastiness ~ baker, data = donuts3, var.equal = TRUE) %>%
  tidy()



donuts3 %>%
  mutate(baker = factor(baker, levels = c("Melanie", "Craig"))) %>%
  t.test(tastiness ~ baker, data = ., var.equal = TRUE) %>%
  tidy()

  

# Convert type to factor, where treatment group b is first
donuts2 = donuts %>%
  mutate(type = factor(type, levels = c("b", "a")))




# donuts$tastiness %>% unique()





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


long

long %>%
  tidyr::pivot_wider(id_cols = testid, names_from = type, values_from = xbar) %>%
  mutate(dbar = b - a)

library(tidyr)


# T-test Examples ##########################################################

donuts2 = donuts %>%
  mutate(type = factor(type, levels = c("a", "b")))


donuts2 %>%
  # Run our t-test using the data from donuts, then tidy() it into a data.frame
  summarize(t.test(weight ~ type, var.equal = TRUE) %>% tidy()) %>%
  glimpse()


donuts2 %>%
  lm(formula = weight ~ type) %>%
  broom::tidy()

donuts2 %>%
  group_by(type) %>%
  summarize(xbar = mean(weight))

# There's a -3.4 gram difference (95% CI is -1.8 ~ -4.9, p < 0.001)
# What if we knew that 1 gram costs us $0.01
# What if we knew that we're going to produce 50,000 donuts
# 

dbar = -3.4
dbar_lower = -1.8
n = 50000
cost_per_gram = 0.01
dbar * cost_per_gram * n



donuts %>%
  group_by(type) %>%
  summarize(var = var(weight))



donuts2 %>%
  summarize(t.test(weight ~ type, var.equal = FALSE) %>% tidy())  




ggplot() +
  geom_violin(data = donuts2, mapping = aes(x = type, y = weight)) +
  geom_jitter(data = donuts2, mapping = aes(x = type, y = weight)) 


ggplot() +
  geom_boxplot(data = donuts2, mapping = aes(x = type, y = weight)) +
  geom_jitter(data = donuts2, mapping = aes(x = type, y = weight)) 























donuts %>% glimpse()


donuts %>% group_by(baker) %>% count()


m = donuts %>% lm(formula = tastiness ~ baker)

m


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














# Permutation Test Examples ##################################################
# Load packages, to get our dplyr, ggplot, tibble, and readr functions
library(dplyr)
library(broom) # get our tidy() function

# Read data!
donuts = read_csv("workshops/donuts.csv")


obs = donuts %>%
  summarize(dbar = mean(tastiness[baker == "Melanie"])  - mean(tastiness[baker == "Craig"]))

obs$dbar

donuts %>%
  mutate(tastiness = sample(tastiness,size = n(), replace = FALSE) ) 

mydbar = tibble(reps = 1:1000) %>%
  # Get 1000 identical dataset
  group_by(reps) %>%
  reframe(donuts %>% select(baker, tastiness)) %>%
  # We shuffle the quality metric within each dataset
  group_by(reps) %>%
  mutate(tastiness = sample(tastiness, replace = FALSE))  %>%
  # For each rep, get mean
  group_by(reps) %>%
  summarize(dbar = mean(tastiness[baker == "Melanie"])  - mean(tastiness[baker == "Craig"]))


ggplot() +
  geom_histogram(data = mydbar, mapping = aes(x = dbar)) +
  geom_vline(xintercept = obs$dbar)


mean(mydbar$dbar > obs$dbar)





####################################################
# Deprecated content
# rt(n = 1000, df = 98) %>% hist()
# long2 = donuts %>% 
#   group_by(baker, type) %>%
#   summarize(xbar = mean(tastiness)) %>%
#   ungroup() %>%
#   mutate(testid = c(1,1, 2,2, 3,3)) 
# 
# 
# long2 %>%
#   pivot_wider(id_cols = c(baker, testid), names_from = type, values_from = xbar) %>%
#   mutate(dbar = b - a)
# 
# 
# donuts %>%
#   select(type, tastiness) %>%
#   mutate(tastiness = sample(tastiness, replace = FALSE)) %>%
#   group_by(type) %>%
#   summarize(xbar = mean(tastiness)) %>%
#   summarize(dbar = xbar[type == "b"] - xbar[type == "a"])


