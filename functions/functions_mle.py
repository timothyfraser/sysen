# What this file is ----------------------------------------------------------
#
# Functions that fit a life distribution (exponential, Weibull, gamma or
# lognormal) to failure data by maximum likelihood, and then test the fit with
# chi-squared. They work on a cross-tabulation: a DataFrame with one row per
# time interval and the columns `lower`, `upper` and `r_obs` (the number of
# failures in that interval). They also work on a list of exact failure times.
#
# Units still running when the test ended are counted too. Tell the functions
# how many units were on test (`n_total`) and when the test stopped (`tmax`).
#
# The chi-squared test follows the eight steps in Tobias and Trindade, Applied
# Reliability (3rd ed., section 3.8). Its last cell runs from the end of the
# table to infinity and holds every unit that had not failed, so the expected
# counts add up to the number on test. Cells with fewer than 5 expected
# failures are merged with a neighbour before the statistic is added up.
#
# It is the Python twin of functions_mle.R: same arguments, same numbers.
# Python reserves the word lambda, so write lambda_ (with the underscore).
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_mle import get_fit
#
# Then try:
#   import pandas as pd
#   crops = pd.DataFrame({"lower": [0, 40, 80, 120, 160],
#                         "upper": [40, 80, 120, 160, 200],
#                         "r_obs": [18, 14, 10, 5, 3]})
#   get_fit(data = crops, n_total = 75, tmax = 200)  # does each family fit?
#
# You never need to edit anything below.
#
# What is in here:
#   plife(), dlife(), qlife(), rlife(), hlife()  the four distributions
#   get_mle()      fit one distribution
#   get_expected() observed and expected failures, by interval
#   get_chisq()    chi-squared test of a fit
#   get_fit()      fit and test all four distributions at once
#

import warnings
import numpy as np
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import norm, expon, weibull_min, gamma, chi2

# Parameter names, in order, for each distribution
_life_names = {
  "exponential": ["lambda"],
  "weibull": ["m", "c"],
  "gamma": ["k", "lambda"],
  "lognormal": ["t50", "sigma"],
}


def _life_args(dist, **params):
  # Check the distribution name, and pull out its parameters by name.
  # `lambda_` (or `lambda`) is stored as "lambda".
  if not isinstance(dist, str) or dist not in _life_names:
    shown = ", ".join(map(str, dist)) if isinstance(dist, (list, tuple)) else str(dist)
    raise ValueError("Unknown `dist`: '" + shown + "'. Use one of: "
                     + ", ".join(_life_names) + ".")
  a = {("lambda" if k == "lambda_" else k): v for k, v in params.items()}
  need = _life_names[dist]
  miss = [k for k in need if k not in a]
  if len(miss) > 0:
    shown_need = ", ".join("lambda_" if k == "lambda" else k for k in need)
    shown_miss = ", ".join("lambda_" if k == "lambda" else k for k in miss)
    raise ValueError("For dist = '" + dist + "', please supply: " + shown_need
                     + ". Missing: " + shown_miss + ".")
  return a


def _life_p(t, dist, a, upper = False, log = False):
  # Failure function F(t) (or reliability 1 - F(t) if upper), optionally logged
  t = np.asarray(t, dtype = float)
  with np.errstate(all = "ignore"):
    if dist == "exponential":
      d, x = expon, dict(scale = 1 / a["lambda"])
    elif dist == "weibull":
      d, x = weibull_min, dict(c = a["m"], scale = a["c"])
    elif dist == "gamma":
      d, x = gamma, dict(a = a["k"], scale = 1 / a["lambda"])
    else:
      d, x, t = norm, dict(), np.log(t / a["t50"]) / a["sigma"]
    if log:
      return d.logsf(t, **x) if upper else d.logcdf(t, **x)
    return d.sf(t, **x) if upper else d.cdf(t, **x)


def _life_d(t, dist, a):
  # Density f(t)
  t = np.asarray(t, dtype = float)
  with np.errstate(all = "ignore"):
    if dist == "exponential":
      return expon.pdf(t, scale = 1 / a["lambda"])
    if dist == "weibull":
      return weibull_min.pdf(t, c = a["m"], scale = a["c"])
    if dist == "gamma":
      return gamma.pdf(t, a = a["k"], scale = 1 / a["lambda"])
    return norm.pdf(np.log(t / a["t50"]) / a["sigma"]) / (t * a["sigma"])


