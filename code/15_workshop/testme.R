# testme.R

# A script for testing our different products in this folder.

library(plumber)
library(rmarkdown)

# Run Rmarkdown reporter
rmarkdown::render(
  input = "code/15_workshop/report.Rmd", 
  output_file = "report.html")


# Run app1
plumber::plumb(file='code/15_workshop/app1.R')$run()


# Run app2
plumber::plumb(file='code/15_workshop/app2.R')$run()


# Run app3
plumber::plumb(file='code/15_workshop/app3.R')$run()
