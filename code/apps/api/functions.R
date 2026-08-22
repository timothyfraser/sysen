# functions.R
# A script of helper functions to perform your analysis
# Load this into your app/reporter/api of choice and use.

# pairs with this data: https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/edit?usp=sharing 
# pairs with this form: https://forms.gle/R8axC5GAMXcm7VWd6

# 1. SETUP ----------------------------------

# Load any requisite packages
library(dplyr)
library(readr)
library(ggplot2)

# 2. HELPER FUNCTIONS ------------------------

# Let's write some helper functions to procure data and summarize that data

#' @name get_data
#' @description A function to retrieve `n` rows from dataset
#' @param n:int number of most recent orders to retrieve
get_data = function(n){
  n = as.integer(n)  
  
  # Change share link to download link
  url = "https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/export?format=csv"
  
  # Download data
  data = url %>% 
    read_csv(show_col_types = FALSE) %>%
    tail(n) %>%
    select(Timestamp, order_id, task, team, person, done, elapsed) 
  
  return(data)
}


# Test it!
# data = get_data(1000)


#' @name get_n
#' @description Function to get back tallies about orders
#' @param data data.frame of order stage data
get_n = function(data){
  
  # Calculate some performance metrics...
  stat1 = data %>% 
    summarize(
      n_orders = n(),
      n_customers = length(unique(order_id )),
      n_customers_served = length(unique(order_id[done == TRUE] ))
    )
  
  return(stat1)
}

# Try it!
# get_n(data)


#' @name get_time
#' @description Function to get back average completion times
#' @param data data.frame of order stage data
get_time_avg = function(data){
  
  stat2 = data %>%
    filter(done == TRUE) %>%
    group_by(order_id) %>%
    summarize(total_time = sum(elapsed)) %>%
    ungroup() %>%
    summarize(avg_time_to_completion = mean(total_time))
  
  return(stat2)
}

# Try it!
# get_time_avg(data)


#' @name get_time_threshold
#' @description Function to get back n orders within thresholds
#' @param data data.frame of order stage data
#' @param lower:int Order must take more time than this to be counted. Defaults to 0
#' @param upper:int Order must take less time than this to be counted.
get_time_threshold = function(data, upper, lower = 0){
  
  data %>%
    filter(done == TRUE) %>%
    group_by(order_id) %>%
    summarize(total_time = sum(elapsed)) %>%
    ungroup() %>%
    summarize(
      n_orders = sum(total_time > lower & total_time < upper),
      upper = upper,
      lower = lower
    )
}

# Try it!
# get_time_threshold(data, upper = 16)


#' @name get_viz_by_team
#' @description Visualize a bar chart of average time to order completion by person by team
#' @param data data.frame of order stage data
#' @param .team:str Filter by team (eg. "Front")
get_viz_by_team = function(data, .team = "Front"){
  viz1 = data %>%
    filter(team == .team) %>%
    group_by(person) %>%
    summarize(time_avg = mean(elapsed))
  
  ggplot() +
    geom_col(data = viz1, mapping = aes(x = person, y = time_avg)) +
    coord_flip()
}

# Try it!
# get_viz_by_team(data, .team = "Front")
