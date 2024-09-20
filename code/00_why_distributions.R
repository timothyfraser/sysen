# 00_why_distributions.R


# A quick example summarizing why we use hypothetical distributions

# If we have the observed data, great! Let's use that
hours = c(1000, 2000,3000, 2500, 3200, 500, 3000, 5000, 600, 4000, 3000)
# Make observed density function
dobs = hours %>% density() %>% approxfun()

# If we DON'T have the observed data, we could use exponential.
dexp = function(t, lambda){  lambda * exp(-lambda* t)  }

# Let's get a crap ton of probabilities
dat = tibble(
  t = 1:1000, 
  prob = dexp(t = t, lambda = 0.001), 
  prob2 = dexp(t, lambda = 0.002),
  prob3 = dexp(t, lambda = 0.003),
  prob4 = dobs(t),
  prob5 = dexp(t, lambda = 1 / mean(hours)))

# Key finding: don't use the exponential to model this particular data
# it doesn't look right AT ALL!
ggplot() +
  geom_line(data = dat, mapping = aes(x = t, y = prob)) + 
  geom_line(data = dat, mapping = aes(x = t, y = prob2)) +
  geom_line(data = dat, mapping = aes(x = t, y = prob3))  +
  geom_line(data = dat, mapping = aes(x = t, y = prob4), color = "red") +
  geom_line(data = dat, mapping = aes(x = t, y = prob5), color = "blue")





