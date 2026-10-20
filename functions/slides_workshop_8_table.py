# Recitation 12 -- the restaurant tracking table (slide "Example: Restaurant Tracking System").
# Reads workshops/bistro_tracking.csv and prints the HTML <thead>/<tbody> the slide carries (Done = TRUE tinted blue, FALSE orange).
# Run from the top of the repo:  python functions/slides_workshop_8_table.py
import pandas as pd

d = pd.read_csv("workshops/bistro_tracking.csv", dtype = str)  # keep TRUE/FALSE as text
head = "".join(f"<th>{c.title()}</th>" for c in d.columns)
rows = "\n".join(
    "<tr>" + "".join(
        (f'<td class="{"t-b" if v == "TRUE" else "t-o"}">{v}</td>' if c == "done" else f"<td>{v}</td>")
        for c, v in r.items()) + "</tr>"
    for _, r in d.iterrows())
print(f"<thead><tr>{head}</tr></thead>\n<tbody>\n{rows}\n</tbody>")
