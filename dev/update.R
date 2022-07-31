# Update

# This script allows the course instructors to swiftly update the HTML pages of all RMarkdown tutorials hosted in the /docs folder.

library(rmarkdown)
library(rmdformats)

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

# Pack and delete the dev/prep directory.
#source("dev/pack.R")

