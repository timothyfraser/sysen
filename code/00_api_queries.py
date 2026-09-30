# 00_api_queries.py
# Tim Fraser
# This is a script one of the project teams and I cooked up together.
# I include it here as an example of how you could use an API to gather data.
# We're using the FDA's medical devices database
# to query data about Medtronic Pacemakers.

# It mirrors 00_api_queries.R section by section.
# Run it from the top of the sysen folder.

# NOTE: the openFDA API is public and needs no API key.

# NOTE: this script talks to the internet, so every network call sits behind
#   if __name__ == "__main__" and os.environ.get("RUN_API_QUERIES") == "1":
# Importing this file, or running it without that flag (as our automated
# checks do), sends no requests at all. To really run the queries:
#   RUN_API_QUERIES=1 python code/00_api_queries.py            (Mac / Linux / Git Bash)
#   $env:RUN_API_QUERIES="1"; python code/00_api_queries.py    (Windows PowerShell)

# Load packages
import os
import json                    # work with json data (jsonlite in R)
import urllib.request          # sends http requests (httr in R)
import pandas as pd            # data wrangling (dplyr + readr + stringr in R)

# Write a simplication function to handle API results
def get_result(url):
    # GET() the url, then turn the raw bytes into text, then parse the JSON.
    # (We name ourselves with a User-Agent header, as httr does in R;
    # some servers refuse Python's default "Python-urllib" name.)
    request = urllib.request.Request(url, headers={"User-Agent": "sysen-course-example"})
    with urllib.request.urlopen(request) as result:
        result2 = result.read().decode("utf-8")
    output = json.loads(result2)
    return output

# NOTE: R's httr percent-encodes the quotes in the url for us;
# in Python we swap each " for %22 ourselves.
def fda_url(skip, limit=1000):
    return ("https://api.fda.gov/device/event.json?"
            'search=device.model_number.exact:%22ADDRL1%22'
            f"&skip={skip}"
            f"&limit={limit}")


if __name__ == "__main__" and os.environ.get("RUN_API_QUERIES") == "1":

    # CHUNK 1
    result1 = get_result(fda_url(skip=0))

    # CHUNK 1
    result2 = get_result(fda_url(skip=1000))

    # CHUNK 1
    result3 = get_result(fda_url(skip=2000))

    # Bundle results into a data.frame
    output = pd.DataFrame(
        result1.get("results", []) +
        result2.get("results", []) +
        result3.get("results", [])
    )

    # Investigate variables
    print(list(output.columns))

    # print([c for c in output.columns if "problem" in c])

    # print(output.filter(like="date").info())

    output2 = output[["product_problems",
                      "patient",
                      "device_date_of_manufacturer",
                      "date_of_event"]].copy()

    # dates arrive as text like "20190314"
    print(type(output2["device_date_of_manufacturer"].iloc[0]))

    print(output2.dropna(subset=["device_date_of_manufacturer", "date_of_event"]))

    # Handle dates and calculate time intervals
    output3 = output2.dropna(subset=["device_date_of_manufacturer", "date_of_event"]).copy()
    # year = first 4 characters, month = next 2, day = last 2 (make_date() in R)
    output3["device_date_of_manufacturer"] = pd.to_datetime(
        output3["device_date_of_manufacturer"], format="%Y%m%d", errors="coerce")
    output3["date_of_event"] = pd.to_datetime(
        output3["date_of_event"], format="%Y%m%d", errors="coerce")
    gap = output3["date_of_event"] - output3["device_date_of_manufacturer"]
    output3["days"] = gap / pd.Timedelta(days=1)
    output3["hours"] = gap / pd.Timedelta(hours=1)
    output3.to_csv("dataset.csv", index=False)

    # Cleanup!
    # (Python frees these objects when the script ends; nothing to rm().)

elif __name__ == "__main__":
    print("00_api_queries.py: set RUN_API_QUERIES=1 to send the openFDA queries.")
