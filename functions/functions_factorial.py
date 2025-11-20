# functions_factorial.py
# Script of Python functions for running difference of means tests on factorial experiments.

import pandas as pd
import numpy as np


def se_factorial(formula: str = "y ~ machine + syrup + art", data: pd.DataFrame = None):
    """
    Calculate Standard Error for Factorial Experiments
    
    Calculates the standard error for a response variable in a factorial experiment by pooling 
    standard deviations across all treatment combinations.
    
    Parameters
    ----------
    formula : str
        A formula string specifying the response variable and factors 
        (e.g., "y ~ machine + syrup + art"). The first variable should be the response variable.
    data : pd.DataFrame
        A data frame containing the variables specified in the formula.
    
    Returns
    -------
    float
        A single numeric value representing the pooled standard error.
    
    Examples
    --------
    >>> # Load the lattes data
    >>> lattes = pd.read_csv("workshops/lattes.csv")
    >>> 
    >>> # Calculate standard error for a three-factor experiment
    >>> se_factorial(formula="tastiness ~ machine + syrup + art", data=lattes)
    >>> 
    >>> # Calculate standard error for a two-factor experiment
    >>> se_factorial(formula="tastiness ~ machine + syrup", data=lattes)
    """
    # formula = "y ~ machine + syrup + art"
    # data = lattes
    
    # Parse formula to extract response and predictor variables
    parts = formula.split("~")
    y_var = parts[0].strip()
    x_vars = [v.strip() for v in parts[1].split("+")]
    
    # Get frame of data
    frame = data[[y_var] + x_vars].copy()
    frame = frame.rename(columns={y_var: "y"})
    
    # Calculate a standard error the tastiness metric in this factorial experiment
    grouped = frame.groupby(x_vars).agg(s=("y", "std"), n=("y", "count")).reset_index()
    se_squared_sum = (grouped["s"]**2 / grouped["n"]).sum()
    output = np.sqrt(se_squared_sum)
    
    return output


def dbar_oneway(formula: str, data: pd.DataFrame):
    """
    Calculate One-Way Treatment Effect
    
    Calculates the mean difference (dbar) between two levels of a single factor in a factorial 
    experiment. The function compares the "High" group (second level) to the "Low" group (first level).
    
    Parameters
    ----------
    formula : str
        A formula string with a single factor (e.g., "y ~ machine"). The first variable should be 
        the response variable, and the second should be the factor of interest.
    data : pd.DataFrame
        A data frame containing the variables specified in the formula.
    
    Returns
    -------
    float
        A single numeric value representing the mean difference between the two factor levels.
    
    Examples
    --------
    >>> # Load the lattes data
    >>> lattes = pd.read_csv("workshops/lattes.csv")
    >>> 
    >>> # Calculate one-way effect for machine factor
    >>> dbar_oneway(formula="tastiness ~ machine", data=lattes)
    >>> 
    >>> # Calculate one-way effect for syrup factor
    >>> dbar_oneway(formula="tastiness ~ syrup", data=lattes)
    """
    # formula = "y ~ machine"
    # data = lattes
    
    # Parse formula
    parts = formula.split("~")
    y_var = parts[0].strip()
    a_var = parts[1].strip()
    
    # Get frame
    frame = data[[y_var, a_var]].copy()
    frame = frame.rename(columns={y_var: "y", a_var: "a"})
    frame["a"] = pd.Categorical(frame["a"])
    frame["a"] = frame["a"].cat.codes
    
    # Compute the one-way effect
    # The mean difference between the "High" group (a == 1) and the "Low" group (a == 0)
    y_high = frame.loc[frame["a"] == 1, "y"].values
    y_low = frame.loc[frame["a"] == 0, "y"].values
    # Match R's mean(y[a == 1] - y[a == 0]) - works when balanced, otherwise use difference of means
    if len(y_high) == len(y_low):
        dbar = (y_high - y_low).mean()
    else:
        dbar = y_high.mean() - y_low.mean()
    
    return dbar


