# app3.py
# Example FastAPI REST API - the Python twin of app3.R
# Author: Tim Fraser

# Run it (from code/apps/api):   uvicorn app3:app --port 8000
# Then open http://127.0.0.1:8000/docs to try every endpoint (Swagger docs).

# PACKAGES ###############################

import numpy as np   # for random draws
import pandas as pd  # for data wrangling
from fastapi import FastAPI  # for REST APIs
from fastapi.responses import PlainTextResponse  # to send back CSV text

app = FastAPI(
    title = "Bahamas Bistro API",
    description = "REST API for querying our database of customer orders.",
    version = "1")

# Our database: a Google Sheet, downloaded as CSV
URL = "https://docs.google.com/spreadsheets/d/15yBf5tapFSq-n6668GQ_fa3LQNafJUtxxJdjPhbaT3c/export?format=csv"


# ENDPOINTS ##############################

## /random/ ##############################
@app.get("/random/")
def random_values(n: int = 3):
    """Test retrieve `n` randomly generated values"""
    return np.random.normal(size = n).tolist()


## /retrieve-data/ ########################
@app.get("/retrieve-data/", response_class = PlainTextResponse)
def retrieve_data(n: int = 3):
    """Retrieve the `n` most recent orders, as CSV"""
    data = pd.read_csv(URL).tail(n)
    data = data[["Timestamp", "order_id", "task", "team", "person", "done", "elapsed"]]
    return data.to_csv(index = False)


## /retrieve-stats/ ########################
@app.get("/retrieve-stats/")
def retrieve_stats(n: int = 30):
    """Calculate statistics from the `n` most recent orders"""
    data = pd.read_csv(URL)

    # Overwrite n if there are fewer rows, then clip to the most recent n
    n = min(n, len(data))
    data = data.tail(n)

    # Calculate some performance metrics...
    served = data[data["done"].astype(str) == "TRUE"]  # done arrives as the text TRUE / FALSE
    avg_time = served.groupby("order_id")["elapsed"].sum().mean()

    # Format output
    return {
        "n_orders": n,
        "n_customers": int(data["order_id"].nunique()),
        "n_customers_served": int(served["order_id"].nunique()),
        "avg_time_to_completion": float(avg_time)}
