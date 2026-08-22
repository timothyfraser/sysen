# # app1.R
# Example Shiny App Dashboard
# Author: Tim Fraser

# startup -------------------------------------------

## This app has the following components:
# input$n  (selectInput)
# output$recent_orders = renderTable({ ... })
# output$n_customers = renderText({ ... })

# pairs with this data: https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/edit?usp=sharing 
# pairs with this form: https://forms.gle/R8axC5GAMXcm7VWd6


# Load packages
library(dplyr)
library(readr)
library(ggplot2)
library(shiny)

# Load in helper functions (in app script, we run app as if from app directory)
source("functions.R")


# Define the user interface function - the 'frontend' component
ui = function(){
  fluidPage(
    h1("Bahamas Bistro Status Report"),
    ## input$n ---------------------------------
    selectInput(inputId = "n", label = "SELECT NUMBER OF RECENT ORDERS", choices = c(20, 50, 100, 500), selected = 100),
    ## output$recent_orders --------------------
    div(h2("Recent Orders"), tableOutput("recent_orders")),
    ## output$n_customers ----------------------
    div(h4("Total Customers"), textOutput("n_customers"))
  )
  
}


# Define the server function - the 'backend' equivalent
server = function(input, output){
  
  ## data() --------------------------------
  data = reactive({
    get_data(n = input$n)
  })

  ## output$recent_orders --------------------------------
  # Return the 5 most recent orders
  output$recent_orders = renderTable({  
    data() %>% tail(5)  
  })
  
  ## output$n_customers --------------------------------
  output$n_customers = renderText({  
    stat1 = data() %>% get_n() 
    stat1$n_customers
  })
  
}

# run app ---------------------------------------------
# Run the app
shinyApp(ui = ui, server = server)
