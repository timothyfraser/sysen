# 00_p_charts.R

library(dplyr)

# Fraction defection (p) chart
# # of defective items
# has a binomial distribution
# each of the n itmes being tests is being classified
# into 2 categories: defective or not defective
# the probability p of a defective item is constant for every item.

# inventory example
inventory = tribble(
  ~t, ~n, ~x,
  1,  100, 10,
  2,  60, 4,
  3, 84, 7,
  4, 122, 12,
  5, 100, 6,
  6, 50, 4,
  7, 67, 5,
  8, 100, 5,
  9, 115, 9,
  10, 75, 3,
  11, 82, 6,
  12, 100, 7,
  13, 130, 7,
  14, 67, 5,
  15, 45, 2,
  16, 100, 4,
  17, 134, 8
) %>%
  readr::write_csv("workshops/inventory.csv")

bulbs = tribble(
  ~n, ~x,
  200, 4,
  200, 8,
  200, 6,
  200, 6,
  200, 4,
  200, 8,
  200, 2,
  200, 1,
  200, 9,
  200, 6,
  200, 8, 
  200, 1,
  200, 2,
  200, 9,
  200, 4,
  200, 3,
  200, 9,
  200, 6,
  200, 2,
  200, 7
) %>% mutate(t = 1:n()) %>%
  select(t,x,n) %>%
  write_csv("workshops/bulbs.csv")



# Defect per product (u) chart
# Assumes # of defects per product follows Poisson Distribution

tribble(
  ~t, ~x,
  1, 9,
  2, 7,
  3, 10,
  4, 11,
  5, 7, 
  6, 5,
  7, 9, 
  8, 10, 
  9, 8, 
  10, 13,
  
  11, 8,
  12, 3,
  13, 4,
  14, 14,
  15, 10,
  16, 12,
  17, 15,
  18, 9,
  19, 6,
  20, 14,
  
  21, 9,
  22, 15,
  23, 11,
  24, 8,
  25, 4,
  26, 2,
  27, 8,
  28, 5,
  29, 3,
  30, 2
) %>%
  readr::write_csv("workshops/accidents.csv")



# If X represents the # of defective items in n items,
# then the probability of finding x defective in n items is:
# px = function(x,n,p){factorial(n) / (factorial(x)*factorial(n - x)) * p^(x)*(1 - p)^(n-x) }

# px(x = 5, n = 150, p = 0.50)


ggp = function(t, x, n, xlab = "Time (Subgroup)", ylab = "Fraction Defective"){
  
  # Testing values
  # inventory = read_csv("workshops/inventory.csv")
  # t = inventory$t; x = inventory$x; n = inventory$n; xlab = "Time (Subgroup)"; ylab = "Fraction Defective"
  
  # Make a data.frame
  data = tibble(t = t, x = x, n = n)
  
  # Get subgroup statistics
  stat_s = data %>%
    # For each subgroup...
    group_by(t) %>%
    mutate(
      # Get probability 
      p = x / n,
      # Mean number of defective items
      mu = n * p,
      # Standard deviation of defective items
      sigma = sqrt(n*p*(1-p))
    ) %>%
    ungroup()
  
  # Add total traits here
  stat_s = stat_s %>%
    mutate(
      # get total problems and total items
      xsum = sum(x),
      nsum = sum(n),
      # calculate centerline
      pbar = xsum / nsum,
      # calculate standard deviation with binomial assumptions
      se = sqrt(pbar * (1 - pbar) / n),
      # Calculate 3-sigma control limits
      lower = pbar - 3*se,
      upper = pbar + 3*se
    ) %>%
    # Clip the lower estimate at zero or higher
    mutate(lower = if_else(lower < 0, true = 0, false = lower))
  
  # Visualize it
  gg = ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = t, ymin = lower, ymax = upper),
      fill = "steelblue", alpha = 0.2) +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = pbar),
      linewidth = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = t, y = p)) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = t, y = p)) +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Fraction Defective (p) Chart")
  
  # Return result
  return(gg)
}

