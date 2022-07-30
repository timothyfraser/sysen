# This R script prepares a function we can use to zip our development, 
# so that students don't get mixed up by it.
# We'll password protect it.

# I have set a password in the file "dev/pw.R",
# that only I have a copy of. 

# Make packing function
pack = function(path, pw = source("dev/pw.R")$value){
  # Get path of zipfile to be made
  zippath <- paste(path, ".zip", sep = "")
  # Delete any file currently there
  unlink(zippath, recursive = TRUE)
  # Zip it, and password protect it
  zip(
    zipfile = zippath, 
    files = path, 
    flags = paste("--password", pw, "-r", sep = " "))
  # Delete the directory that was zipped
  unlink(path, recursive = TRUE)
}

# Packe the directory into a zipfile
pack("dev/prep")
