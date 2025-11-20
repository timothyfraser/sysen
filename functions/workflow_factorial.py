# workflow_factorial.py
# Simple demonstration script for the factorial functions

# Import the functions
from functions.functions_factorial import se_factorial, dbar_oneway, dbar_twoway, dbar_threeway
import pandas as pd



# Load the lattes data
lattes = pd.read_csv("workshops/lattes.csv")

# Execute the functions
se_factorial(formula="tastiness ~ machine + syrup + art", data=lattes)

dbar_oneway(formula="tastiness ~ machine", data=lattes)

dbar_twoway(formula="tastiness ~ machine * syrup", data=lattes)

dbar_threeway(formula="tastiness ~ machine * syrup * art", data=lattes)

