# packages.R
# Tim Fraser

# What this script does:
# Installs the R packages the course workshops rely on. Run it ONCE, at the
# start of the term, from the repo root. After that you only ever need
# library(...) at the top of each workshop script.

# Inputs: none. It downloads from CRAN, so you need an internet connection.
# This takes a while the first time. Warnings about packages that were
# built under a different R version are usually safe to ignore.

# Install main classroom use packages
install.packages(
  c("tidyverse",
    "broom",
    "devtools",
    
    # Visualization packages
    "viridis",
    "ggtext",
    "shadowtext",
    "DiagrammeR",
    "ggpubr",
    "metR",
    
    # Statistical packages
    "mvtnorm",
    "PearsonDS",
    "moments",
    "texreg",
    "mosaicCalc",
    "rsm",
    "gtools",
    
    # Dashboards and APIs (the code/apps folder)
    "shiny",
    "plumber",
    
    # Sample data packages
    "gapminder",
    "nycflights13",
    "fivethirtyeight"))

# Install extra packages for visualization, etc.
install.packages(
  c("magick",
    "rsvg",
    "fontawesome",
    "cowplot",
    "knitr",
    "kableExtra",
    "rmdformats",
    "fidelius",
    "credentials")
)
