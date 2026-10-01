"""tidyfault for Python: a faithful port of Tim Fraser and Jingyao Tong's R
package tidyfault (GPL-3). R is the reference: function names, column names and
return shapes match R. See README.md for the R | Python table."""

from . import data
from .calculate import calculate
from .concentrate import concentrate
from .curate import curate
from .data import load_data
from .equate import equate
from .formulate import Formula, formal_args, formulate
from .gates import gate, gate_and, gate_or, gate_top, get_gate
from .mocus import mocus, mocus_cpp, mocus_r, mocus_rcpp
from .populate import populate
from .quantify import quantify, quantify_binary, quantify_binary_fast, quantify_prob_fast
from .quantify_prob import quantify_prob
from .simulate import simulate
from .tabulate import tabulate
from .tree import GATE_TYPES, NODE_TYPES, as_edges, as_nodes, validate_tree

__version__ = "0.0.0.9"  # tracks the R package version it was ported from

__all__ = [
    # R exports ported so far (same names as R)
    "calculate", "concentrate", "curate", "equate", "formulate", "gate", "gate_and",
    "gate_or", "gate_top", "get_gate", "mocus", "mocus_cpp", "mocus_r", "mocus_rcpp",
    "populate", "quantify", "quantify_binary", "quantify_binary_fast", "quantify_prob",
    "quantify_prob_fast", "simulate", "tabulate",
    # Python-side helpers
    "Formula", "formal_args", "as_nodes", "as_edges", "validate_tree",
    "load_data", "NODE_TYPES", "GATE_TYPES",
]
from .illustrate import illustrate
from .plot import plot, to_png
__all__ += ["illustrate", "plot", "to_png"]
