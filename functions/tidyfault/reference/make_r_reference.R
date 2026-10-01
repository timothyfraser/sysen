# make_r_reference.R -- regenerate r_reference.json, the R outputs that the
# Python port of tidyfault is tested against (tests/test_tidyfault_core.py).
#
# R is the reference. This script SOURCES the R functions the port mirrors
# straight from a tidyfault source checkout (https://github.com/timothyfraser/tidyfault),
# so the fixtures describe exactly that source, not whatever build is installed.
# The installed tidyfault is used for one thing only: concentrate() (compiled
# MOCUS), whose minimal cutsets feed tabulate().
#
# Usage (from this folder):
#   Rscript make_r_reference.R <path-to-tidyfault-source> r_reference.json
# Needs: dplyr, stringr, tidyr, tibble, scales, jsonlite, tidyfault.

args <- commandArgs(trailingOnly = TRUE)
src <- if (length(args) >= 1) args[[1]] else "."
out <- if (length(args) >= 2) args[[2]] else "r_reference.json"

suppressPackageStartupMessages({
  library(dplyr); library(stringr); library(tidyr); library(tibble)
  library(scales); library(jsonlite)
})
for (f in c("curate", "equate", "formulate", "calculate", "tabulate", "populate",
            "quantify_prob", "gate", "gate_and", "gate_or", "gate_top", "get_gate")) {
  source(file.path(src, "R", paste0(f, ".R")))
}
ld <- function(name) { e <- new.env(); load(file.path(src, "data", paste0(name, ".rda")), envir = e); e[[name]] }
num <- function(x) sprintf("%.17g", x)   # full double precision, parsed back with float()

# the minimal OR-top tree from tests/testthat/helper-trees.R
minimal <- list(
  nodes = tibble(id = 1:3, event = c("T", "A", "B"),
                 type = factor(c("top", "not", "not"), levels = c("top", "and", "or", "not"))),
  edges = tibble(from = c(1L, 1L), to = c(2L, 3L)))

trees <- list(
  minimal     = list(nodes = minimal$nodes, edges = minimal$edges, probs = NULL),
  fake        = list(nodes = ld("fakenodes"), edges = ld("fakeedges"), probs = NULL),
  db          = list(nodes = ld("db_nodes"), edges = ld("db_edges"), probs = ld("db_probs")),
  # R's equate() matches gate names as regex SUBSTRINGS, so on ai_nodes the top
  # gate "T" matches inside basic event "TO" and equate() never terminates (the
  # string grows until memory runs out). The top event's name never appears in
  # the finished equation, so it is renamed here to get R's intended output.
  ai          = list(nodes = mutate(ld("ai_nodes"), event = ifelse(event == "T", "TOPEVENT", event)),
                     edges = ld("ai_edges"), probs = ld("ai_probs")),
  security    = list(nodes = ld("security_nodes"), edges = ld("security_edges"), probs = ld("security_probs")),
  it_security = list(nodes = ld("it_security_nodes"), edges = ld("it_security_edges"), probs = ld("it_security_probs")),
  breach      = list(nodes = ld("breach_nodes"), edges = ld("breach_edges"), probs = NULL))

res <- list(r_version = R.version.string, trees = list())
for (nm in names(trees)) {
  t <- trees[[nm]]
  gates <- curate(t$nodes, t$edges)
  eq <- equate(gates)
  f <- formulate(eq)
  fa <- formalArgs(f)
  tt <- calculate(f)
  rec <- list(
    curate = list(gate = as.character(gates$gate), type = as.character(gates$type),
                  class = as.character(gates$class), n = gates$n, set = gates$set,
                  items = lapply(gates$items, as.character)),
    equation = eq,
    formals = fa,
    body = paste(deparse(body(f)), collapse = " "),
    calculate_columns = names(tt),
    calculate_rows = paste0(apply(as.matrix(tt[fa]), 1, paste, collapse = ""), ":", tt$outcome))
  if (!is.null(t$probs)) {
    p <- if (all(c("event", "probability") %in% names(t$probs))) {
      setNames(t$probs$probability, t$probs$event)
    } else {
      unlist(t$probs[1, ])
    }
    rec$quantify_prob <- num(quantify_prob(f, newdata = p))
  }
  # concentrate() (admisc::simplify) does not finish within minutes on the
  # 10-event it_security tree, so cutsets/tabulate fixtures skip it.
  if (nm != "it_security") {
    cuts <- tidyfault::concentrate(gates)
    tab <- tabulate(cuts, formula = f, query = TRUE)
    rec$concentrate <- cuts
    rec$tabulate <- list(mincut = tab$mincut, query = tab$query, cutsets = tab$cutsets,
                         failures = tab$failures, coverage = num(tab$coverage))
  }
  res$trees[[nm]] <- rec
}

pop <- populate(ld("db_outcomes_binary"), ld("db_probs"))
res$populate_db <- lapply(as.list(pop), function(col) if (is.numeric(col)) num(col) else col)
res$populate_db_columns <- names(pop)

poly <- function(d) list(x = num(d$x), y = num(d$y))
res$gates <- list(
  gate_and_1_12 = poly(gate_and(size = 1, res = 12)),
  gate_or_1_12  = poly(gate_or(size = 1, res = 12)),
  gate_top_2_12 = poly(gate_top(size = 2, res = 12)),
  gate_and_default_50 = poly(gate_and(res = 50)),
  get_gate_and  = poly(get_gate(0.5, -1, gate = "and", size = 1, res = 10)),
  get_gate_or   = poly(get_gate(0, 0, gate = "or", size = 1, res = 10)),
  get_gate_top  = poly(get_gate(2, 3, gate = "top", size = 0.5, res = 10)))
gnodes <- tibble(id = 1:3, event = c("T", "G1", "G2"),
                 type = factor(c("top", "and", "or"), levels = c("top", "and", "or", "not")),
                 x = c(0, -1, 1), y = c(1, 0, 0))
gp <- gate(gnodes, size = 0.5, res = 16)
res$gate_frame <- list(columns = names(gp), group = gp$group, gate = as.character(gp$gate),
                       x = num(gp$x), y = num(gp$y))

writeLines(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = NA), out, useBytes = TRUE)
cat("wrote", out, "\n")
