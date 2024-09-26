#' @name functions_process_control.R
#' @title Functions for Statistical Process Control
#' @description 
#' Below are several functions that you can use or customize to perform statistical process control.

library(dplyr) # for data wrangling
library(readr) # for reading in data
library(ggplot2) # for visualization
library(ggpubr) # for combining plots
library(moments) # for skewness and kurtosis 

#' @name set_theme
#' @title Set Theme of All ggplots
set_theme = function(){
  
  # By running theme_set()
  theme_set(
    # we tell ggplot to give EVERY plot this theme
    theme_classic(base_size = 14) +
      # With these theme traits, including
      theme(
        # Putting the legend on the bottom, if applicable
        legend.position = "bottom",
        # horizontally justify plot subtitle and caption in center
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        plot.caption = element_text(hjust = 0.5),
        # Getting rid of busy axis ticks
        axis.ticks = element_blank(),
        # Getting rid of busy axis lines
        axis.line = element_blank(),
        # Surrounding the plot in a nice grey border
        panel.border = element_rect(fill = NA, color = "grey"),
        # Remove the right margin, for easy joining of plots
        plot.margin = margin(r = 0)
      )
  )
  
}

#' @name describe
#' @title Describe a vector `x`
#' @param x [numeric] a numeric vector of observed metric values
describe = function(x){
  # Put our vector x in a tibble
  tibble(x) %>%
    # Calculate summary statistics
    summarize(
      mean = mean(x, na.rm = TRUE),
      sd = sd(x, na.rm = TRUE),
      # We'll use the moments package for these two
      skew = skewness(x, na.rm = TRUE),
      kurtosis = kurtosis(x, na.rm = TRUE)) %>%
    # Let's add a caption, that compiles  all these statistics  
    mutate(
      # We'll paste() the following together
      caption = paste(
        # Listing the name of each stat, then reporting its value and rounding it, then separating with " | "
        "Process Mean: ", mean %>% round(2), " | ", 
        "SD: ", sd %>% round(2), " | ",
        "Skewness: ", skew %>% round(2), " | ",
        "Kurtosis: ", kurtosis %>% round(2), 
        # Then make sure no extra spaces separate each item
        sep = "")) %>%
    return()
}

# example 
# describe(x = rnorm(1000,0,1))


#' @name ggprocess
#' @title Make a Process Overview Diagram in ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @param xlab [string] label for x-axis.
#' @param ylab [string] label for y-axis.
ggprocess = function(x, y, xlab = "Subgroup", ylab = "Metric"){
  
  # Testing values
  # water = read_csv("workshops/onsen.csv")
  # x = water$time; y = water$temp; xlab = "Subgroup"; ylab = "Metric"
  
  # Convert vectors and bundle as data.frame
  data = tibble(x = x, y = y)  
  
  # Get grand mean lines
  stat = data %>% summarize(mu = mean(y))
  
  #describe data
  tab = describe(data$y)
  
  # Visualize data
  g1 = ggplot() +
    # Plot grand mean
    geom_hline(data = stat, mapping = aes(yintercept = mu), color = "lightgrey", linewidth = 3) +
    # Plot raw data points
    geom_jitter(data = data, mapping = aes(x = x, y = y), height = 0, width = 0.25) +
    geom_boxplot(data = data, mapping = aes(x = x, y = y, group = x)) +
    # Add descriptive stats in the caption
    labs(x = xlab, y = ylab, subtitle = "Process Overview", caption = tab$caption)
  
  # Make the histogram  
  g2 = ggplot() +
    geom_histogram(data = data, mapping = aes(x = y), bins = 15, color = "white", fill = "grey") +
    theme_void() + # clear the theme
    coord_flip() # tilt on its side
  
  # Then bind them together into 1 plot, horizontally aligned.
  output = ggarrange(plotlist = list(g1,g2), nrow = 1, ncol = 2, widths = c(4,1), align = "h")
    
  return(output)
}

# Example
# water = read_csv("workshops/onsen.csv")
# ggprocess(x = water$time, y = water$temp, xlab = "Subgroup", ylab = "Metric")


#' @name get_stat_s
#' @title Get Subgroup Statistics
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
get_stat_s = function(x,y){
  
  # Calculate sigma t direct
  sigma_t = sd(y)
  
  # Let’s calculate sigma_s and sigma_t!
  output = data %>%
    # for each subgroup x
    group_by(x) %>%
    # Calculate...
    summarize(
      # within-group mean
      xbar = mean(y),
      # within-group range
      r = max(y) - min(y),
      # within-group standard deviation
      s = sd(y),
      # within-group sample size
      nw = n(),
      # within-group degrees of freedom
      df = nw - 1) %>%
    ungroup() %>%
    # to get between group estimates...
    mutate(
      # Get grand mean
      xbbar = mean(xbar),
      # How to get sigma-short!
      #   we're trying to pool the standard deviation from all these different subgroups
      #   to approximate the average standard deviation
      sigma_s = sqrt(sum(df * s^2) / sum(df) ),
      #    sigma_s = sqrt(mean(s^2))
      sigma_t = sigma_t,
      se = sigma_s / sqrt(nw),
      upper = mean(xbar) + 3*se,
      lower = mean(xbar) - 3*se
    )
  return(output)
}
# Example
# water = read_csv("workshops/onsen.csv")
# get_stat_s(x = water$time, y = water$temp)


