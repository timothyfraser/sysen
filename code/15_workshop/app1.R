# app1.R
# Example Plumber REST API
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
