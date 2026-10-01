"""tidyfault for Python: a faithful port of Tim Fraser and Jingyao Tong's R
package tidyfault (GPL-3). R is the reference: function names, column names and
return shapes match R. See README.md for the R | Python table."""

from . import data
from .calculate import calculate
from .curate import curate
from .data import load_data
from .equate import equate
from .formulate import Formula, formal_args, formulate
from .gates import gate, gate_and, gate_or, gate_top, get_gate
from .populate import populate
from .quantify_prob import quantify_prob
from .tabulate import tabulate
from .tree import GATE_TYPES, NODE_TYPES, as_edges, as_nodes, validate_tree

__version__ = "0.0.0.9"  # tracks the R package version it was ported from

__all__ = [
    # R exports ported so far (same names as R)
    "calculate", "curate", "equate", "formulate", "gate", "gate_and", "gate_or",
    "gate_top", "get_gate", "populate", "quantify_prob", "tabulate",
    # Python-side helpers
    "Formula", "formal_args", "as_nodes", "as_edges", "validate_tree",
    "load_data", "NODE_TYPES", "GATE_TYPES",
]