def plife(t, dist, **params):
  """
  Failure function F(t) for any of the four life distributions.

  Parameters:
    t: a number or list of times
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    **params: the parameters, by course name: exponential lambda_;
      Weibull m (shape) and c (characteristic life); gamma k (shape) and
      lambda_ (rate); lognormal t50 (median) and sigma.

  Returns: a pandas Series of F(t).
  """
  # Testing values
  # plife(t = 500, dist = "lognormal", t50 = 1000, sigma = 0.8)
  a = _life_args(dist, **params)
  return pd.Series(np.atleast_1d(_life_p(t, dist, a)))


def dlife(t, dist, **params):
  """
  Density f(t) for any of the four life distributions.

  Parameters:
    t: a number or list of times
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    **params: the parameters, by course name (see plife)

  Returns: a pandas Series of f(t).
  """
  # Testing values
  # dlife(t = 500, dist = "weibull", m = 1.5, c = 1300)
  a = _life_args(dist, **params)
  return pd.Series(np.atleast_1d(_life_d(t, dist, a)))


def qlife(p, dist, **params):
  """
  Quantile: the time by which a share p of units has failed.

  Parameters:
    p: a number or list of probabilities between 0 and 1
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    **params: the parameters, by course name (see plife)

  Returns: a pandas Series of times.
  """
  # Testing values
  # qlife(p = 0.5, dist = "lognormal", t50 = 1000, sigma = 0.8)   # the median, 1000
  a = _life_args(dist, **params)
  p = np.asarray(p, dtype = float)
  if dist == "exponential":
    out = expon.ppf(p, scale = 1 / a["lambda"])
  elif dist == "weibull":
    out = weibull_min.ppf(p, c = a["m"], scale = a["c"])
  elif dist == "gamma":
    out = gamma.ppf(p, a = a["k"], scale = 1 / a["lambda"])
  else:
    out = a["t50"] * np.exp(a["sigma"] * norm.ppf(p))
  return pd.Series(np.atleast_1d(out))


def rlife(n, dist, **params):
  """
  Random failure times.

  Parameters:
    n: how many times to draw
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    **params: the parameters, by course name (see plife)

  Returns: a pandas Series of n times.
  """
  # Testing values
  # rlife(n = 5, dist = "exponential", lambda_ = 0.001)
  a = _life_args(dist, **params)
  if dist == "exponential":
    out = expon.rvs(scale = 1 / a["lambda"], size = n)
  elif dist == "weibull":
    out = weibull_min.rvs(c = a["m"], scale = a["c"], size = n)
  elif dist == "gamma":
    out = gamma.rvs(a = a["k"], scale = 1 / a["lambda"], size = n)
  else:
    out = a["t50"] * np.exp(a["sigma"] * norm.rvs(size = n))
  return pd.Series(np.atleast_1d(out))


def hlife(t, dist, **params):
  """
  Cumulative hazard H(t) = -log(1 - F(t)).

  Parameters:
    t: a number or list of times
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    **params: the parameters, by course name (see plife)

  Returns: a pandas Series of H(t).
  """
  # Testing values
  # hlife(t = 1000, dist = "exponential", lambda_ = 0.001)   # 1
  a = _life_args(dist, **params)
  # log of the reliability, computed directly so it stays accurate when F is tiny
  return pd.Series(np.atleast_1d(-_life_p(t, dist, a, upper = True, log = True)))


