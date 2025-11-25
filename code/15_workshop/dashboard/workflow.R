# workflow.R
# Example Workflow for Shiny App Dashboard
# Author: Tim Fraser

# pairs with this data: https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/edit?usp=sharing 
# pairs with this form: https://forms.gle/R8axC5GAMXcm7VWd6

# 1. SETUP -------------------------------------------

# Load packages
library(dplyr)
library(readr)

# 2. HELPER FUNCTIONS ---------------------------------------

# check working directory and adjust code below as needed
getwd() 
# Load in helper functions
source("code/15_workshop/dashboard/functions.R")

# 3. WORKFLOW ----------------------------------------------

# Demo the analytical process you're going to perform.

input = list(
  n = 20,
  team = "Front"
)

output = list(
  recent_orders = NULL,
  n_customers = NULL
)

data = get_data(n = input$n)

output$recent_orders = data %>% tail(5)
output$recent_orders

stat1 = get_n(data)
stat1

output$n_customers = stat1$n_customers
output$n_customers




# eventually, it will be this
# output = list(
#   recent_orders = NULL,
#   n_customers = NULL,
#   n_customers_served = NULL,
#   avg_time_to_completion = NULL,
#   viz_by_team = NULL
# )

# And we'll handle these calculations too..
# stat2 = get_time_avg(data)
# stat2
# 
# plot = get_viz_by_team(data, .team = input$team)
