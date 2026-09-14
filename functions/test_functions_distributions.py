# Tests for the t-distribution helpers in functions_distributions.py
#
# Run them, from the top of the project folder:
#   python -m pytest functions/test_functions_distributions.py -v
#
# The reference numbers below were printed by R 4.5.2 at 10 decimal places, so
# these tests check the promise the helper library actually makes to students:
# dt/pt/qt/rt in Python give you the same answer as dt/pt/qt/rt in R.
#
#   dt(0, df = 1)                 0.3183098862
#   dt(1, df = 10)                0.2303619892
#   dt(1.5, df = 7)               0.1262630613
#   dt(0, df = 10, ncp = 2)       0.0526600934
#   pt(2, df = 5)                 0.9490302606
#   pt(-1, df = 30)               0.1626543077
#   pt(c(-2,-1,0,1,2), df = 8)    0.0402581190 0.1732967535 0.5000000000
#                                 0.8267032465 0.9597418810
#   qt(0.975, df = 10)            2.2281388520
#   qt(0.95, df = 30)             1.6972608866
#   qt(c(0.025,0.5,0.975), df=8) -2.3060041352 0.0000000000 2.3060041352

import sys
from pathlib import Path

import pytest
from pandas import Series
from scipy.stats import t as scipy_t

# Let the tests import the library the same way a student would.
sys.path.append(str(Path(__file__).resolve().parent))

from functions_distributions import dt, pt, qt, rt, pnorm


# Agreement with R #################################################

class TestAgainstR:
    def test_dt_matches_r(self):
        assert dt(0, df=1)[0] == pytest.approx(0.3183098862, abs=1e-10)
        assert dt(1, df=10)[0] == pytest.approx(0.2303619892, abs=1e-10)
        assert dt(1.5, df=7)[0] == pytest.approx(0.1262630613, abs=1e-10)

    def test_pt_matches_r(self):
        assert pt(2, df=5)[0] == pytest.approx(0.9490302606, abs=1e-10)
        assert pt(-1, df=30)[0] == pytest.approx(0.1626543077, abs=1e-10)

    def test_qt_matches_r(self):
        assert qt(0.975, df=10)[0] == pytest.approx(2.2281388520, abs=1e-9)
        assert qt(0.95, df=30)[0] == pytest.approx(1.6972608866, abs=1e-9)

    def test_dt_with_ncp_matches_r(self):
        # R: dt(0, df = 10, ncp = 2)
        assert dt(0, df=10, ncp=2)[0] == pytest.approx(0.0526600934, abs=1e-10)

    def test_vectorised_pt_matches_r(self):
        expected = [0.0402581190, 0.1732967535, 0.5000000000,
                    0.8267032465, 0.9597418810]
        assert pt([-2, -1, 0, 1, 2], df=8).tolist() == pytest.approx(expected, abs=1e-10)

    def test_vectorised_qt_matches_r(self):
        expected = [-2.3060041352, 0.0000000000, 2.3060041352]
        assert qt([0.025, 0.5, 0.975], df=8).tolist() == pytest.approx(expected, abs=1e-9)


# Agreement with scipy #############################################

class TestAgainstScipy:
    def test_dt_matches_scipy(self):
        assert dt(1.5, df=7)[0] == pytest.approx(scipy_t.pdf(1.5, df=7))

    def test_pt_matches_scipy(self):
        assert pt(1.5, df=7)[0] == pytest.approx(scipy_t.cdf(1.5, df=7))

    def test_qt_matches_scipy(self):
        assert qt(0.9, df=7)[0] == pytest.approx(scipy_t.ppf(0.9, df=7))


# R-shaped conventions #############################################

class TestConventions:
    def test_scalar_input_returns_a_series(self):
        # Tim's ruling: these helpers return a pandas Series even for a
        # scalar, exactly like dnorm/pnorm/qnorm/rnorm already do.
        for value in (dt(0, df=5), pt(0, df=5), qt(0.5, df=5)):
            assert isinstance(value, Series)
            assert len(value) == 1

    def test_vector_input_returns_a_series_of_the_same_length(self):
        x = [-2, -1, 0, 1, 2]
        for value in (dt(x, df=8), pt(x, df=8)):
            assert isinstance(value, Series)
            assert len(value) == len(x)

        p = [0.025, 0.5, 0.975]
        value = qt(p, df=8)
        assert isinstance(value, Series)
        assert len(value) == len(p)

    def test_pt_is_the_lower_tail_like_r(self):
        # R's pt() is P(T <= q), not the upper tail.
        assert pt(0, df=9)[0] == pytest.approx(0.5)
        assert pt(3, df=9)[0] > 0.5

    def test_qt_takes_a_probability_and_inverts_pt(self):
        assert qt(pt(1.3, df=12)[0], df=12)[0] == pytest.approx(1.3)

    def test_rt_returns_n_draws(self):
        draws = rt(50, df=6)
        assert isinstance(draws, Series)
        assert len(draws) == 50

    def test_dt_is_symmetric(self):
        assert dt(-1.7, df=4)[0] == pytest.approx(dt(1.7, df=4)[0])


# Sanity checks on the shape of the distribution ###################

class TestBehaviour:
    def test_t_converges_on_the_normal_as_df_grows(self):
        assert pt(1.96, df=100000)[0] == pytest.approx(pnorm(1.96)[0], abs=1e-4)

    def test_t_has_fatter_tails_than_the_normal(self):
        # More probability beyond 2 sd under t(5) than under the normal.
        assert (1 - pt(2, df=5)[0]) > (1 - pnorm(2)[0])

    def test_dt_ncp_zero_is_the_central_t(self):
        assert dt(0, df=10, ncp=0)[0] == pytest.approx(dt(0, df=10)[0])