def _clean_crosstab(data):
  # Tidy a crosstab before anything else: right columns, numbers only, no gaps,
  # sorted by `lower`, no overlaps. Returns the sorted crosstab.
  if not isinstance(data, pd.DataFrame):
    raise ValueError("`data` must be a DataFrame with the columns `lower`, `upper` and `r_obs`.")
  cols = ["lower", "upper", "r_obs"]
  miss = [c for c in cols if c not in data.columns]
  if len(miss) > 0:
    raise ValueError("`data` is missing the column(s): " + ", ".join(miss)
                     + ". It needs `lower`, `upper` and `r_obs`.")
  bad = [c for c in cols if not (pd.api.types.is_numeric_dtype(data[c])
                                 and not pd.api.types.is_bool_dtype(data[c]))]
  if len(bad) > 0:
    raise ValueError("Column(s) " + ", ".join(bad) + " must be numbers, not text or factors. "
                     "Convert them with pd.to_numeric().")
  if data[cols].isna().any().any():
    raise ValueError("`lower`, `upper` and `r_obs` must not have missing (NA) values. "
                     "Remove or fill those rows.")
  if not np.isfinite(data["upper"].astype(float)).all():
    raise ValueError("`upper` must be finite in every row. Put units still running in `n_total`, "
                     "not in a last open interval.")
  if (data["r_obs"] < 0).any():
    raise ValueError("`r_obs` has a negative count. Failure counts must be 0 or more.")
  if (data["upper"] <= data["lower"]).any():
    raise ValueError("`upper` must be greater than `lower` in every row (found upper <= lower).")
  data = data.sort_values("lower", kind = "mergesort").reset_index(drop = True)
  if (data["lower"].to_numpy()[1:] < data["upper"].to_numpy()[:-1]).any():
    raise ValueError("Intervals overlap: a row starts before the previous one ends. "
                     "Each `lower` must be at or after the previous `upper`.")
  return data


def _check_data(data, t, n_total, tmax, np_):
  # Check the numbers that go with the data (call _clean_crosstab() first for a crosstab)
  if data is None and t is None:
    raise ValueError("Please supply either `data` (a crosstab) or `t` (a vector of failure times).")
  if (n_total is None or isinstance(n_total, (bool, str)) or not np.isscalar(n_total)
      or not np.isfinite(n_total)):
    raise ValueError("`n_total` must be a single number (not NA). Give the number of units on test.")
  if data is not None:
    if tmax is not None and ((data["r_obs"] > 0) & (data["upper"] > tmax)).any():
      raise ValueError("`tmax` (" + str(tmax) + ") falls before the end of an interval that holds failures. "
                       "`tmax` must be at or after the end of the last interval with failures.")
    r = data["r_obs"].sum()
    cells = int((data["r_obs"] > 0).sum())
  else:
    t = np.asarray(t)
    if not np.issubdtype(t.dtype, np.number) or np.isnan(t.astype(float)).any():
      raise ValueError("`t` must be numbers with no missing (NA) values.")
    if (t <= 0).any():
      raise ValueError("Failure times must be greater than 0. Remove zero or negative values from `t`.")
    if tmax is not None and (t > tmax).any():
      raise ValueError("Some failure times in `t` are after `tmax` (" + str(tmax)
                       + "). `tmax` must be at or after the last failure.")
    r = len(t)
    cells = r
  if n_total < r:
    raise ValueError("`n_total` (" + str(n_total) + ") is smaller than the number of failures ("
                     + str(r) + "). Give the total units on test.")
  if n_total > r:
    cells = cells + 1
  if cells < np_ + 1:
    raise ValueError("Too few non-empty cells (" + str(cells) + ") to fit " + str(np_)
                     + " parameter(s). Need at least " + str(np_ + 1)
                     + " (survivors cell included).")
  return True


