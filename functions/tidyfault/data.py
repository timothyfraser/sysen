"""The datasets bundled with R tidyfault, converted from data/*.rda to data/*.csv.

    from tidyfault.data import fakenodes, fakeedges     # attribute access
    tidyfault.load_data("db_probs")                      # by name
    tidyfault.data.available()                           # every name

``*_nodes`` tables get ``type`` back as a Categorical with R's levels
``top, and, or, not``. Whole-number columns (ids, 0/1 indicators) load as int64;
R stores them as double, the values are identical.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .tree import NODE_TYPES

DATA_DIR = Path(__file__).resolve().parent / "data"


def available():
    """Names of every bundled dataset."""
    return sorted(p.stem for p in DATA_DIR.glob("*.csv"))


def load_data(name: str) -> pd.DataFrame:
    """Load one bundled dataset by its R name (e.g. ``"fakenodes"``)."""
    path = DATA_DIR / f"{name}.csv"
    if not path.is_file():
        raise ValueError(f"no tidyfault dataset named {name!r}; available: {', '.join(available())}")
    df = pd.read_csv(path, keep_default_na=False, na_values=["NA"])
    if "type" in df.columns and {"id", "event"} <= set(df.columns):
        df["type"] = pd.Categorical(df["type"], categories=list(NODE_TYPES))
    return df


def __getattr__(name):
    if (DATA_DIR / f"{name}.csv").is_file():
        return load_data(name)
    raise AttributeError(f"module 'tidyfault.data' has no attribute {name!r}")
