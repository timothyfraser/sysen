# Update

# This script allows the course instructors to swiftly update the HTML pages of all RMarkdown tutorials hosted in the /docs folder.

library(rmarkdown)
library(rmdformats)
library(fidelius)

# Unpack the zipfile into dev/prep, using the functions in "unpack.R"
#source("dev/unpack.R")

# Set working directory as project location
setwd(".")

# Render all Workshops
render("dev/prep/workshop_1.Rmd", output_dir = "docs"); rm(list= ls())
render("dev/prep/workshop_2.Rmd", output_dir = "docs"); rm(list= ls())
render("dev/prep/workshop_3.Rmd", output_dir = "docs"); rm(list= ls())
render("dev/prep/lesson_3.Rmd", output_dir = "docs"); rm(list= ls())
render("dev/prep/workshop_4.Rmd", output_dir = "docs"); rm(list= ls())
render("dev/prep/workshop_5.Rmd", output_dir = "docs"); rm(list = ls())

# Render all assignments
# render("dev/prep/assignment_1.Rmd", output_dir = "docs"); rm(list = ls())
# render("dev/prep/assignment_2.Rmd", output_dir = "docs"); rm(list = ls())

# Password protect
# Pack and delete the dev/prep directory.
#source("dev/pack.R")