def get_mle(data = None, t = None, n_total = None, tmax = None,
            dist = "exponential", lik = "interval"):
  """
  Fit a life distribution by maximum likelihood.

  Parameters:
    data: a DataFrame with `lower`, `upper`, `r_obs` (one row per interval)
    t: instead of `data`: a list of exact failure times
    n_total: units on test. Default: the number of failures (complete data).
    tmax: time the unfailed units were still running. Default: the largest
      `upper` (or the largest `t`). Time-censored: the planned end of the test.
      Failure-censored: the time of the last failure.
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    lik: "interval" (default) uses F(upper) - F(lower) for each interval;
      "midpoint" uses the density at each interval's midpoint. Ignored if you
      give `t`. `loglik` from the two forms cannot be compared.

  Returns: a one-row DataFrame: `dist`, the parameters (the rate is called
    `lambda`), `loglik`, `np`, `r`, `n_total`, `tmax`, `lik`, `converged`.
  """
  # Testing values
  # crops = pd.DataFrame({"lower": range(0, 200, 40), "upper": range(40, 201, 40), "r_obs": [18, 14, 10, 5, 3]})
  # get_mle(data = crops, n_total = 75, tmax = 200, dist = "weibull")   # m 0.832, c 172.9

  # Check the family first, so a typo gets a clear message
  if not (isinstance(dist, str) and dist in _life_names):
    _life_args(dist)
  names_par = _life_names[dist]
  n_par = len(names_par)
  if lik not in ("interval", "midpoint"):
    raise ValueError("Unknown `lik`: '" + str(lik) + "'. Use \"interval\" or \"midpoint\".")

  # Defaults for the number of units and the stopping time
  if data is not None:
    data = _clean_crosstab(data)
  elif t is not None:
    t = np.asarray(t, dtype = float)
  r = data["r_obs"].sum() if data is not None else (len(t) if t is not None else 0)
  if n_total is None:
    n_total = r
  if tmax is None and (data is not None or (t is not None and len(t) > 0)):
    tmax = data["upper"].max() if data is not None else t[np.isfinite(t)].max()
  _check_data(data, t, n_total, tmax, n_par)

  # Points and weights used for the starting values
  if data is not None:
    pts = ((data["lower"] + data["upper"]) / 2).to_numpy(dtype = float)
    wts = data["r_obs"].to_numpy(dtype = float)
  else:
    pts = t
    wts = np.ones(len(t))
  ok = (wts > 0) & (pts > 0)
  pts, wts = pts[ok], wts[ok]

  # Starting values from the midpoints
  lambda0 = r / ((pts * wts).sum() + (n_total - r) * tmax)
  mlog = (wts * np.log(pts)).sum() / wts.sum()
  slog = np.sqrt((wts * (np.log(pts) - mlog) ** 2).sum() / wts.sum())
  start = {"exponential": [lambda0],
           "weibull": [1, 1 / lambda0],
           "gamma": [1, lambda0],
           "lognormal": [np.exp(mlog), max(slog, 0.1)]}[dist]
  start = np.log(np.asarray(start, dtype = float))

  # Failures: only the rows that hold some
  if data is not None:
    d = data[data["r_obs"] > 0]
    lo, up = d["lower"].to_numpy(dtype = float), d["upper"].to_numpy(dtype = float)
    cnt = d["r_obs"].to_numpy(dtype = float)

  # Log-likelihood, written in terms of log(parameters) so they stay positive
  def loglik_fn(logpar):
    a = dict(zip(names_par, np.exp(logpar)))
    with np.errstate(all = "ignore"):
      # Units still running at tmax: log of the reliability. Dropped if none survive.
      surv = (n_total - r) * _life_p(tmax, dist, a, upper = True, log = True) if n_total > r else 0.0
      # Failures
      if data is not None:
        if lik == "interval":
          fail = (cnt * np.log(_life_p(up, dist, a) - _life_p(lo, dist, a))).sum()
        else:
          fail = (cnt * np.log(_life_d((lo + up) / 2, dist, a))).sum()
      else:
        fail = np.log(_life_d(t, dist, a)).sum()
    out = float(fail + surv)
    return out if np.isfinite(out) else -1e10

  # Maximise: one parameter, a one-dimensional search; two, Nelder-Mead
  if n_par == 1:
    o = minimize_scalar(lambda x: -loglik_fn(np.array([x])), method = "bounded",
                        bounds = (start[0] - 10, start[0] + 10),
                        options = dict(xatol = 1e-10))
    par, value = np.array([o.x]), -o.fun
  else:
    o = minimize(lambda x: -loglik_fn(x), x0 = start, method = "Nelder-Mead",
                 options = dict(xatol = 1e-10, fatol = 1e-10, maxiter = 5000, maxfev = 10000))
    par, value = o.x, -o.fun

  est = dict(zip(names_par, np.exp(par)))
  out = {"dist": dist}
  out.update(est)
  out.update({"loglik": value, "np": n_par,
              "r": r, "n_total": n_total, "tmax": tmax, "lik": lik,
              "converged": bool(o.success and value > -1e10)})
  return pd.DataFrame([out])


