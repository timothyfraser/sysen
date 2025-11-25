# # app3.R
# Example Shiny App Dashboard
# Author: Tim Fraser

# startup -------------------------------------------

## This app has the following components:
# input$n  (selectInput)
# input$team (selectInput)
# output$recent_orders = renderTable({ ... })
# output$n_customers = renderText({ ... })
# output$n_customers_served = renderText({ ... })
# output$avg_time_to_completion = renderText({ ... })
# output$viz_by_team = renderPlot({ ... })
# +
# debugger for data()

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
    ## input$n --------------------------------------
    selectInput(inputId = "n", label = "SELECT NUMBER OF RECENT ORDERS", choices = c(20, 50, 100, 500), selected = 100),
    # input$team ------------------------------------
    selectInput(inputId = "team", label = "SELECT TEAM", choices = c("Front", "Kitchen", "Cashier"), selected = "Front"),
    ## output$recent_orders -------------------------
    div(h2("Recent Orders"), tableOutput("recent_orders")),
    ## output$n_customers ---------------------------
    div(h4("Total Customers"), textOutput("n_customers")),
    ## output$n_customers_served --------------------
    div(h4("Total Customers Served"), textOutput("n_customers_served")),
    ## output$avg_time_to_completion ----------------
    div(h4("Average Time to Order Completion"), textOutput("avg_time_to_completion")),
    ## output$viz_by_team ---------------------------
    div(h2("Employee Performance by Team"), plotOutput("viz_by_team"))
  )
  
}

# Define the server function - the 'backend' equivalent
server = function(input, output){
  
  ## data() -----------------------------------------
  data = reactive({
    result = get_data(n = input$n)
    ## DEBUG ----------------------------------------
    print(paste("---data(): ", nrow(result), "rows")) # summarize the object
    print(glimpse(result)) # show a glimpse of the object
    result # remember to return the output
  })
  
  ## output$n_customers -------------------------
  output$n_customers = renderText({  
    stat1 = data() %>% get_n() 
    stat1$n_customers
  })
  
  ## output$n_customers_served -------------------------
  output$n_customers_served = renderText({ 
    stat1 = data() %>% get_n() 
    stat1$n_customers_served
  })

  ## output$avg_time_to_completion -------------------------
  output$avg_time_to_completion = renderText({ 
    stat2 = data() %>% get_time_avg()
    stat2$avg_time_to_completion
  })
  
  ## output$viz_by_team -------------------------
  output$viz_by_team = renderPlot({
    get_viz_by_team(data(), .team = input$team)
  })

  ## output$recent_orders -------------------------
  output$recent_orders = renderTable({  
    data() %>% tail(5) 
  })
}

# run app ---------------------------------------------
# Run the app
shinyApp(ui = ui, server = server)
