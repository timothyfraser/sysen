# What this file is ----------------------------------------------------------
#
# One helper, plan_test(), that plans a reliability life test. Give it the
# life distribution and all but one of the planning pieces, and it solves for
# the missing piece: how many units to test (n), how long to test them (t),
# how many failures you can allow (r), how confident you can be (ci), or the
# life parameter the test is able to demonstrate.
#
# It works for four life distributions: exponential, weibull, gamma, lognormal.
# It is the Python twin of functions_planning.R: same arguments, same numbers.
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_planning import plan_test
#
# Then try:
#   plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda_ = 1 / 500000)
#   plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)
#
# Python reserves the word lambda, so write lambda_ (with the underscore).
# The shape parameter (m, k or sigma) has to be assumed from earlier data.
# Write ci by name, as ci = 0.90.
#
# Set exact = True for the exact method. It counts failures with the binomial
# distribution: each unit either fails during the test or does not.
#
# You never need to edit anything below.
#

import warnings
import numpy as np
import pandas as pd
from scipy.stats import norm, gamma, chi2, binom, beta

# Parameter names for each family.
# Exponential: lambda (scale only). Weibull: m (shape), c (scale).
# Gamma: k (shape), lambda (rate). Lognormal: sigma (shape), t50 (scale).
_plan_shape = {"exponential": None, "weibull": "m", "gamma": "k", "lognormal": "sigma"}
_plan_scale = {"exponential": "lambda", "weibull": "c", "gamma": "lambda", "lognormal": "t50"}
# Column order for the life parameters, as the course names them
_plan_order = {"exponential": ["lambda"], "weibull": ["m", "c"],
               "gamma": ["k", "lambda"], "lognormal": ["t50", "sigma"]}


def _plan_h(t, dist, p):
  # Cumulative hazard H(t) = -log(1 - F(t)), accurate even when F is tiny
  if dist == "exponential":
    return p["lambda"] * t
  if dist == "weibull":
    return (t / p["c"]) ** p["m"]
  if dist == "gamma":
    return -gamma.logsf(t, a = p["k"], scale = 1 / p["lambda"])
  return -norm.logsf(np.log(t / p["t50"]) / p["sigma"])


def _plan_f(t, dist, p):
  # Failure function F(t): the chance a unit has failed by time t
  if dist == "exponential":
    return -np.expm1(-p["lambda"] * t)
  if dist == "weibull":
    return -np.expm1(-(t / p["c"]) ** p["m"])
  if dist == "gamma":
    return gamma.cdf(t, a = p["k"], scale = 1 / p["lambda"])
  return norm.cdf(np.log(t / p["t50"]) / p["sigma"])


def _plan_q(f, dist, p):
  # Quantile function: the time by which a share f of units have failed
  if dist == "exponential":
    return -np.log1p(-f) / p["lambda"]
  if dist == "weibull":
    return p["c"] * (-np.log1p(-f)) ** (1 / p["m"])
  if dist == "gamma":
    return gamma.ppf(f, a = p["k"], scale = 1 / p["lambda"])
  return p["t50"] * np.exp(p["sigma"] * norm.ppf(f))


def _plan_scale_solve(f_need, s, dist, p):
  # The scale parameter a test can demonstrate, given the failure share f_need
  # it must show by time s = t * af (the shape stays as assumed)
  if dist == "exponential":
    return -np.log1p(-f_need) / s
  if dist == "weibull":
    return s / (-np.log1p(-f_need)) ** (1 / p["m"])
  if dist == "gamma":
    return gamma.ppf(f_need, a = p["k"], scale = 1) / s
  return s / np.exp(p["sigma"] * norm.ppf(f_need))


def _plan_a(ci, r):
  # A = qchisq(ci, df = 2 * (r + 1)) / 2, vectorized over r and ci.
  # For r of 1 or more, A equals r * qk(p = ci, r = r, .time = True).
  # For r = 0, A equals -log(1 - ci).
  return chi2.ppf(ci, df = 2 * (np.asarray(r, dtype = float) + 1)) / 2


