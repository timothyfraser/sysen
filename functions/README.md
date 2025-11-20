# `functions` README

This folder contains scripts for `functions` that you may call into R or Python.
We may add a few functions here across the course of term to support your learning.

## R Functions

### `functions_factorial.R`

| Function | Description |
|----------|-------------|
| [`se_factorial`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.R) | Calculate Standard Error for Factorial Experiments |
| [`dbar_oneway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.R) | Calculate One-Way Treatment Effect |
| [`dbar_twoway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.R) | Calculate Two-Way Interaction Effect |
| [`dbar_threeway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.R) | Calculate Three-Way Interaction Effect |

### `functions_crosstab.R`

| Function | Description |
|----------|-------------|
| [`crosstab`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_crosstab.R) | Crosstabulate Data into intervals where r >= 5 |

### `functions_process_control.R`

| Function | Description |
|----------|-------------|
| [`set_theme`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Set Theme of All ggplots |
| [`describe`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Describe a vector `x` |
| [`ggprocess`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Make a Process Overview Diagram in ggplot |
| [`get_stat_s`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Subgroup Statistics |
| [`get_stat_t`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Total Statistics |
| [`get_labels`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Labels from Subgroup Statistics |
| [`dn`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Calculate control constants for range charts |
| [`bn`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Calculate control constants for standard deviation charts |
| [`limits_avg`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Upper and Lower Control Limits for an Averages Chart |
| [`limits_s`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Upper and Lower Control Limits for a Standard Deviation Chart |
| [`limits_r`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Upper and Lower Control Limits for a Range Chart |
| [`limits_mr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Get Upper and Lower Control Limits for a Moving Range Chart |
| [`ggxbar`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Average Control Chart with ggplot |
| [`ggs`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Standard Deviation Chart with ggplot |
| [`ggr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Range Chart with ggplot |
| [`ggmr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Moving Range Chart with ggplot |
| [`ggp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Fraction Defective (p) Chart in ggplot |
| [`ggnp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Number of Defects (np) Chart in ggplot |
| [`ggu`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Defects per Product (u) Chart in ggplot |
| [`cp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Capability Index (for centered, stable processes) |
| [`pp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Process Performance Index (for centered, unstable processes) |
| [`cpk`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Capability Index (for uncentered, stable processes) |
| [`ppk`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Process Performance Index (for uncentered, unstable processes) |
| [`get_index`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R) | Bootstrap Process Capability/Performance Index with Confidence Intervals |

### `functions_reliability.R`

| Function | Description |
|----------|-------------|
| [`f`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_reliability.R) | Failure Function |
| [`r`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_reliability.R) | Reliability Function |
| [`z`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_reliability.R) | Failure Rate Function |
| [`h`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_reliability.R) | Accumulative Hazard Function |
| [`afr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_reliability.R) | Average Failure Rate Function |

## Python Functions

### `functions_distributions.py`

| Function | Description |
|----------|-------------|
| [`hist`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Make a quick histogram |
| [`skewness`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Calculate skewness |
| [`kurtosis`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Calculate kurtosis |
| [`seq`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate a sequence of numbers |
| [`density`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Estimate density using Gaussian KDE |
| [`tidy_density`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Create tidy dataframe of density values |
| [`approxfun`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Approximate a data.frame of x and y data into a function |
| [`exp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Euler's number |
| [`dnorm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Normal distribution PDF |
| [`pnorm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Normal distribution CDF |
| [`qnorm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Normal distribution quantile function |
| [`rnorm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random normal values |
| [`dexp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Exponential distribution PDF |
| [`pexp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Exponential distribution CDF |
| [`qexp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Exponential distribution quantile function |
| [`rexp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random exponential values |
| [`dweibull`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Weibull distribution PDF |
| [`pweibull`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Weibull distribution CDF |
| [`qweibull`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Weibull distribution quantile function |
| [`rweibull`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random Weibull values |
| [`dgamma`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Gamma distribution PDF |
| [`pgamma`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Gamma distribution CDF |
| [`qgamma`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Gamma distribution quantile function |
| [`rgamma`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random gamma values |
| [`dpois`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Poisson distribution PMF |
| [`ppois`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Poisson distribution CDF |
| [`qpois`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Poisson distribution quantile function |
| [`rpois`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random Poisson values |
| [`dbinom`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Binomial distribution PMF |
| [`pbinom`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Binomial distribution CDF |
| [`qbinom`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Binomial distribution quantile function |
| [`rbinom`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random binomial values |
| [`dunif`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Uniform distribution PDF |
| [`punif`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Uniform distribution CDF |
| [`qunif`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Uniform distribution quantile function |
| [`runif`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_distributions.py) | Generate random uniform values |

### `functions_models.py`

| Function | Description |
|----------|-------------|
| [`lm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_models.py) | Create a linear model |
| [`tidy`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_models.py) | Create a tidy data.frame of model coefficient statistics |
| [`glance`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_models.py) | Summarize a model with a glance as a data.frame of model statistics |

### `functions_process_control.py`

| Function | Description |
|----------|-------------|
| [`describe`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Describe a vector x |
| [`ggprocess`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Make a Process Overview Diagram |
| [`get_stat_s`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Subgroup Statistics |
| [`get_stat_t`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Total Statistics |
| [`get_labels`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Labels from Subgroup Statistics |
| [`rnorm`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Generate random normal values |
| [`dn`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Calculate control constants for range charts |
| [`bn`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Calculate control constants for standard deviation charts |
| [`limits_avg`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Upper and Lower Control Limits for an Averages Chart |
| [`limits_s`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Upper and Lower Control Limits for a Standard Deviation Chart |
| [`limits_r`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Upper and Lower Control Limits for a Range Chart |
| [`limits_mr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Get Upper and Lower Control Limits for a Moving Range Chart |
| [`ggxbar`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Average Control Chart with ggplot |
| [`ggavg`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Average Control Chart with ggplot (alias for ggxbar) |
| [`ggs`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Standard Deviation Chart with ggplot |
| [`ggr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Range Chart with ggplot |
| [`ggmr`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Moving Range Chart with ggplot |
| [`ggp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Fraction Defective (p) Chart in ggplot |
| [`ggnp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Number of Defects (np) Chart in ggplot |
| [`ggu`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Defects per Product (u) Chart in ggplot |
| [`cp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Capability Index (for centered, stable processes) |
| [`pp`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Process Performance Index (for centered, unstable processes) |
| [`cpk`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Capability Index (for uncentered, stable processes) |
| [`ppk`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Process Performance Index (for uncentered, unstable processes) |
| [`get_index`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py) | Bootstrap Process Capability/Performance Index with Confidence Intervals |

### `functions_factorial.py`

| Function | Description |
|----------|-------------|
| [`se_factorial`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.py) | Calculate Standard Error for Factorial Experiments |
| [`dbar_oneway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.py) | Calculate One-Way Treatment Effect |
| [`dbar_twoway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.py) | Calculate Two-Way Interaction Effect |
| [`dbar_threeway`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_factorial.py) | Calculate Three-Way Interaction Effect |

### `functions_crosstab.py` (Coming soon!)

| Function | Description |
|----------|-------------|
| [`crosstab`](https://github.com/timothyfraser/sysen/tree/main/functions/functions_crosstab.py) | Crosstabulate Data into intervals where r >= 5 |