#' @name get_stat_t
#' @title Get Total Statistics
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
get_stat_t = function(x,y){
  
  # Make a data.frame
  data = tibble(x = x, y = y)
  
  # Get total standard deviation
  sigma_t = sd(y)
  
  # Get statistics for each subgroup
  stat_s = data %>%
    # for each subgroup x
    group_by(x) %>%
    # Calculate...
    summarize(
      # within-group mean
      xbar = mean(y),
      # within-group range
      r = max(y) - min(y),
      # within-group standard deviation
      s = sd(y),
      # within-group sample size
      nw = n(),
      # within-group degrees of freedom
      df = nw - 1) %>%
    ungroup()
  
  
  # Now calculate one row of total statistics
  output = stat_s %>%
    summarize(
      # average average
      xbbar = mean(xbar),
      # average range
      rbar = mean(r),
      # average standard deviation
      sbar = mean(s),
      # average within-group standard deviation
      sigma_s = sqrt(sum(s^2) / sum(nw) ),
      # overall standard deviation
      sigma_t = sigma_t,
      # total sample size
      n = sum(nw)
    )
  
  return(output)
}
# Example
# water = read_csv("workshops/onsen.csv")
# get_stat_t(x = water$time, y = water$temp)



#' @name get_labels
#' @title Get Labels from Subgroup Statistics
#' @param data [data.frame] output of get_stat_s()
get_labels = function(data){
  
  stat_s %>%
    reframe(
      x = c(max(x), max(x), max(x)),
      type = c("xbbar", "upper", "lower"),
      name = c("mean", "+3 s", "-3 s"),
      value = c(mean(xbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))

}

# Example
# water = read_csv("workshops/onsen.csv")
# stat_s = get_stat_s(x = water$time, y = water$temp)
# get_labels(data = stat_s)


#' @name ggavgsd
#' @title Average and Standard Deviation Control Chart
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
ggavgsd = function(x,y, xlab = "Time (Subgroups)", ylab = "Average"){
  
  data = tibble(x = x, y = y)
  
  # Get statistics for each subgroup
  stat_s = get_stat_s(x = data$x, y = data$y)

  # Generate labels
  labels = get_labels(data = stat_s)
  
  # Get overall statistics
  stat_t = get_stat_t(x = x, y = y)
  
  # Generate plot
  gg = ggplot() +
    geom_hline(data = stat_t, mapping = aes(yintercept = xbbar), color = "lightgrey") +
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = x, ymin = lower, ymax = upper),
      fill = "steelblue", alpha = 0.2) +
    geom_line(
      data = stat_s,
      mapping = aes(x = x, y = xbar), size = 1
    ) +
    geom_point(
      data = stat_s,
      mapping = aes(x = x, y = xbar), size = 5
    ) +
    geom_label(
      data = labels,
      mapping = aes(x = x, y = value, label = text),
      hjust = 1 # horizontally justify the labels
    ) +
    labs(x = xlab, y = ylab, subtitle = "Average and Standard Deviation Charts")
  
  return(gg)
}

# Example
# water = read_csv("workshops/onsen.csv")
# ggavgsd(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Average Temperature")






# How do we approximate sigma-short?
dn = function(n = 12, reps = 1e4){
  # For 10,0000 reps
  tibble(rep = 1:reps) %>%
    # For each rep,
    group_by(rep) %>%
    # Simulate the ranges of n values
    summarize(r = rnorm(n = n, mean = 0, sd = 1) %>% range() %>% diff() %>% abs()) %>%
    ungroup() %>%
    # And calculate...
    summarize(
      # Mean range
      d2 = mean(r),
      # standard deviation of ranges
      d3 = sd(r),
      # and constants for obtaining lower and upper ci for rbar
      D3 = 1 - 3*(d3/d2), # sometimes written D3
      D4 = 1 + 3*(d3/d2), # sometimes written D4
      # Sometimes D3 goes negative; we need to bound it at zero
      D3 = if_else(D3 < 0, true = 0, false = D3) ) %>%
    return()
}


dn(n = 12)


#Let's write a function bn() to calculate our B3 and B4 statistics for any subgroup size n
bn = function(n, reps = 1e4){
  tibble(rep = 1:reps) %>%
    group_by(rep) %>%
    summarize(s = rnorm(n, mean = 0, sd = 1) %>% sd()) %>%
    summarize(b2 = mean(s), 
              b3 = sd(s),
              C4 = b2, # this is sometimes called C4
              A3 = 3 / (b2 * sqrt( n  )),
              B3 = 1 - 3 * b3/b2,
              B4 = 1 + 3 * b3/b2,
              # bound B3 at 0, since we can't have a standard deviation below 0
              B3 = if_else(B3 < 0, true = 0, false = B3)) %>%
    return()
}

# For a subgroup of size 12
stat = bn(n = 12)
# Statistic of interest
sbar = 2.5 
# Lower Control Limit
sbar * stat$B3
# Upper control limit
sbar * stat$B4
