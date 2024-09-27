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
# Example
# set_theme()

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
# water
# ggprocess(x = water$time, y = water$temp, xlab = "Subgroup", ylab = "Metric")


#' @name get_stat_s
#' @title Get Subgroup Statistics
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
get_stat_s = function(x,y){

  # Testing values  
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp;
  
  # Make a data.frame
  data = tibble(x=x,y=y)

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
      df = nw - 1)
  
  output = output %>%
    ungroup() %>%
    # to get between group estimates...
    mutate(
      # Get grand mean
      xbbar = mean(xbar),
      # How to get sigma-short!
      #   we're trying to pool the standard deviation from all these different subgroups
      #   to approximate the average standard deviation
      # sigma_s = sqrt(sum(df * s^2) / sum(df) ),
      sigma_s = sqrt(mean(s^2)),
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
  
  # Testing values  
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp;

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


#dn(n = 12)


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
# stat = bn(n = 12)
# # Statistic of interest
# sbar = 2.5 
# # Lower Control Limit
# sbar * stat$B3
# # Upper control limit
# sbar * stat$B4


#' @name limits_avg
#' @title Get Upper and Lower Control Limits for an Averages Chart, using Control Constants
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `bn()` function
limits_avg = function(x,y){
  # Testing values  
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp;

  # Make a data.frame
  data = tibble(x=x,y=y)
  
  # Get within-group stats
  stat_s = data %>%
    group_by(x) %>%
    summarize(xbar = mean(y),
              s = sd(y),
              nw = n(),
              df = nw - 1) %>%
    ungroup()
  
  # For each different subgroup sample size, calculate control constant A3
  constants = stat_s %>%
    select(nw) %>%
    distinct() %>%
    group_by(nw) %>%
    summarize(A3 =  bn(n = nw, reps = 1e4)$A3   ) %>%
    ungroup()

  # Join in the control constants
  stat_s = stat_s %>% 
    left_join(by = "nw", y = constants)
  
  # Add in sbar  and xbbar
  stat_s = stat_s %>%
    mutate(sbar = sqrt(sum(df * s^2) / sum(df) ),
           xbbar = mean(xbar))
  
  # Calculate upper and lower control limits
  stat_s = stat_s %>%
    mutate(lower = xbbar + A3 * sbar,
           upper = xbbar - A3 * sbar)


  return(stat_s)  
}
# # Example
# water = read_csv("workshops/onsen.csv")
# # You could use the standard error...
# get_stat_s(x = water$time, y = water$temp)
# # Or you could use the control constants to approximate the 3 sigma range.
# limits_avg(x = water$time, y = water$temp)





#' @name limits_s
#' @title Get Upper and Lower Control Limits for a Standard Deviation Chart, using Control Constants
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `bn()` function
limits_s = function(x,y){
  # Testing values  
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp;
  
  # Make a data.frame
  data = tibble(x=x,y=y)
  
  # Get within-group stats
  stat_s = data %>%
    group_by(x) %>%
    summarize(s = sd(y),
              nw = n(),
              df = nw - 1) %>%
    ungroup()
  
  # For each different subgroup sample size, calculate control constants
  constants = stat_s %>%
    select(nw) %>%
    distinct() %>%
    group_by(nw) %>%
    summarize( bn(n = nw, reps = 1e4) ) %>%
    ungroup()
  
  # Join in the control constants
  stat_s = stat_s %>% 
    left_join(by = "nw", y = constants)
  
  # Add in sbar
  stat_s = stat_s %>%
    mutate(sbar = sqrt(sum(df * s^2) / sum(df) ) )
  
  # Calculate upper and lower control limits
  stat_s = stat_s %>%
    mutate(lower = B3 * sbar,
           upper = B4 * sbar)
  
  
  return(stat_s)  
}
# # Example
# water = read_csv("workshops/onsen.csv")
# # You can use the control constants to approximate the 3 sigma range.
# limits_s(x = water$time, y = water$temp)



#' @name limits_r
#' @title Get Upper and Lower Control Limits for a Range Chart, using Control Constants
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `dn()` function
limits_r = function(x,y){
  # Testing values  
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp;
  
  # Make a data.frame
  data = tibble(x=x,y=y)
  
  # Get within-group stats
  stat_s = data %>%
    group_by(x) %>%
    summarize(r = max(y) - min(y),
              nw = n(),
              df = nw - 1) %>%
    ungroup()
  
  # For each different subgroup sample size, calculate control constants
  constants = stat_s %>%
    select(nw) %>%
    distinct() %>%
    group_by(nw) %>%
    summarize( dn(n = nw, reps = 1e4) ) %>%
    ungroup()
  
  # Join in the control constants
  stat_s = stat_s %>% 
    left_join(by = "nw", y = constants)
  
  # Add in rbar
  stat_s = stat_s %>%
    mutate(rbar = mean(r) )

  # Calculate upper and lower control limits
  stat_s = stat_s %>%
    mutate(lower = D3 * rbar,
           upper = D4 * rbar)
  
  return(stat_s)  
}
# # Example
# water = read_csv("workshops/onsen.csv")
# # You can use the control constants to approximate the 3 sigma range.
# limits_r(x = water$time, y = water$temp)



#' @name limits_mr
#' @title Get Upper and Lower Control Limits for a Moving Range Chart, using Control Constants
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `dn()` function
limits_mr = function(x,y){
  # Testing values  
  # Suppose we sample just the first out of each our months.
  # water = read_csv("workshops/onsen.csv") %>% filter(id %in% c(1, 21, 41, 61, 81, 101, 121, 141))
  # x = water$time; y = water$temp;
  
  # Make a data.frame
  data = tibble(x=x,y=y)
  
  # Convert our original dataset into a set of moving ranges
  data2 = data %>%
    reframe(
      x = x[-1],
      # get moving range
      mr = y %>% diff() %>% abs()
    )
  
  # Estimate d2 when subgroup size n = 1
  d2 = rnorm(n = 10000, mean = 0, sd = 1) %>% diff() %>% abs() %>% mean()
  
  stat = data2 %>%
    # Get average moving range
    mutate(
      mrbar = mean(mr),
      # Get d2 constant
      d2 = d2,
      # approximate sigma s
      sigma_s = mrbar / d2,
      # Our subgroup size was 1, right?
      n = 1,
      # so this means sigma_s just equals the standard error here
      se = sigma_s / sqrt(n),
      # compute upper 3-se bound
      upper = mrbar + 3 * se,
      # and lower ALWAYS equals 0 for moving range
      lower = 0)
  
  return(stat)  
}
# Example
# You can use the control constants to approximate the 3 sigma range.
# water = read_csv("workshops/onsen.csv") %>% filter(id %in% c(1, 21, 41, 61, 81, 101, 121, 141))
# limits_mr(x = water$time, y = water$temp)


#' @name ggxbar
#' @title Average Control Chart with ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `get_stat_t()`, `get_stat_s()`, `get_labels()` functions
ggxbar = function(x,y, xlab = "Time (Subgroups)", ylab = "Average"){
  
  # Testing values 
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp; xlab = "Time (Subgroups)"; ylab = "Average"
  data = tibble(x = x, y = y)
  
  # Get statistics for each subgroup
  stat_s = get_stat_s(x = data$x, y = data$y)

  # Generate labels
  labels = stat_s %>%
    reframe(
      x = c(max(x), max(x), max(x)),
      type = c("xbbar", "upper", "lower"),
      name = c("xbbar", "+3 s", "-3 s"),
      value = c(mean(xbbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
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
    labs(x = xlab, y = ylab, subtitle = "Average Chart")

  return(gg)
}


# Example
# water = read_csv("workshops/onsen.csv")
# ggxbar(x = water$time, y = water$ph, xlab = "Time (Subgroups)", ylab = "Average pH")


#' @name ggs
#' @title Standard Deviation Chart with ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `limits_s()`, `get_stat_t()`, `bn()` functions
ggs = function(x,y, xlab = "Time (Subgroups)", ylab = "Standard Deviation"){
  
  # Testing values 
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp; xlab = "Time (Subgroups)"; ylab = "Standard Deviation"

  # Make data.frame of input vectors
  data = tibble(x = x, y = y)
  
  # Get subgroup statistics, with UCL and LCL for standard deviation
  stat_s = limits_s(x = data$x, y = data$y)

  # Get overall (total) statistics
  stat_t = get_stat_t(x = data$x, y = data$y)

  # Get labels
  labels = stat_s %>%
    reframe(
      x = c(max(x), max(x), max(x)),
      type = c("sbar", "upper", "lower"),
      name = c("sbar", "+3 s", "-3 s"),
      value = c(mean(sbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
  # Make visual
  gg = ggplot() +
    geom_hline(data = stat_t, mapping = aes(yintercept = sbar), color = "lightgrey") +
    geom_ribbon(data = stat_s, mapping = aes(x = x, ymin = lower, ymax = upper),
                fill = "steelblue", alpha = 0.2) +
    geom_line(data = stat_s, mapping = aes(x = x, y = s), linewidth = 1) +
    geom_point(data = stat_s, mapping = aes(x = x, y = s), size = 5) +
    geom_label(data = labels, mapping = aes(x = x, y = value, label = text),
               hjust = 1) + # horizontally justify labels
    labs(x = xlab, y = ylab, subtitle = "Standard Deviation Chart")
  
  return(gg)
}
# water = read_csv("workshops/onsen.csv");
# ggs(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Standard Deviation")




#' @name ggr
#' @title Range Chart with ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `limits_r()`, `dn()`, `get_stat_t()` functions
ggr = function(x,y, xlab = "Time (Subgroups)", ylab = "Range"){
  
  # Testing values 
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp; xlab = "Time (Subgroups)"; ylab = "Range"
  
  # Make data.frame of input vectors
  data = tibble(x = x, y = y)
  
  # Get subgroup statistics, with UCL and LCL for standard deviation
  stat_s = limits_r(x = data$x, y = data$y)
  
  # Get overall (total) statistics
  stat_t = get_stat_t(x = data$x, y = data$y)
  
  # Get labels
  labels = stat_s %>%
    reframe(
      x = c(max(x), max(x), max(x)),
      type = c("rbar", "upper", "lower"),
      name = c("rbar", "+3 s", "-3 s"),
      value = c(mean(rbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
  # Make visual
  gg = ggplot() +
    geom_hline(data = stat_t, mapping = aes(yintercept = rbar), color = "lightgrey") +
    geom_ribbon(data = stat_s, mapping = aes(x = x, ymin = lower, ymax = upper),
                fill = "steelblue", alpha = 0.2) +
    geom_line(data = stat_s, mapping = aes(x = x, y = r), linewidth = 1) +
    geom_point(data = stat_s, mapping = aes(x = x, y = r), size = 5) +
    geom_label(data = labels, mapping = aes(x = x, y = value, label = text),
               hjust = 1) + # horizontally justify labels
    labs(x = xlab, y = ylab, subtitle = "Range Chart")
  
  
  return(gg)
}

# Example
# water = read_csv("workshops/onsen.csv");
# ggr(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Range")

#' @name ggmr
#' @title Range Chart with ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `limits_mr()`, `dn()` functions
ggmr = function(x,y, xlab = "Time (Subgroups)", ylab = "Moving Range"){
  
  # Testing values  
  # Suppose we sample just the first out of each our months.
  # water = read_csv("workshops/onsen.csv") %>% filter(id %in% c(1, 21, 41, 61, 81, 101, 121, 141))
  # x = water$time; y = water$temp;
  
  # Make data.frame of input vectors
  data = tibble(x = x, y = y)
  
  # Obtain moving range
  data2 = data %>% 
    reframe(x = x[-1],
            mr = y %>% diff() %>% abs())
  
  # Get subgroup statistics, with UCL and LCL for moving range
  stat_s = limits_mr(x = data$x, y = data$y)
  
  
  # Get labels
  labels = stat_s %>%
    reframe(
      x = c(max(x), max(x), max(x)),
      type = c("mrbar", "upper", "lower"),
      name = c("mrbar", "+3 s", "-3 s"),
      value = c(mean(mrbar), max(upper), min(lower))
    ) %>%
    mutate(value = round(value, 2)) %>%
    mutate(text = paste0(name, " = ", value))
  
  # Get one value for grand moving range
  stat_t = stat_s %>%
    summarize(mrbar = mr %>% mean())
  
  # Make visual
  gg = ggplot() +
    geom_hline(data = stat_t, mapping = aes(yintercept = mrbar), color = "lightgrey") +
    geom_ribbon(data = stat_s, mapping = aes(x = x, ymin = lower, ymax = upper),
                fill = "steelblue", alpha = 0.2) + 
    geom_line(data = data2, mapping = aes(x = x, y = mr), linewidth = 1) +
    geom_point(data = stat_s, mapping = aes(x = x, y = mr), size = 5) + 
    geom_label(data = labels, mapping = aes(x = x, y = value, label = text),
               hjust = 1) + # horizontally justify labels
    labs(x = xlab, y = ylab, subtitle = "Moving Range Chart")
  
  return(gg)
}

# Example
# water = read_csv("workshops/onsen.csv") %>% filter(id %in% c(1, 21, 41, 61, 81, 101, 121, 141))
# ggmr(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Moving Range")


#' @name ggp
#' @title Fraction Defective (p) Chart in ggplot
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


#' @name ggnp
#' @title Number of Defects (np) Chart in ggplot
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

#' @name ggu
#' @title Defects per Product (u) Chart in ggplot
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