def _chisq_cells(tab, n_total, f, **kwargs):
  # The cells of the chi-squared test: the table's intervals in time order, an
  # empty cell for any stretch of time the table skips (from 0 to the first
  # interval, or between two intervals), and one last cell from the end of the
  # table to infinity holding the units that had not failed (n_total - r).
  # Expected count = n_total times the chance of failing in the cell, so the
  # expected counts add up to n_total.
  tab = tab[["lower", "upper", "r_obs"]].sort_values("lower", kind = "mergesort")
  lo, up = tab["lower"].to_numpy(dtype = float), tab["upper"].to_numpy(dtype = float)
  gaps = pd.DataFrame({"lower": np.concatenate([[0.0], up[:-1]]), "upper": lo, "r_obs": 0.0})
  gaps = gaps[gaps["upper"] > gaps["lower"]]
  last = pd.DataFrame({"lower": [up.max()], "upper": [np.inf],
                       "r_obs": [n_total - tab["r_obs"].sum()]})
  cells = pd.concat([tab.astype(float), gaps, last], ignore_index = True)
  cells = cells.sort_values("lower", kind = "mergesort").reset_index(drop = True)

  def fv(x):
    return np.asarray(f(x, **kwargs), dtype = float)

  upper = cells["upper"].to_numpy()
  fin = np.isfinite(upper)
  p_upper = np.ones(len(cells))
  p_upper[fin] = fv(upper[fin])
  cells["p_fail"] = p_upper - fv(cells["lower"].to_numpy())
  cells["r_exp"] = n_total * cells["p_fail"]
  return cells[["lower", "upper", "r_obs", "p_fail", "r_exp"]]


def _pool_cells(cells):
  # Merge thin cells: take the last cell with an expected count under 5 and
  # join it to the cell before it (the first cell joins the one after it).
  # Repeat until every expected count is at least 5, or one cell is left.
  cells = cells.reset_index(drop = True)
  while len(cells) > 1:
    thin = np.flatnonzero(cells["r_exp"].to_numpy() < 5)
    if len(thin) == 0:
      break
    i = thin.max()
    a = 0 if i == 0 else i - 1
    b = a + 1
    merged = pd.DataFrame([{
      "lower": cells["lower"][a], "upper": cells["upper"][b],
      "r_obs": cells["r_obs"][a] + cells["r_obs"][b],
      "p_fail": cells["p_fail"][a] + cells["p_fail"][b],
      "r_exp": cells["r_exp"][a] + cells["r_exp"][b]}])
    cells = pd.concat([cells.iloc[:a], merged, cells.iloc[b + 1:]], ignore_index = True)
  return cells


def get_expected(data, n_total = None, dist = "exponential", pooled = False, **params):
  """
  Observed and expected failures by cell.

  Parameters:
    data: a DataFrame with `lower`, `upper`, `r_obs`
    n_total: units on test. Default: the number of failures.
    dist: one of "exponential", "weibull", "gamma", "lognormal"
    pooled: if False (default), one row per interval, plus a row for any time
      the table skips and a last row (`upper` = inf) for the units that had not
      failed. If True, the cells after merging, exactly as get_chisq() uses them.
    **params: the parameters, by course name (see plife)

  Returns: a DataFrame: `lower`, `upper`, `r_obs`, `p_fail`, `r_exp`.
    The `r_exp` column adds up to `n_total`.
  """
  # Testing values
  # crops = pd.DataFrame({"lower": range(0, 200, 40), "upper": range(40, 201, 40), "r_obs": [18, 14, 10, 5, 3]})
  # get_expected(crops, n_total = 75, dist = "exponential", lambda_ = 0.00595)
  a = _life_args(dist, **params)
  data = _clean_crosstab(data)
  if n_total is None:
    n_total = data["r_obs"].sum()
  _check_data(data, None, n_total, None, 0)
  cells = _chisq_cells(data, n_total = n_total, f = lambda t: _life_p(t, dist, a))
  if pooled:
    cells = _pool_cells(cells)
  return cells


