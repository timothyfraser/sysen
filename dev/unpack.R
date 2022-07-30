# This R script prepares a function we can use to unzip our prep folder, 
# so that students don't get mixed up by it.
# It will unzip it using a password from the dev folder, that only I have.

# Make unpacking function
unpack = function(zipfile, pw = source("dev/pw.R")$value){
  system(
    command = paste0("unzip -o -P ", pw, " ", zipfile), 
    wait = TRUE)
}

# Unpack zipfile into directory
unpack("dev/prep.zip", pw = source("dev/pw.R")$value)