def _plan_one(x, dist, solved, exact):
  # Plan one test (one row of inputs). `x` is a dict holding n, t, r, ci, af and
  # the life parameters; the missing piece is nan and `solved` names it.
  # Testing values
  # x = {"n": np.nan, "t": 5000, "r": 5, "ci": 0.9, "af": 1, "lambda": 1/500000}
  # dist = "exponential"; solved = "n"; exact = False
  p = {k: x[k] for k in _plan_order[dist]}
  n, t, r, ci, af = x["n"], x["t"], x["r"], x["ci"], x["af"]

  if solved == "n":
    h = _plan_h(t * af, dist, p)
    if not exact:
      n = _plan_a(ci, r) / h
    else:
      # smallest n whose binomial chance of r or fewer failures is at most 1 - ci
      f = _plan_f(t * af, dist, p)
      top = int(np.ceil(4 * _plan_a(ci, r) / h)) + 100
      if top >= 1e7:
        raise ValueError("the exact search needs too many units; try a longer test")
      cand = np.arange(int(r) + 1, top + 1)
      hit = cand[binom.cdf(r, cand, f) <= 1 - ci]
      n = float(hit[0]) if len(hit) > 0 else np.nan
  if solved == "t":
    f_need = -np.expm1(-_plan_a(ci, r) / n) if not exact else beta.ppf(ci, r + 1, n - r)
    t = _plan_q(f_need, dist, p) / af
  if solved == "r":
    h = _plan_h(t * af, dist, p)
    cand = np.arange(0, int(np.floor(n)) + 1)
    if not exact:
      ok = _plan_a(ci, cand) <= n * h
    else:
      ok = binom.cdf(cand, n, _plan_f(t * af, dist, p)) <= 1 - ci
    r = float(cand[ok].max()) if ok.any() else np.nan
    if np.isnan(r):
      warnings.warn("No number of allowed failures meets this plan; use more units, a longer test, or less confidence.")
  if solved == "ci":
    if not exact:
      ci = chi2.cdf(2 * n * _plan_h(t * af, dist, p), df = 2 * (r + 1))
    else:
      ci = 1 - binom.cdf(r, n, _plan_f(t * af, dist, p))
  if solved in _plan_scale.values():
    f_need = -np.expm1(-_plan_a(ci, r) / n) if not exact else beta.ppf(ci, r + 1, n - r)
    p[solved] = _plan_scale_solve(f_need, t * af, dist, p)

  n_up = np.ceil(n - 1e-9)
  if solved == "n" and not np.isnan(n) and n <= r:
    n_up = r + 1
    warnings.warn("The plan needs more units than allowed failures (n is at or below r), so n_up is set to r + 1.")
  f_t = _plan_f(t * af, dist, p)
  a = np.nan if (np.isnan(r) or np.isnan(ci)) else float(_plan_a(ci, r))
  row = {"dist": dist}
  row.update({k: float(v) for k, v in p.items()})
  row.update({"n": float(n), "n_up": float(n_up), "t": float(t), "r": float(r), "ci": float(ci),
              "af": float(af), "F_t": float(f_t), "A": a, "solved": solved,
              "method": "exact" if exact else "k-factor"})
  return row


