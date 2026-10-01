# 00_api_queries.py
# Tim Fraser
# This is a script one of the project teams and I cooked up together.
# I include it here as an example of how you could use an API to gather data.
# We're using the FDA's medical devices database
# to query data about Medtronic Pacemakers.
# NOTE: requests are only sent when RUN_API_QUERIES=1 is set in your environment.

# Load packages
import os
import pandas as p
import urllib.request # sends http requests
import json # work with json data

# Write a simplication function to handle API results
def get_result(url):
  if os.environ.get("RUN_API_QUERIES") != "1":
    return {"results": []}
  request = urllib.request.Request(url.replace('"', "%22"), headers = {"User-Agent": "sysen-course-example"})
  with urllib.request.urlopen(request) as result:
    result2 = result.read().decode("utf-8")
  output = json.loads(result2)
  return output



# CHUNK 1
result1 = get_result(
  "https://api.fda.gov/device/event.json?" +
  'search=device.model_number.exact:"ADDRL1"' +
  "&skip=0" +
  "&limit=1000"
)

# CHUNK 1
result2 = get_result(
  "https://api.fda.gov/device/event.json?" +
  'search=device.model_number.exact:"ADDRL1"' +
  "&skip=1000" +
  "&limit=1000"
)

# CHUNK 1
result3 = get_result(
  "https://api.fda.gov/device/event.json?" +
  'search=device.model_number.exact:"ADDRL1"' +
  "&skip=2000" +
  "&limit=1000"
)

# Bundle results into a data.frame
output = p.DataFrame(
  result1["results"] +
  result2["results"] +
  result3["results"]
)

# Investigate variables
output.columns

# [c for c in output.columns if "problem" in c]

# output.filter(like = "date").info()

output2 = output.reindex(columns = ["product_problems",
         "patient",
         "device_date_of_manufacturer",
         "date_of_event"])

output2.device_date_of_manufacturer.dtype

output2.dropna(subset = ["device_date_of_manufacturer", "date_of_event"])

# Handle dates and calculate time intervals
(output2
  .dropna(subset = ["device_date_of_manufacturer", "date_of_event"])
  .assign(
    device_date_of_manufacturer = lambda d: p.to_datetime(
      d.device_date_of_manufacturer, format = "%Y%m%d", errors = "coerce"),
    date_of_event = lambda d: p.to_datetime(
      d.date_of_event, format = "%Y%m%d", errors = "coerce")
  )
  .assign(days = lambda d: (d.date_of_event - d.device_date_of_manufacturer) / p.Timedelta(days = 1),
          hours = lambda d: (d.date_of_event - d.device_date_of_manufacturer) / p.Timedelta(hours = 1))
  .to_csv("dataset.csv" if os.environ.get("RUN_API_QUERIES") == "1" else None, index = False))

# Cleanup!
globals().clear()
