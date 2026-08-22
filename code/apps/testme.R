# testme.R
# Tim Fraser
# Extras: run the Shiny dashboards, Plumber APIs and parameterized report in code/apps/
# Chapter: none - these apps are course extras, not a textbook chapter

library(shiny)
library(plumber)
library(rmarkdown)


# Run shiny app v1
shiny::runApp("code/apps/dashboard/app1.R")

# Run shiny app v2
shiny::runApp("code/apps/dashboard/app2.R")

# Run shiny app v3
shiny::runApp("code/apps/dashboard/app3.R")

# Run shiny app v4
shiny::runApp("code/apps/dashboard/app4.R")


# Run Rmarkdown reporter
rmarkdown::render(
  input = "code/apps/report/report.Rmd", 
  output_file = "report.html")


# Run app1
plumber::plumb(file='code/apps/api/app1.R')$run()


# Run app2
plumber::plumb(file='code/apps/api/app2.R')$run()


# Run app3
plumber::plumb(file='code/apps/api/app3.R')$run()

# Run app4
plumber::plumb(file='code/apps/api/app4.R')$run()
