# app3.R
# Example Plumber REST API - added data processing!
# Author: Tim Fraser

# pairs with these slides: https://docs.google.com/presentation/d/1BBkr_ElCpgXijiTIwyKqxGMNjvhPJx7xEWkjh8YJfSA/edit?usp=sharing
# pairs with this data: https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/edit?usp=sharing 
# pairs with this form: https://forms.gle/R8axC5GAMXcm7VWd6

# PACKAGES ###############################

library(plumber) # for REST APIs
library(dplyr) # for data wrangling
library(readr) # for reading/writing data
library(httr) # for API calls
library(jsonlite) # for using JSONs

#* @apiTitle Bahamas Bistro API
#* @apiDescription REST API for querying our database of customer orders.
#* @apiHost NULL
#* @apiContact list(name = "Tim Fraser, PhD", url = "https://www.timothyfraser.com", email = "tmf77@cornell.edu")
#* @apiVersion 1


# ENDPOINTS ##############################

## /random/ ##############################
#* Test retrieve `n` randomly generated values
#* @get /random/
#* @param n:int An integer number of samples to draw from normal distribution
#* @response 200 A vector
#* @serializer json
function(n = 3){
  n = as.integer(n)
  output = rnorm(n = n)
  return(output)
}



## /retrieve-data/ ########################
#* Retrieve data from spreadsheet
#* @get /retrieve-data/
#* @param n:int Number of most recent orders to return
#* @response 200 A data.frame
#* @serializer csv
function(n = 3){
  
  n = as.integer(n)  
  
  # Change share link to download link
  url = "https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/export?format=csv"
  
  # Download data
  data = url %>% 
    read_csv() %>%
    tail(n) %>%
    select(Timestamp, order_id, task, team, person, done, elapsed) 
  
  return(data)
}




## /retrieve-stats/ ########################
#* Calculate statistics from spreadsheet
#* @get /retrieve-stats/
#* @param n:int Number of most recent orders to evaluate
#* @response 200 A list
#* @serializer json
function(n = 30){
  
  # Change share link to download link
  url = "https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/export?format=csv"
  
  # Download data
  data = url %>% 
    read_csv()
  
  # Overwrite n if nrows is greater
  if(nrow(data) < n){ n = nrow(data) }
  
  # Clip to most recent n rows
  data = data %>%
    tail(n)
  
  # Calculate some performance metrics...
  stat1 = data %>% 
    summarize(
      n_customers = length(unique(order_id )),
      n_customers_served = length(unique(order_id[done == TRUE] ))
    )
  
  stat2 = data %>%
    filter(done == TRUE) %>%
    group_by(order_id) %>%
    summarize(total_time = sum(elapsed)) %>%
    ungroup() %>%
    summarize(avg_time_to_completion = mean(total_time))
  
  # Format output
  output = list(
    n_orders = n,
    n_customers = stat1$n_customers,
    n_customers_served = stat1$n_customers_served,
    avg_time_to_completion = stat2$avg_time_to_completion
  )
  
  return(output)
}