def _bin_times(t, binwidth):
  # Tally failures by interval of width `binwidth`, starting at 0, (lower, upper]
  t = np.asarray(t, dtype = float)
  n_bins = int(np.ceil(t.max() / binwidth))
  breaks = np.arange(n_bins + 1) * binwidth
  idx = np.clip(np.searchsorted(breaks, t, side = "left") - 1, 0, n_bins - 1)
  return pd.DataFrame({"lower": breaks[:-1], "upper": breaks[1:],
                       "r_obs": np.bincount(idx, minlength = n_bins)})


def _chisq_stat(obs, exp):
  # sum of (observed - expected)^2 / expected
  with np.errstate(all = "ignore"):
    return float(((obs - exp) ** 2 / exp).sum())


def get_chisq(t = None, binwidth = 5, data = None, n_total = None, f = None, np = 1, **kwargs):
  """
  Chi-squared test of a fitted failure function.

  If observed vector...
    t: a list of times to failure
    binwidth: size of intervals (eg. 5 hours) (only if t is provided)
  If cross-tabulated data...
    data: a DataFrame with the columns `lower`, `upper`, and `r_obs`
  Common parameters:
    n_total: total number of units. Default: the number of failures.
    f: specific failure function, such as f = pexp
    np: total number of parameters in your function (eg. if exponential, 1)
    **kwargs: fill in here any named parameters f needs, like rate = 2.3 or mean = 0, sd = 2

  The test follows Tobias and Trindade, Applied Reliability (3rd ed., section
  3.8): a last cell from the end of the table to infinity holds the units that
  had not failed, and cells with fewer than 5 expected failures are merged
  before adding up.

  Censored test? Pass a crosstab (`data`) whose last interval ends when the
  test stopped, or use get_fit(), which trims the table at `tmax` for you.

  Returns: a one-row DataFrame: `chisq`, `nbin` (cells after merging), `np`,
    `df`, `p_value`, and `min_exp` (the smallest expected count).
  """
  # Testing values
  # masks = pd.read_csv("workshops/masks.csv")
  # get_chisq(t = masks["left_earloop"], binwidth = 5, n_total = 50, f = pexp, np = 1, rate = 1 / masks["left_earloop"].mean())

  # Part 1: Count failures by interval
  if t is not None:
    tab = _bin_times(t, binwidth)
  elif data is not None:
    tab = _clean_crosstab(data)
  else:
    raise ValueError("Please supply either `t` (failure times) or `data` (a crosstab).")
  if f is None:
    raise ValueError("Please supply `f`, a failure function such as f = pexp.")
  if n_total is None:
    n_total = tab["r_obs"].sum()
  if n_total < tab["r_obs"].sum():
    raise ValueError("`n_total` (" + str(n_total) + ") is smaller than the number of failures ("
                     + str(tab["r_obs"].sum()) + ").")

  # Part 2: Expected failures in each cell, plus a last cell (to infinity)
  # for the n_total - r units that had not failed
  cells = _chisq_cells(tab, n_total = n_total, f = f, **kwargs)

  # Part 3: Merge cells until every expected count is at least 5
  cells = _pool_cells(cells)

  # Part 4: Calculate Chi-Squared statistic, degrees of freedom and p-value
  obs, exp = cells["r_obs"].to_numpy(), cells["r_exp"].to_numpy()
  chisq = _chisq_stat(obs, exp)
  nbin = len(cells)
  df = nbin - np - 1
  p_value = float(chi2.sf(chisq, df)) if df >= 1 else float("nan")

  # A test needs at least one degree of freedom
  if df < 1:
    warnings.warn("Only " + str(df) + " degrees of freedom after merging cells, so p_value is NA. "
                  "Use narrower intervals or a longer test, so more cells hold 5 or more expected failures.",
                  UserWarning)

  return pd.DataFrame({"chisq": [chisq], "nbin": [nbin], "np": [np], "df": [df],
                       "p_value": [p_value], "min_exp": [float(exp.min())]})