def plan_test(dist = "exponential", n = None, t = None, r = None, ci = None,
              af = 1, exact = False, **params):
  """
  Plan a reliability life test. Leave out exactly one of n, t, r, ci, or the
  scale parameter, and it is solved for. The shape parameter (m, k, sigma) can
  never be the one left out.

  Parameters:
    dist: "exponential", "weibull", "gamma", or "lognormal"
    n: number of units on test
    t: test time (in the same units as the life parameters)
    r: number of failures allowed during the test (0 or more)
    ci: confidence level, between 0 and 1 (name it: ci = 0.90)
    af: acceleration factor; t hours at stress count as t * af hours of use
    exact: use the exact answer instead of the k-factor formula? The exact
      method counts failures with the binomial distribution (each unit either
      fails during the test or does not).
    **params: the life parameters, by name:
      exponential: lambda_; weibull: m (shape), c (scale);
      gamma: k (shape), lambda_ (rate); lognormal: t50 (median life), sigma (shape)
      Each can be one number or a list; lists recycle to one row each.

  Returns:
    a pandas DataFrame, one row per plan: dist, the life parameters, n, n_up
    (n rounded up), t, r, ci, af, F_t, A, solved, method
  """
  # Python reserves the word lambda, so lambda_ is the Python spelling
  params = {("lambda" if k == "lambda_" else k): v for k, v in params.items()}

  # Input error handling
  if not (isinstance(dist, str) and dist in _plan_scale):
    raise ValueError("dist must be one of exponential, weibull, gamma, lognormal")
  if not isinstance(exact, (bool, np.bool_)):
    raise ValueError("exact must be True or False")
  shape = _plan_shape[dist]
  scale = _plan_scale[dist]
  need = [v for v in (shape, scale) if v is not None]
  scale_py = "lambda_" if scale == "lambda" else scale
  extra = [k for k in params if k not in need]
  if len(extra) > 0:
    raise ValueError(f'For dist = "{dist}", the life parameters are: {", ".join(need)}. '
                     f"Name each one, e.g. {scale_py} = 1000.")
  if shape is not None and shape not in params:
    raise ValueError(f"The shape parameter {shape} is missing. It cannot be solved for; "
                     f"assume a value for {shape}.")

  # Which one piece is missing?
  given = {"n": n, "t": t, "r": r, "ci": ci, scale: params.get(scale)}
  missing = [k for k, v in given.items() if v is None]
  if len(missing) != 1:
    raise ValueError(f"Leave out exactly one of n, t, r, ci, or {scale}, and it will be solved for. "
                     f"You left out {len(missing)}.")
  solved = missing[0]

  # Put all inputs side by side; vectors recycle to one row each
  inputs = {k: v for k, v in given.items() if v is not None}
  inputs.update({k: v for k, v in params.items() if k != scale})
  inputs["af"] = af
  arrays = {}
  for k, v in inputs.items():
    try:
      a = np.atleast_1d(np.asarray(v, dtype = float))
    except (TypeError, ValueError):
      a = np.array([np.nan])
    arrays[k] = a
  bad = [k for k, a in arrays.items() if not np.all(np.isfinite(a))]
  if bad:
    raise ValueError("Every input must be a finite number, with no NA, NaN, Inf or text. Check: "
                     + ", ".join(bad) + ".")
  sizes = {a.size for a in arrays.values()} - {1}
  if len(sizes) > 1:
    raise ValueError("Vector inputs must all have the same length (or length 1).")
  size = sizes.pop() if sizes else 1
  inputs = {k: np.resize(a, size) if a.size == 1 else a for k, a in arrays.items()}
  inputs[solved] = np.full(size, np.nan)

  def has(key, test):
    return key in inputs and bool(np.any(test(inputs[key])[~np.isnan(inputs[key])]))
  if has("n", lambda v: v <= 0):
    raise ValueError("n must be greater than 0. Change n to at least 1 unit.")
  if has("t", lambda v: v <= 0):
    raise ValueError("t must be greater than 0. Change t to a positive test time.")
  if any(has(v, lambda a: a <= 0) for v in need):
    raise ValueError(f"The life parameters ({', '.join(need)}) must all be greater than 0.")
  nn, rr = inputs.get("n"), inputs.get("r")
  if nn is not None and rr is not None:
    both = ~np.isnan(nn) & ~np.isnan(rr)
    if np.any(nn[both] <= rr[both]):
      raise ValueError("n must be larger than r: you cannot allow as many failures as units. Raise n or lower r.")
  if exact and has("n", lambda v: v != np.round(v)):
    raise ValueError("With exact = True, n must be a whole number.")
  if has("af", lambda v: v <= 0):
    raise ValueError("af must be positive.")
  if has("ci", lambda v: (v <= 0) | (v >= 1)):
    raise ValueError("ci must be between 0 and 1.")
  if has("r", lambda v: (v < 0) | (v != np.round(v))):
    raise ValueError("r must be a whole number, 0 or more.")

  rows = [_plan_one({k: v[i] for k, v in inputs.items()}, dist, solved, exact)
          for i in range(size)]
  out = pd.DataFrame(rows)

  if not exact and (out["F_t"] > 0.10).any():
    warnings.warn("F_t is above 0.10 (many units fail during the test), so the k-factor formula is loose. "
                  "Try exact = True for the exact binomial answer.")
  return out

# Examples
# plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda_ = 1 / 500000)     # solves n
# plan_test("exponential", n = 100, r = 10, ci = 0.95, lambda_ = 1 / 20000)      # solves t
# plan_test("exponential", n = 50, t = 2000, ci = 0.80, lambda_ = 0.00005)       # solves r
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)       # solves n
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2, exact = True)
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = [1.5, 2, 2.5])