# Testing values
# inv = read_csv("workshops/inventory.csv")
# ggp(t = inv$t, x = inv$x, n = inv$n, xlab = "Time (Subgroups)", y = "Fraction Defective")


ggnp = function(t,x,n, xlab = "Time (Subgroups)", ylab = "Number of Defectives (np)"){
  
  # Testing values
  # inv = read_csv("workshops/inventory.csv")
  # t = inv$t; x = inv$x; n = inv$n;  xlab = "Time (Subgroups)"; ylab = "Number of Defective (np)"
  
  # Make a data.frame
  data = tibble(t = t, x = x, n = n)
  
  # Get subgroup statistics
  stat_s = data %>%
    # For each subgroup...
    group_by(t) %>%
    mutate(
      # Get probability 
      p = x / n,
      # Mean number of defective items
      np = n * p
    ) %>%
    ungroup()
  
  
  # Add total traits here
  stat_s = stat_s %>%
    mutate(
      # get total problems and total items
      xsum = sum(x),
      nsum = sum(n),
      # calculate centerline
      npbar = sum(n * p)/n(),
      pbar = sum(n*p)/sum(n),
      # calculate standard error
      se = sqrt(npbar * (1 - pbar)),
      # Calculate 3-sigma control limits
      lower = npbar - 3*se,
      upper = npbar + 3*se
    ) %>%
    # Clip the lower estimate at zero or higher
    mutate(lower = if_else(lower < 0, true = 0, false = lower))
  
  labels = stat_s %>%
    reframe(
      t = c(max(t), max(t), max(t)),
      type = c("npbar", "upper", "lower"),
      name = c("npbar", "+3 s", "-3 s"),
      value = c(mean(npbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
  
  
  # Visualize it
  gg = ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = t, ymin = lower, ymax = upper),
      fill = "steelblue", alpha = 0.2) +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = npbar),
      linewidth = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = t, y = np)) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = t, y = np)) +
    # Add text
    geom_label(data = labels, mapping = aes(x = t, y = value, label = text), hjust = 1) +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Mean Defective (np) Chart")
  
  return(gg)
}

# Example
# inv = read_csv("workshops/inventory.csv")
# ggnp(t = inv$t, x = inv$x, n = inv$n, xlab = "Time (Subgroups)", y = "Number of Defectives")

# Example
# bulbs = read_csv("workshops/bulbs.csv")
# ggnp(t = bulbs$t, x = bulbs$x, n = bulbs$n, xlab = "Time (Subgroups)", y = "Number of Defectives")

# More info here:
# https://sixsigmastudyguide.com/attribute-chart-np-chart/


ggu = function(t,x, xlab = "Time (Subgroups)", ylab = "Number of Defects (u)"){
  
  data = tibble(t = t, x = x)
  stat_s = data %>%
    group_by(t) %>%
    mutate(
      # get total accidents per time stamp
      u = sum(x),
      # within-group sample size
      nw = n()
    ) %>%
    ungroup() %>%
    # Calculate centerline
    mutate(ubar = sum(u)/ sum(nw)) %>%
    mutate(se = sqrt(ubar / nw)) %>%
    mutate(lower = ubar - 3*se,
           upper = ubar + 3*se) %>%
    # Curb lower to be no lower than 0
    mutate(lower = if_else(lower < 0, 0, lower))
  
  labels = stat_s %>%
    reframe(
      t = c(max(t), max(t), max(t)),
      type = c("ubar", "upper", "lower"),
      name = c("ubar", "+3 s", "-3 s"),
      value = c(mean(ubar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
  # Visualize
  gg = ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = t, ymin = lower, ymax = upper),
      fill = "steelblue", alpha = 0.2)  +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = ubar),
      linewidth = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = t, y = u)) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = t, y = u)) +
    # Add text
    geom_label(data = labels, mapping = aes(x = t, y = value, label = text), hjust = 1) +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Number of Defects (u) Chart")
  
  
  return(gg)
}
# Example
# acc = read_csv("workshops/accidents.csv")
# ggu(t = acc$t, x = acc$x, xlab = "Time", ylab = "Number of Defects")
