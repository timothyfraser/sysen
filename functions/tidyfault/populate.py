"""R's populate(): replace each 1 in a binary scenario table with that event's probability."""

from __future__ import annotations

import numpy as np
import pandas as pd


def populate(binary_outcomes, event_probs) -> pd.DataFrame:
    """Same shape and column order as ``binary_outcomes``; every event column
    becomes P(event) where it was 1 and 0 where it was 0. A ``scenario`` column
    passes through unchanged. ``event_probs`` needs columns ``event``, ``probability``."""
    if not isinstance(binary_outcomes, pd.DataFrame):
        raise TypeError("binary_outcomes must be a data frame.")
    if not isinstance(event_probs, pd.DataFrame):
        raise TypeError("event_probs must be a data frame.")
    if not {"event", "probability"} <= set(event_probs.columns):
        raise ValueError("event_probs must have columns 'event' and 'probability'.")
    event_cols = [c for c in binary_outcomes.columns if c != "scenario"]
    missing = [c for c in event_cols if c not in set(event_probs["event"])]
    if missing:
        raise ValueError("event_probs missing probabilities for events: " + ", ".join(missing))
    prob = dict(zip(event_probs["event"], event_probs["probability"].astype(float)))
    result = binary_outcomes.copy()
    for evt in event_cols:
        col = binary_outcomes[evt]
        result[evt] = np.where(col.isna(), np.nan, np.where(col == 1, prob[evt], 0.0))
    return result
