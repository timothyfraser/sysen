# testme.R

# A script for testing our different products in this folder.

library(shiny)
library(plumber)
library(rmarkdown)


# Run shiny app v1
shiny::runApp("code/15_workshop/dashboard/app1.R")

# Run shiny app v2
shiny::runApp("code/15_workshop/dashboard/app2.R")

# Run shiny app v3
shiny::runApp("code/15_workshop/dashboard/app3.R")

# Run shiny app v4
shiny::runApp("code/15_workshop/dashboard/app4.R")


# Run Rmarkdown reporter
rmarkdown::render(
  input = "code/15_workshop/report/report.Rmd", 
  output_file = "report.html")


# Run app1
plumber::plumb(file='code/15_workshop/api/app1.R')$run()


# Run app2
plumber::plumb(file='code/15_workshop/api/app2.R')$run()


# Run app3
plumber::plumb(file='code/15_workshop/api/app3.R')$run()

# Run app4
plumber::plumb(file='code/15_workshop/api/app4.R')$run()