def dbar_twoway(formula: str, data: pd.DataFrame):
    """
    Calculate Two-Way Interaction Effect
    
    Calculates the two-way interaction effect (dbar) between two factors in a factorial experiment. 
    The function compares combinations where factors are aligned (both high or both low) versus 
    combinations where factors are opposite (one high, one low).
    
    Parameters
    ----------
    formula : str
        A formula string with two factors and their interaction (e.g., "y ~ machine * syrup"). 
        The first variable should be the response variable, followed by two factors.
    data : pd.DataFrame
        A data frame containing the variables specified in the formula.
    
    Returns
    -------
    float
        A single numeric value representing the two-way interaction effect.
    
    Examples
    --------
    >>> # Load the lattes data
    >>> lattes = pd.read_csv("workshops/lattes.csv")
    >>> 
    >>> # Calculate two-way interaction between machine and syrup
    >>> dbar_twoway(formula="tastiness ~ machine * syrup", data=lattes)
    >>> 
    >>> # Calculate two-way interaction between machine and art
    >>> dbar_twoway(formula="tastiness ~ machine * art", data=lattes)
    """
    # formula = "y ~ machine * syrup"
    # data = lattes
    
    # Parse formula - extract variables from interaction formula
    parts = formula.split("~")
    y_var = parts[0].strip()
    # Handle interaction notation (e.g., "machine * syrup" or "machine + syrup")
    interaction_part = parts[1].strip()
    if "*" in interaction_part:
        x_vars = [v.strip() for v in interaction_part.split("*")]
    else:
        x_vars = [v.strip() for v in interaction_part.split("+")]
    
    # Extract model frame
    frame = data[[y_var] + x_vars].copy()
    # Rename columns as y, a, b
    frame = frame.rename(columns={y_var: "y", x_vars[0]: "a", x_vars[1]: "b"})
    frame["a"] = pd.Categorical(frame["a"])
    frame["b"] = pd.Categorical(frame["b"])
    
    levels_a = frame["a"].cat.categories
    levels_b = frame["b"].cat.categories
    
    # Convert factors to integer codes
    frame["a"] = frame["a"].cat.codes + 1  # R uses 1-based indexing for factor levels
    frame["b"] = frame["b"].cat.codes + 1
    
    # Now pick the combinations for comparison
    # Same factors: HH or LL
    x1 = frame.loc[((frame["a"] == 2) & (frame["b"] == 2)) | 
                   ((frame["a"] == 1) & (frame["b"] == 1)), "y"]
    # Opposite factors: HL or LH
    x0 = frame.loc[((frame["a"] == 1) & (frame["b"] == 2)) | 
                   ((frame["a"] == 2) & (frame["b"] == 1)), "y"]
    
    # Calculate dbar
    dbar = x1.mean() - x0.mean()
    
    return dbar


def dbar_threeway(formula: str, data: pd.DataFrame):
    """
    Calculate Three-Way Interaction Effect
    
    Calculates the three-way interaction effect (dbar) between three factors in a factorial experiment. 
    The function evaluates the AC interaction at different levels of factor B, then computes the 
    average difference between these interactions.
    
    Parameters
    ----------
    formula : str
        A formula string with three factors and their interactions (e.g., "y ~ machine * syrup * art"). 
        The first variable should be the response variable, followed by three factors.
    data : pd.DataFrame
        A data frame containing the variables specified in the formula.
    
    Returns
    -------
    float
        A single numeric value representing the three-way interaction effect.
    
    Examples
    --------
    >>> # Load the lattes data
    >>> lattes = pd.read_csv("workshops/lattes.csv")
    >>> 
    >>> # Calculate three-way interaction between machine, syrup, and art
    >>> dbar_threeway(formula="tastiness ~ machine * syrup * art", data=lattes)
    """
    # formula = "y ~ machine * syrup * art"
    # data = lattes
    
    # Parse formula
    parts = formula.split("~")
    y_var = parts[0].strip()
    # Handle interaction notation
    interaction_part = parts[1].strip()
    if "*" in interaction_part:
        x_vars = [v.strip() for v in interaction_part.split("*")]
    else:
        x_vars = [v.strip() for v in interaction_part.split("+")]
    
    frame = data[[y_var] + x_vars].copy()
    frame = frame.rename(columns={y_var: "y", x_vars[0]: "a", x_vars[1]: "b", x_vars[2]: "c"})
    frame["a"] = pd.Categorical(frame["a"])
    frame["b"] = pd.Categorical(frame["b"])
    frame["c"] = pd.Categorical(frame["c"])
    frame["a"] = frame["a"].cat.codes  # R uses 0-based after subtracting 1
    frame["b"] = frame["b"].cat.codes
    frame["c"] = frame["c"].cat.codes
    
    # Get the AC interaction when B = 0
    y_a1_b0_c1 = frame.loc[(frame["a"] == 1) & (frame["b"] == 0) & (frame["c"] == 1), "y"].values
    y_a0_b0_c1 = frame.loc[(frame["a"] == 0) & (frame["b"] == 0) & (frame["c"] == 1), "y"].values
    y_a1_b0_c0 = frame.loc[(frame["a"] == 1) & (frame["b"] == 0) & (frame["c"] == 0), "y"].values
    y_a0_b0_c0 = frame.loc[(frame["a"] == 0) & (frame["b"] == 0) & (frame["c"] == 0), "y"].values
    
    # Get the AC interaction when B = 1
    y_a1_b1_c1 = frame.loc[(frame["a"] == 1) & (frame["b"] == 1) & (frame["c"] == 1), "y"].values
    y_a0_b1_c1 = frame.loc[(frame["a"] == 0) & (frame["b"] == 1) & (frame["c"] == 1), "y"].values
    y_a1_b1_c0 = frame.loc[(frame["a"] == 1) & (frame["b"] == 1) & (frame["c"] == 0), "y"].values
    y_a0_b1_c0 = frame.loc[(frame["a"] == 0) & (frame["b"] == 1) & (frame["c"] == 0), "y"].values
    
    # Calculate differences (matching R's vectorized operations)
    d1a = y_a1_b0_c1 - y_a0_b0_c1
    d0a = y_a1_b0_c0 - y_a0_b0_c0
    d1b = y_a1_b1_c1 - y_a0_b1_c1
    d0b = y_a1_b1_c0 - y_a0_b1_c0
    
    # Get AC interaction effect when B = 0
    dbar_a = (np.mean(d1a) - np.mean(d0a)) / 2
    # Get AC interaction effect when B = 1
    dbar_b = (np.mean(d1b) - np.mean(d0b)) / 2
    # Get the average of the two effects
    dbar = (dbar_b - dbar_a) / 2
    
    return dbar


