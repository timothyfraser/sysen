#' @name 13_examples.R
#' @title Factorial Design Examples for Practice
#' @description Five factorial design experiments for participants to analyze
#' using the functions from functions/functions_factorial.R

# Load required packages
library(dplyr)
library(readr)

# Source the factorial analysis functions
source("functions/functions_factorial.R")

# ============================================================================
# Example 1: Plant Growth Experiment (2^2 Factorial Design)
# ============================================================================
# 
# A researcher wants to test how fertilizer and watering schedule affect
# plant growth. They set up a 2^2 factorial experiment with:
# - Factor A: Fertilizer (none vs. added)
# - Factor B: Watering (daily vs. weekly)
# 
# Your task: Calculate the direct effects of fertilizer and watering,
# and the two-way interaction effect between them.

# Load the data
example1_plants = read_csv("workshops/plants.csv")

# View the data
example1_plants

# Your turn! Use the functions to analyze:
# 1. Direct effect of fertilizer: dbar_oneway...
# 2. Direct effect of watering: dbar_oneway...
# 3. Two-way interaction: dbar_twoway...
# 4. Standard error: se_factorial...
# 5. Which effects are statistically significant? Remember that 1.96 standard errors is a good approximation of a 95% confidence interval.
# 6. What is your conclusion for the experiment?



# ============================================================================
# Example 2: Battery Life Experiment (2^3 Factorial Design)
# ============================================================================
#
# An engineer tests how three factors affect battery life:
# - Factor A: Battery type (alkaline vs. lithium)
# - Factor B: Temperature (cold vs. warm)
# - Factor C: Usage pattern (light vs. heavy)
#
# Your task: Calculate all direct effects, two-way interactions,
# and the three-way interaction effect.

# Load the data
example2_batteries = read_csv("workshops/batteries.csv")

# View the data
example2_batteries

# Your turn! Use the functions to analyze:
# 1. Direct effect of battery_type: dbar_oneway...
# 2. Direct effect of temperature: dbar_oneway...
# 3. Direct effect of usage: dbar_oneway...
# 4. Two-way interaction (battery_type * temperature): dbar_twoway...
# 5. Two-way interaction (battery_type * usage): dbar_twoway...
# 6. Two-way interaction (temperature * usage): dbar_twoway...
# 7. Three-way interaction: dbar_threeway...
# 8. Standard error: se_factorial...
# 9. Which effects are statistically significant? Remember that 1.96 standard errors is a good approximation of a 95% confidence interval.
# 10. What is your conclusion for the experiment? Which combination of factors leads to the longest battery life?


# ============================================================================
# Example 3: Website Purchase Amount (2^3 Factorial Design)
# ============================================================================
#
# A marketing team tests three website design factors to improve customer
# spending. They measure how much each visitor spends (in dollars) when
# they visit the website:
# - Factor A: Button color (blue vs. green)
# - Factor B: Page layout (simple vs. detailed)
# - Factor C: Headline style (short vs. long)
#
# Your task: Calculate all direct effects, two-way interactions,
# and the three-way interaction effect. Interpret which combinations
# lead to the highest purchase amounts.

# Load the data
example3_website = read_csv("workshops/website.csv")

# View the data
example3_website

# Your turn! Use the functions to analyze:
# 1. Direct effect of button_color: dbar_oneway...
# 2. Direct effect of layout: dbar_oneway...
# 3. Direct effect of headline: dbar_oneway...
# 4. Two-way interaction (button_color * layout): dbar_twoway...
# 5. Two-way interaction (button_color * headline): dbar_twoway...
# 6. Two-way interaction (layout * headline): dbar_twoway...
# 7. Three-way interaction: dbar_threeway...
# 8. Standard error: se_factorial...
# 9. Which effects are statistically significant? Remember that 1.96 standard errors is a good approximation of a 95% confidence interval.
# 10. What is your conclusion for the experiment? Which combination of factors leads to the highest purchase amounts?




# ============================================================================
# Example 4: Bikeshare Usage (2^3 Fractional Factorial Design)
# ============================================================================
#
# A transportation planner wants to test how three factors affect bikeshare
# usage, but can only run half the experiments to save time and resources.
# This is a fractional factorial design (2^(3-1) = 4 runs instead of 8).
# - Factor A: Station location (downtown vs. residential)
# - Factor B: Bike type (standard vs. electric)
# - Factor C: Pricing (flat vs. per-minute)
#
# Your task: Calculate the direct effects and two-way interactions.
# Note: In fractional factorial designs, some effects are confounded
# (cannot be separated - you didn't observe enough combinations). The three-way interaction is confounded with
# the main effects in this half-fraction design.

# Load the data
example4_bikeshare = read_csv("workshops/bikeshare.csv")

# View the data
example4_bikeshare

# Your turn! Use the functions to analyze:
# 1. Direct effect of location: dbar_oneway...
# 2. Direct effect of bike_type: dbar_oneway...
# 3. Direct effect of pricing: dbar_oneway...
# 4. Two-way interaction (location * bike_type): dbar_twoway...
# 5. Two-way interaction (location * pricing): dbar_twoway...
# 6. Two-way interaction (bike_type * pricing): dbar_twoway...
# 7. Standard error: se_factorial...
# 8. Which effects are statistically significant? Remember that 1.96 standard errors is a good approximation of a 95% confidence interval.
# 9. What is your conclusion for the experiment? Which combination leads to the most daily rides?
# 10. What are the limitations of using a fractional factorial design compared to a full factorial?






# ============================================================================
# Example 5: Drone Flight Time (3^2 Factorial Design)
# ============================================================================
#
# A drone engineer tests how two factors with three levels each affect
# flight time. This is a 3^2 factorial design (2 factors, 3 levels each):
# - Factor A: Propeller size (small, medium, large)
# - Factor B: Battery capacity (low, medium, high)
#
# Your task: Analyze the effects of propeller size and battery capacity
# on flight time. Note: The standard factorial functions are designed for
# 2-level factors. For 3-level factors, you may need to:
# - Compare specific level pairs (e.g., small vs. large, low vs. high)
# - Create binary variables for comparisons

# Load the data
example5_drones = read_csv("workshops/drones.csv")

# View the data
example5_drones

# Your turn! Analyze the data:
# 1. Create binary comparisons (e.g., small vs. large propeller, low vs. high battery)
# 2. Calculate direct effects using dbar_oneway for your binary comparisons... eg.
dbar_oneway(formula = flight_time ~ propeller == "small", data = example5_drones)
# 4. Standard error: se_factorial...
# 5. Which effects are statistically significant? Remember that 1.96 standard errors is a good approximation of a 95% confidence interval.





# ============================================================================
# Tips for Interpretation
# ============================================================================
#
# 1. Direct effects tell you the average difference when changing one factor
#    from its low to high level, averaged across all other factors. 
#    By default, the low level is the level that comes alphabeticall first.
#
# 2. Two-way interactions tell you whether the effect of one factor depends
#    on the level of another factor. A large interaction means the factors
#    work together (or against each other) in a meaningful way.
#
# 3. Three-way interactions are more complex: they tell you whether a two-way
#    interaction itself depends on the level of a third factor.
#
# 4. Use the standard error to construct confidence intervals and determine
#    statistical significance. Compare each effect to its standard error to
#    see if it's meaningfully different from zero.
#
# 5. Remember: effects are calculated as (High level - Low level), where
#    "High" and "Low" are determined alphabetically by factor levels.

