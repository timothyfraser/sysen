# 12_workshop.R

library(dplyr)
library(broom)


# Unpaired t-tests ###############################################

data = tibble(
  method = c("A", "A", "A", "A", "A", "A", "A", "A", "A", "A", 
              "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"),
  yield = c(89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
            84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5)  )

# T-test assuming equal variance (unpaired)
t.test(formula = yield ~ method, data = data, var.equal = TRUE)


# T-test not assuming equal variance
t.test(formula = yield ~ method, data = data, var.equal = FALSE)


# Variance F-tests ################################

# How different are the variances?
data %>%
  group_by(method) %>%
  summarize(var = var(yield))

# Is that difference significant?
# F test to compare two variances. 
var.test(formula = yield ~ method, data = data)
# Are they significantly different? (No --> p = 0.5049)


# How would we do this in a 'tidy' way?

# Use broom's tidy() function to return result as a data.frame
data %>%
  summarize(
    t.test(formula = yield ~ method, var.equal = TRUE) %>% broom::tidy())

# 'statistic' is the t-statistic.
# 'p.value' is the p-value of the t-statistic
# 'estimate' is the difference of means.
# 'conf.low' and 'conf.high' are the 95% confidence intervals 
#      around the difference of means.





# Paired t-tests ##################################################

# When data comes in pairs, like this, we use paired t-tests.
data2 = tibble(
  yield_a = c(89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5),
  yield_b = c(84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5)  
)


# Basic method for paired t-test
t.test(data2$yield_a, data2$yield_b, paired = TRUE, var.equal = TRUE)

# Or, do it in a data.frame friendly way like this:
data2 %>%
  summarize(
    t.test(yield_a, yield_b,  paired = TRUE, var.equal = TRUE) %>% tidy())



# Permutation Test #################################################

# How would we do a permutation test of the difference of means?


# Let's do 1 permutation together.

# Randomly shuffle the outcomes across groups
data %>%
  mutate(yield = sample(yield, size = n(), replace = FALSE))

# Get back the means for A and B, and the difference
data %>%
  mutate(yield = sample(yield, size = n(), replace = FALSE)) %>%
  summarize(
    xbar_a = mean( yield[method == "A"] ),
    xbar_b = mean( yield[method == "B"]),
    dbar = xbar_a - xbar_b
  )


# Let's try it 1000 times!

# Get the dataset, 1000 times
tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(data)


# Shuffle the outcome for each replicated dataset...
tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(data) %>%
  group_by(rep) %>%
  mutate(yield = sample(yield, size = n(), replace = FALSE))


# Do it all!
perms = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(data) %>%
  group_by(rep) %>%
  mutate(yield = sample(yield, size = n(), replace = FALSE)) %>%
  group_by(rep) %>%
  summarize(
    xbar_a = mean( yield[method == "A"] ),
    xbar_b = mean( yield[method == "B"]),
    dbar = xbar_a - xbar_b
  )
perms

# Get the observed difference of means
obs = data %>%
  summarize(
    xbar_a = mean( yield[method == "A"] ),
    xbar_b = mean( yield[method == "B"]),
    dbar = xbar_a - xbar_b
  )


# Now, what percentage of random stats were greater than the observed?
# That's our p-value!

# 1-tailed test
mean(perms$dbar >= obs$dbar)

# 2-tailed test --> turn all dbars positive
mean( abs(perms$dbar) >= abs(obs$dbar) )


# Or in a tidy way...
perms %>%
  summarize(
    estimate = obs$dbar,
    p_value = mean( abs(dbar) >= abs(estimate))
  )

# Visualize it!


ggplot() +
  geom_histogram(data = perms, mapping = aes(x = dbar), fill = "dodgerblue", color = "white") +
  geom_vline(data = obs, mapping = aes(xintercept = dbar)) +
  geom_label(data = obs, mapping = aes(y = 50, x = dbar, label = dbar), hjust = 0)




# ANOVA ###################################################

library(dplyr)
library(readr)
library(broom)

donuts = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Use lm()...
donuts %>%
  summarize(lm(weight ~ baker) %>% glance()) %>%
  select(sigma, statistic, p.value, df)

# Or use aov()...
donuts %>%
  reframe(aov(weight ~ baker) %>% tidy())

# Visualize the difference

ggplot() +
  geom_violin(data = donuts, mapping = aes(x = baker, y = weight)) +
  geom_point(data = donuts, mapping = aes(x = baker, y = weight)) +
  geom_point(
    data = donuts %>% group_by(baker) %>% summarize(xbar = mean(weight)), 
    mapping = aes(x = baker, y = xbar), color = "dodgerblue", size = 5) +
  geom_hline(yintercept = mean(donuts$weight), color = "dodgerblue" ) +
  coord_flip()


# Unequal Variances #####################################

# Are the variances of my 3+ groups significantly different?
# Homogeneity of Variance - Barlett's test for K^2
bartlett.test(weight ~ baker, data = donuts)

# K-squared is a ratio showing how different are the variances, from 0 to infinity.
# If K-squared is not significant, the differences are not significant.

# Looks like the differences in variance are quite significant.
# Best **not** to assume equal variance.

# You can do an ANOVA without the equal variance assumption using oneway.test()
oneway.test(weight ~ baker, data = donuts, var.equal = FALSE)

donuts %>%
  summarize(oneway.test(weight ~ baker, data = donuts, var.equal = FALSE) %>% tidy())
