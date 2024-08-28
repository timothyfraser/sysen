# functions_models.py

# Functions for modeling in Python 
#
# !pip install pandas # for dataframes
# !pip install statsmodels # for models
# !pip install patsy # for model specification

# Let's write an lm() equivalent
def lm(formula, data):
    """
    Create a linear model, in syntax matching the method in R.
    
    Parameters:
      formula: a string of the shape 'y ~ x + z'. Can perform most all the same syntax as formulas in R.
      data: a pandas DataFrame containing all vectors referenced in the formula.
      
    Returns: 
      statsmodels.regression.linear_model.RegressionResultsWrapper: A model object
    """
    import statsmodels.api as sm
    # Create an OLS model
    m = sm.formula.ols(formula = formula, data = data).fit()
    return m

sm.api.formula.ols
# Let's replicate tidy() and glance() from the broom package.

## tidy() #########################################
def tidy(x, ci = 0.95):
    """
    Create a tidy data.frame of model coefficient statistics
    
    Parameters: 
      x (statsmodels.regression.linear_model.RegressionResultsWrapper): A fitted OLS model object from statsmodels.
      ci (float, optional): Confidence level. Default is 0.95 (95% confidence).
      
    Returns:
        pandas.DataFrame: A DataFrame containing the terms, estimates, standard errors, t-statistics, p-values, 
                          and confidence intervals (lower and upper bounds) for the model coefficients.
    """
    # Dependencies
    from pandas import DataFrame, Series
    from statsmodels.api import OLS
    # Testing values
    x = m
    ci = 0.95
    output = DataFrame({
      'term' : x.params.index.values,
      'estimate' : x.params.values,
      'se' : x.bse.values,
      'statistic' : x.tvalues.values,
      'p_value' : x.pvalues.values
    })
    
    # Get confidence intervals
    intervals = x.conf_int(alpha = 1 - ci)
    # Assign confidence intervals to data.frame
    output['lower'] = intervals.iloc[:,0].values
    output['upper'] = intervals.iloc[:,1].values
    # Return output
    return output


## glance() ##########################################
def glance(x):
    """
    Summarize a model with a glance as a data.frame of model statistics   
    Parameters: 
      x (statsmodels.regression.linear_model.OLSResults): A fitted OLS model object from statsmodels.
      
    Returns:
        pandas.DataFrame: A DataFrame containing the goodness of fit statistics for model.
    """
    # Dependencies
    from pandas import DataFrame, Series
    from statsmodels.api import OLS
    # Extract values as series from model into data.frame
    output = DataFrame({
        'rsq' : Series(x.rsquared),
        'adj_rsq' : Series(x.rsquared_adj),
        'sigma' : Series(x.mse_resid**.5),
        'statistic' : Series(x.fvalue),
        'p_value' : Series(x.f_pvalue),
        'df': Series(x.df_model),
        'loglik': Series(x.llf),
        'aic': Series(x.aic),
        'bic': Series(x.bic),
        'df.residual': Series(x.df_resid),
        'nobs': Series(x.nobs)
      })
    return output