def get_fit(data, n_total = None, tmax = None,
            dist = ("exponential", "weibull", "gamma", "lognormal"),
            lik = "interval"):
  """
  Fit and test each life distribution.

  Parameters:
    data: a DataFrame with `lower`, `upper`, `r_obs`
    n_total: units on test. Default: the number of failures.
    tmax: time the unfailed units were still running. Default: the largest `upper`.
    dist: one or more of "exponential", "weibull", "gamma", "lognormal" (default: all four)
    lik: "interval" (default) or "midpoint" (see get_mle)

  Returns: a DataFrame, one row per distribution, sorted by `loglik`, highest first: `dist`,
    `par1`, `est1`, `par2`, `est2`, `loglik`, `chisq`, `nbin`, `np`,
    `df`, `p_value`, `min_exp`, `converged`. A small p_value rules a
    distribution out. Among those left, the highest `loglik` fits best (here the lowest chi-squared usually agrees).
  """
  # Testing values
  # crops = pd.DataFrame({"lower": range(0, 200, 40), "upper": range(40, 201, 40), "r_obs": [18, 14, 10, 5, 3]})
  # get_fit(data = crops, n_total = 75, tmax = 200)
  data = _clean_crosstab(data)
  if n_total is None:
    n_total = data["r_obs"].sum()
  if tmax is None:
    tmax = data["upper"].max()
  _check_data(data, None, n_total, tmax, 0)
  # Keep only rows that end by tmax (the rest are empty), so the last cell
  # of the chi-squared test begins where the likelihood censors
  data = data[data["upper"] <= tmax].reset_index(drop = True)
  if len(data) == 0:
    raise ValueError("No interval ends by `tmax`. Check `tmax` and the `upper` column.")
  if data["lower"][0] > 0:
    warnings.warn("The first interval starts at " + str(data["lower"][0]) + ", not 0: "
                  "the chi-squared test adds an empty cell from 0.", UserWarning)
  if isinstance(dist, str):
    dist = [dist]

  def one(d):
    m = get_mle(data = data, n_total = n_total, tmax = tmax, dist = d, lik = lik)
    pars = _life_names[d]
    est = [float(m[p][0]) for p in pars]
    pl = dict(zip(pars, est))
    # Failure function at the fitted parameters
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      ch = get_chisq(data = data, n_total = n_total, f = lambda t: _life_p(t, d, pl), np = len(pars))
    # A test needs at least one degree of freedom
    if ch["df"][0] < 1:
      warnings.warn("Only " + str(ch["df"][0]) + " degrees of freedom for " + d
                    + " after merging cells: p_value set to NA.", UserWarning)
    return {"dist": d, "par1": pars[0], "est1": est[0],
            "par2": pars[1] if len(pars) > 1 else None,
            "est2": est[1] if len(pars) > 1 else np.nan,
            "loglik": m["loglik"][0],
            "chisq": ch["chisq"][0], "nbin": ch["nbin"][0], "np": ch["np"][0],
            "df": ch["df"][0], "p_value": ch["p_value"][0], "min_exp": ch["min_exp"][0],
            "converged": bool(m["converged"][0])}

  # One family that cannot be fitted must not stop the others
  def failed_row(d, why):
    warnings.warn("Could not fit " + str(d) + ": " + why, UserWarning)
    pars = _life_names.get(d)
    return {"dist": d, "par1": pars[0] if pars else None, "est1": np.nan,
            "par2": pars[1] if pars and len(pars) > 1 else None, "est2": np.nan,
            "loglik": np.nan, "chisq": np.nan, "nbin": np.nan,
            "np": np.nan, "df": np.nan, "p_value": np.nan, "min_exp": np.nan,
            "converged": False}

  rows, whys = [], []
  for d in dist:
    try:
      rows.append(one(d))
      whys.append(None)
    except Exception as e:
      whys.append(str(e))
      rows.append(failed_row(d, str(e)))
  if all(w is not None for w in whys):
    raise ValueError(whys[0])

  out = pd.DataFrame(rows)
  for c in ["nbin", "np", "df"]:
    out[c] = out[c].astype("Int64")
  return out.sort_values("loglik", ascending = False, kind = "mergesort", na_position = "last").reset_index(drop = True)
