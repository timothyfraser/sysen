#' @name 00_api_queries.R
#' @author Tim Fraser
#' @description 
#' This is a script one of the project teams and I cooked up together.
#' I include it here as an example of how you could use an API to gather data.
#' We're using the FDA's medical devices database 
#' to query data about Medtronic Pacemakers.

# Load packages
library(dplyr)
library(readr)
library(stringr)
library(lubridate)
library(httr) # sends http requests
library(jsonlite) # work with json data

# Write a simplication function to handle API results
get_result = function(result){
  result2 = rawToChar(result$content)
  output = jsonlite::fromJSON(result2)
  return(output)
}



# CHUNK 1
result1 = paste0(
  "https://api.fda.gov/device/event.json?",
  'search=device.model_number.exact:"ADDRL1"',
  "&skip=0",
  "&limit=1000"
) %>%
  GET() %>%
  get_result()

# CHUNK 1
result2 = paste0(
  "https://api.fda.gov/device/event.json?",
  'search=device.model_number.exact:"ADDRL1"',
  "&skip=1000",
  "&limit=1000"
) %>%
  GET() %>%
  get_result()

# CHUNK 1
result3 = paste0(
  "https://api.fda.gov/device/event.json?",
  'search=device.model_number.exact:"ADDRL1"',
  "&skip=2000",
  "&limit=1000"
) %>%
  GET() %>%
  get_result()

# Bundle results into a data.frame
output = bind_rows(
  result1$results,
  result2$results,
  result3$results
)

# Investigate variables
output %>%
  names()

# tibble(table = output %>% names() ) %>%
#   filter(str_detect(table, "problem"))

# output %>%
#   select(contains("date")) %>%
#   glimpse()

output2 = output %>%
  select(product_problems, 
         patient,
         device_date_of_manufacturer,
         date_of_event)

output2$device_date_of_manufacturer %>% class()

output2 %>%
  filter(!is.na(device_date_of_manufacturer), !is.na(date_of_event))

# Handle dates and calculate time intervals
output2 %>%
  filter(!is.na(device_date_of_manufacturer), !is.na(date_of_event)) %>%
  mutate(
    device_date_of_manufacturer = lubridate::make_date(
      year = str_sub(device_date_of_manufacturer, 1,4),
      month = str_sub(device_date_of_manufacturer, 5,6),
      day = str_sub(device_date_of_manufacturer, 7,8)
    ),
    date_of_event = lubridate::make_date(
      year = str_sub(date_of_event, 1,4),
      month = str_sub(date_of_event, 5,6),
      day = str_sub(date_of_event, 7,8)
    )
  ) %>%
  mutate(days = as.numeric(difftime(date_of_event, device_date_of_manufacturer, units = "days")),
         hours = as.numeric(difftime(date_of_event, device_date_of_manufacturer, units = "hours"))) %>%
  write_csv("dataset.csv")

# Cleanup!
rm(list())