# ============================================================================
# Testing Examples
# ============================================================================

# if __name__ == "__main__":
#     # Create sample data for testing
#     np.random.seed(42)
    
#     # Generate factorial design data similar to lattes example
#     machines = ["Low", "High"] * 8
#     syrups = ["Low", "Low", "High", "High"] * 4
#     arts = ["Low"] * 8 + ["High"] * 8
    
#     # Generate response with some structure
#     tastiness = (
#         5.0 + 
#         (np.array([1 if m == "High" else 0 for m in machines]) * 1.5) +
#         (np.array([1 if s == "High" else 0 for s in syrups]) * 0.8) +
#         (np.array([1 if a == "High" else 0 for a in arts]) * 0.6) +
#         np.random.normal(0, 0.5, 16)
#     )
    
#     lattes = pd.DataFrame({
#         "machine": machines,
#         "syrup": syrups,
#         "art": arts,
#         "tastiness": tastiness
#     })
    
#     print("=" * 70)
#     print("Testing functions_factorial.py")
#     print("=" * 70)
#     print("\nSample data (first 10 rows):")
#     print(lattes.head(10))
#     print("\n" + "=" * 70)
    
#     # Test se_factorial
#     print("\n1. Testing se_factorial:")
#     print("-" * 70)
#     se_3way = se_factorial(formula="tastiness ~ machine + syrup + art", data=lattes)
#     print(f"   Three-factor SE: {se_3way:.4f}")
    
#     se_2way = se_factorial(formula="tastiness ~ machine + syrup", data=lattes)
#     print(f"   Two-factor SE:   {se_2way:.4f}")
    
#     # Test dbar_oneway
#     print("\n2. Testing dbar_oneway:")
#     print("-" * 70)
#     dbar_machine = dbar_oneway(formula="tastiness ~ machine", data=lattes)
#     print(f"   Machine effect:  {dbar_machine:.4f}")
    
#     dbar_syrup = dbar_oneway(formula="tastiness ~ syrup", data=lattes)
#     print(f"   Syrup effect:    {dbar_syrup:.4f}")
    
#     dbar_art = dbar_oneway(formula="tastiness ~ art", data=lattes)
#     print(f"   Art effect:      {dbar_art:.4f}")
    
#     # Test dbar_twoway
#     print("\n3. Testing dbar_twoway:")
#     print("-" * 70)
#     dbar_machine_syrup = dbar_twoway(formula="tastiness ~ machine * syrup", data=lattes)
#     print(f"   Machine × Syrup interaction: {dbar_machine_syrup:.4f}")
    
#     dbar_machine_art = dbar_twoway(formula="tastiness ~ machine * art", data=lattes)
#     print(f"   Machine × Art interaction:   {dbar_machine_art:.4f}")
    
#     dbar_syrup_art = dbar_twoway(formula="tastiness ~ syrup * art", data=lattes)
#     print(f"   Syrup × Art interaction:     {dbar_syrup_art:.4f}")
    
#     # Test dbar_threeway
#     print("\n4. Testing dbar_threeway:")
#     print("-" * 70)
#     dbar_three = dbar_threeway(formula="tastiness ~ machine * syrup * art", data=lattes)
#     print(f"   Machine × Syrup × Art interaction: {dbar_three:.4f}")
    
#     print("\n" + "=" * 70)
#     print("All tests completed!")
#     print("=" * 70)

