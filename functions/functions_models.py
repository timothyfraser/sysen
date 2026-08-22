# What this file is ----------------------------------------------------------
#
# Python versions of the modeling commands R gives you: lm() to fit a linear
# model, tidy() to lay its coefficients out as a table, and glance() to
# summarize how the whole model did in a single row.
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_models import lm, tidy, glance
#
# Then try:
#   import pandas as pd
#   diamonds = pd.read_csv("workshops/mydiamonds.csv")
#   m = lm(formula = 'price ~ carat', data = diamonds)
#   tidy(m)
#
# You never need to edit anything below.
#

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

# sm.api.formula.ols
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


## htmlreg() ##########################################
def htmlreg(models, file=None, bold=0.05, include_fstat=True, 
            custom_model_names=None, custom_coef_map=None, 
            caption="Statistical models", caption_above=False,
            custom_note=None, single_row=False):
    """
    Create an HTML regression table similar to R's htmlreg() from texreg package.
    
    Parameters:
      models: A list of fitted OLS model objects from statsmodels
      file: Path to save HTML file (optional)
      bold: P-value threshold for bold formatting (default 0.05)
      include_fstat: Whether to include F-statistic (default True)
      custom_model_names: List of custom names for models (optional)
      custom_coef_map: Dictionary mapping coefficient names to display names (optional)
      caption: Table caption (default "Statistical models")
      caption_above: Whether to place caption above table (default False)
      custom_note: Custom footnote text (optional)
      single_row: Whether to put coefficient and SE on same row (default False)
      
    Returns:
        str: HTML table as string
    """
    import numpy as np
    from pandas import DataFrame
    
    if not isinstance(models, list):
        models = [models]
    
    # Get all unique coefficient names across all models
    all_coefs = set()
    for model in models:
        all_coefs.update(model.params.index.tolist())
    all_coefs = sorted(list(all_coefs))
    
    # Apply custom coefficient mapping if provided
    if custom_coef_map:
        # Filter coefficients to only those in the map
        all_coefs = [c for c in all_coefs if c in custom_coef_map]
        # Reorder according to custom_coef_map order
        all_coefs = [c for c in custom_coef_map.keys() if c in all_coefs]
        coef_display_names = {c: custom_coef_map[c] for c in all_coefs}
    else:
        coef_display_names = {c: c for c in all_coefs}
    
    # Model names
    if custom_model_names:
        model_names = custom_model_names
    else:
        model_names = [f"Model {i+1}" for i in range(len(models))]
    
    # Start building HTML
    html_parts = []
    html_parts.append('<table class="texreg" style="margin: 10px auto;border-collapse: collapse;border-spacing: 0px;caption-side: bottom;color: #000000;border-top: 2px solid #000000;">')
    
    # Caption
    if caption_above:
        html_parts.append(f'<caption style="caption-side: top;">{caption}</caption>')
    
    # Header
    html_parts.append('<thead>')
    html_parts.append('<tr>')
    html_parts.append('<th style="padding-left: 5px;padding-right: 5px;">&nbsp;</th>')
    for name in model_names:
        html_parts.append(f'<th style="padding-left: 5px;padding-right: 5px;">{name}</th>')
    html_parts.append('</tr>')
    html_parts.append('</thead>')
    html_parts.append('<tbody>')
    
    # Helper function to get significance stars
    def get_stars(p_value):
        if p_value < 0.001:
            return '<sup>***</sup>'
        elif p_value < 0.01:
            return '<sup>**</sup>'
        elif p_value < 0.05:
            return '<sup>*</sup>'
        else:
            return ''
    
    # Helper function to format number
    def fmt_num(x, decimals=2):
        if abs(x) < 0.01:
            return f"{x:.2e}"
        else:
            return f"{x:.{decimals}f}"
    
    # Add coefficients
    for coef_name in all_coefs:
        # Coefficient name row
        html_parts.append('<tr style="border-top: 1px solid #000000;">')
        html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{coef_display_names[coef_name]}</td>')
        
        for model in models:
            if coef_name in model.params.index:
                coef_val = model.params[coef_name]
                se_val = model.bse[coef_name]
                p_val = model.pvalues[coef_name]
                stars = get_stars(p_val)
                is_bold = p_val < bold
                
                if single_row:
                    # Coefficient and SE on same row
                    coef_str = fmt_num(coef_val, 2)
                    if is_bold:
                        coef_str = f"<b>{coef_str}</b>"
                    html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{coef_str}{stars}<br/>({fmt_num(se_val, 2)})</td>')
                else:
                    # Coefficient row
                    coef_str = fmt_num(coef_val, 2)
                    if is_bold:
                        coef_str = f"<b>{coef_str}</b>"
                    html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{coef_str}{stars}</td>')
            else:
                html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">&nbsp;</td>')
        
        html_parts.append('</tr>')
        
        # Standard error row (if not single_row)
        if not single_row:
            html_parts.append('<tr>')
            html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">&nbsp;</td>')
            for model in models:
                if coef_name in model.params.index:
                    se_val = model.bse[coef_name]
                    html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">({fmt_num(se_val, 2)})</td>')
                else:
                    html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">&nbsp;</td>')
            html_parts.append('</tr>')
    
    # Add model fit statistics
    html_parts.append('<tr style="border-top: 1px solid #000000;">')
    html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">R<sup>2</sup></td>')
    for model in models:
        r2 = model.rsquared
        html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{fmt_num(r2, 2)}</td>')
    html_parts.append('</tr>')
    
    html_parts.append('<tr>')
    html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">Adj. R<sup>2</sup></td>')
    for model in models:
        adj_r2 = model.rsquared_adj
        html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{fmt_num(adj_r2, 2)}</td>')
    html_parts.append('</tr>')
    
    html_parts.append('<tr>')
    html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">Num. obs.</td>')
    for model in models:
        nobs = int(model.nobs)
        html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{nobs}</td>')
    html_parts.append('</tr>')
    
    if include_fstat:
        html_parts.append('<tr>')
        html_parts.append('<td style="padding-left: 5px;padding-right: 5px;">F statistic</td>')
        for model in models:
            fstat = model.fvalue
            html_parts.append(f'<td style="padding-left: 5px;padding-right: 5px;">{fmt_num(fstat, 2)}</td>')
        html_parts.append('</tr>')
    
    html_parts.append('</tbody>')
    
    # Caption at bottom if not above
    if not caption_above:
        html_parts.append(f'<caption>{caption}</caption>')
    
    html_parts.append('</table>')
    
    # Add footnote if provided
    if custom_note:
        html_parts.append(f'<p style="font-size: 0.9em; margin-top: 10px;">{custom_note}</p>')
    else:
        # Default significance note
        html_parts.append('<p style="font-size: 0.9em; margin-top: 10px;">Statistical Significance: *** p &lt; 0.001; ** p &lt; 0.01; * p &lt; 0.05</p>')
    
    html_string = '\n'.join(html_parts)
    
    # Save to file if specified
    if file:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html_string)
    
    return html_string

