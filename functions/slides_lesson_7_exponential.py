# Python twin of functions/slides_lesson_7_exponential.R (Lesson 7, Useful Life
#   Distributions - Exponential; slides 6-7, 10, 12-13, 16, 22, 27, 30 plus the
#   numbers behind Exercises 1-3 and Examples 1-3).
# Run from the sigma repo root:  python3 functions/slides_lesson_7_exponential.py
# Reads  workshops/bulb_lifetimes.csv. Writes gen_*_py.png parity copies to
#   docs-v3/images/slides/lesson-7/ and prints the same numbers as the R script.
#   Nothing is random. Notation: f, F, R, z(t) failure rate, H, lambda, MTTF = 1/lambda.
import numpy as np
import pandas as pd
from scipy import integrate, stats
from plotnine import *

out = "docs-v3/images/slides/lesson-7"
red = "#B31B1B"; grey = "#595959"

def r_exp(t, lam): return np.exp(-lam * t)
def f_exp(t, lam): return lam * np.exp(-lam * t)

def theme_deck():
    return theme_classic(base_size = 20) + theme(figure_size = (11, 6))

def save(g, name):
    g.save(f"{out}/{name}", dpi = 100, verbose = False)
    print("wrote", f"{out}/{name}")

# 1. Bathtub (slides 6-7)
t = np.linspace(0.02, 10, 600)
bath = pd.DataFrame({"t": t, "z": 1.2 * np.exp(-t / 0.5) + 0.25 + 0.25 * (t / 8) ** 6})
labs_b = pd.DataFrame({"t": [0.8, 4.45, 8.65], "z": 0.1,
                       "lab": ["Burn-in\nperiod", "Useful life\nperiod", "Wear-out\nperiod"]})
g = (ggplot(bath, aes("t", "z")) +
     geom_vline(xintercept = [1.6, 7.3], linetype = "dashed", color = grey) +
     geom_line(color = red, size = 1.8) +
     geom_text(labs_b, aes(label = "lab"), size = 18, va = "bottom") +
     scale_x_continuous(expand = (0, 0), breaks = []) +
     scale_y_continuous(expand = (0, 0), limits = (0, 1.5), breaks = []) +
     labs(x = "Time t", y = "z(t)") + theme_deck())
save(g, "gen_bathtub_py.png")

# 2. Mode, median, MTTF: lognormal, median 10, MTTF 15
ml = np.log(10); sl = np.sqrt(2 * np.log(1.5))
ln_d = stats.lognorm(s = sl, scale = np.exp(ml))
mode_t, med_t, mttf_t = np.exp(ml - sl ** 2), np.exp(ml), np.exp(ml + sl ** 2 / 2)
print(f"Slide 10 lognormal: mode = {mode_t:.2f}, median = {med_t:.2f}, MTTF = {mttf_t:.2f}, f(mode) = {ln_d.pdf(mode_t):.4f}")
tt = np.linspace(0.01, 25, 600)
ln = pd.DataFrame({"t": tt, "f": ln_d.pdf(tt)})
marks = pd.DataFrame({"t": [mode_t, med_t, mttf_t], "lab": ["Mode", "Median", "MTTF"]})
marks["f"] = ln_d.pdf(marks["t"]); marks["ft"] = marks["f"] + 0.006
g = (ggplot(ln, aes("t", "f")) +
     geom_segment(marks, aes(x = "t", xend = "t", y = 0, yend = "f"), linetype = "dashed", color = grey) +
     geom_line(color = red, size = 1.8) +
     geom_text(marks, aes(y = "ft", label = "lab"), size = 18, va = "bottom") +
     scale_x_continuous(expand = (0, 0), breaks = list(range(0, 26, 5))) +
     scale_y_continuous(expand = (0, 0), limits = (0, 0.085)) +
     labs(x = "Time t", y = "f(t)") + theme_deck())
save(g, "gen_mode_median_mttf_py.png")

# 3. R, z, f for Exercise 1
t = np.linspace(0, 10, 400)
ex1 = pd.concat([pd.DataFrame({"t": t, "fn": "R(t)", "y": 1 / (0.2 * t + 1) ** 2}),
                 pd.DataFrame({"t": t, "fn": "f(t)", "y": 0.4 / (0.2 * t + 1) ** 3}),
                 pd.DataFrame({"t": t, "fn": "z(t)", "y": 0.4 / (0.2 * t + 1)})])
lab3 = pd.DataFrame({"fn": ["R(t)", "z(t)", "f(t)"], "t": 1.6, "y": [0.72, 0.38, 0.1]})
g = (ggplot(ex1, aes("t", "y", linetype = "fn")) +
     geom_line(color = red, size = 1.6) +
     geom_text(lab3, aes(label = "fn"), size = 20, ha = "left", fontstyle = "italic") +
     scale_linetype_manual(values = {"R(t)": "solid", "f(t)": "solid", "z(t)": "dashed"}, guide = None) +
     scale_x_continuous(expand = (0, 0), breaks = list(range(0, 11, 2))) +
     scale_y_continuous(expand = (0, 0), limits = (0, 1.02), breaks = np.arange(0, 1.01, 0.2)) +
     labs(x = "Time t (months)", y = "") + theme_deck())
save(g, "gen_r_z_f_py.png")
ex1_mttf = integrate.quad(lambda t: 1 / (0.2 * t + 1) ** 2, 0, np.inf)[0]
print(f"Exercise 1: MTTF = {ex1_mttf:.4f} months (scan: 5 months)")

# 4. MTTF shaded pdf (slide 12)
t = np.linspace(0, 25, 400)
pdf1 = pd.DataFrame({"t": t, "f": 0.4 / (0.2 * t + 1) ** 3})
g = (ggplot(pdf1, aes("t", "f")) + geom_area(fill = red, alpha = 0.35) + geom_line(color = red, size = 1.4) +
     geom_vline(xintercept = ex1_mttf, color = red, size = 1) +
     annotate("text", x = ex1_mttf + 0.5, y = 0.3, label = "MTTF = 5", color = red, size = 20,
              fontweight = "bold", ha = "left") +
     scale_x_continuous(expand = (0, 0)) + scale_y_continuous(expand = (0, 0), limits = (0, 0.42)) +
     labs(x = "Months", y = "f(t)") + theme_deck())
save(g, "gen_mttf_shaded_py.png")

# 5. t and t + x (slide 13)
t0, x0 = 8, 5
g = (ggplot(ln, aes("t", "f")) + geom_area(fill = red, alpha = 0.18) +
     geom_area(ln[ln.t >= t0 + x0], fill = red, alpha = 0.45) + geom_line(color = red, size = 1.4) +
     geom_vline(xintercept = [t0, t0 + x0], color = red, size = 1) +
     annotate("text", x = [t0 + 0.3, t0 + x0 + 0.3], y = 0.078, label = ["t", "t + x"], color = red,
              size = 22, fontweight = "bold", ha = "left") +
     scale_x_continuous(expand = (0, 0), breaks = []) +
     scale_y_continuous(expand = (0, 0), limits = (0, 0.085), breaks = []) +
     labs(x = "Months", y = "f(t)") + theme_deck())
save(g, "gen_t_plus_x_py.png")

# Exercise 2
def r_ex2(t): return (t + 1) * np.exp(-t)
ex2_mttf = integrate.quad(r_ex2, 0, np.inf)[0]
def mrl(t): return integrate.quad(lambda x: r_ex2(t + x) / r_ex2(t), 0, np.inf)[0]
H2 = integrate.quad(lambda u: u / (u + 1), 0, 2)[0]
print(f"Exercise 2: H(2) = {H2:.4f} vs -ln R(2) = {-np.log(r_ex2(2)):.4f}; MTTF = {ex2_mttf:.4f} (scan says 5 months)")
print("Exercise 2: MRL(t) numeric vs 1 + 1/(t+1): " +
      ", ".join(f"t={a} {mrl(a):.4f}/{1 + 1 / (a + 1):.4f}" for a in (0, 1, 4)))

# 6. Constant failure rate (slides 16-17)
g = (ggplot(pd.DataFrame({"t": [0, 10], "z": [1, 1]}), aes("t", "z")) + geom_line(color = red, size = 2) +
     scale_x_continuous(expand = (0, 0), breaks = []) +
     scale_y_continuous(expand = (0, 0), limits = (0, 1.6), breaks = [1], labels = ["λ"]) +
     labs(x = "t = time", y = "z(t)") + theme_deck())
save(g, "gen_constant_hazard_py.png")

# Exercise 3
lam3 = 0.08e-5
p1 = 1 - np.exp(-lam3 * 20000); t1pct = -np.log(1 - 0.01) / lam3
print(f"Exercise 3: F(20000) = {p1:.5f} (scan 0.016); two fail = {p1**2:.6f} (scan 0.016^2 = {0.016**2:.6f}); t_1% = {t1pct:.0f} h (scan 12563)")
print(f"Slide 19: F(MTTF) = 1 - 1/e = {1 - np.exp(-1):.4f}; slide 20: ln 2 = {np.log(2):.4f}")

# 7. Light bulbs (slide 22)
bulbs = pd.read_csv("workshops/bulb_lifetimes.csv")
breaks = list(range(0, 551, 55)) + [np.inf]
lam_hat = 1 / bulbs.days.mean()
cells = pd.cut(bulbs.days, bins = breaks, right = True, include_lowest = True)
freq = cells.value_counts(sort = False).rename_axis("cell").reset_index(name = "n")
freq["lower"] = breaks[:-1]; freq["upper"] = breaks[1:]
freq["expected"] = (100 * (r_exp(freq.lower, lam_hat) - r_exp(freq.upper, lam_hat))).round(1)
freq["scan"] = [40, 23, 8, 10, 4, 3, 4, 4, 0, 3, 1]; freq["match"] = freq.n == freq.scan
print(f"Bulbs: n = {len(bulbs)}, mean = {bulbs.days.mean():.2f}, lambda-hat = 1/mean = {lam_hat:.6f} per day, total = {freq.n.sum()}")
print(freq.to_string())
hist_d = freq.copy(); hist_d.loc[hist_d.upper == np.inf, "upper"] = 605
curve = pd.DataFrame({"t": np.linspace(0, 600, 400)}); curve["pct"] = 100 * 55 * f_exp(curve.t, lam_hat)
g = (ggplot() +
     geom_rect(hist_d, aes(xmin = "lower", xmax = "upper", ymin = 0, ymax = "n"), fill = red, alpha = 0.35, color = red, size = 0.6) +
     geom_line(curve, aes("t", "pct"), color = "black", size = 1.3) +
     scale_x_continuous(expand = (0, 0), breaks = list(range(0, 601, 100))) +
     scale_y_continuous(expand = (0, 0), limits = (0, 45), breaks = list(range(0, 41, 10))) +
     labs(x = "Days to failure (last bar: > 550)", y = "Frequency (%)") + theme_deck())
save(g, "gen_bulb_histogram_pdf_py.png")
t = np.linspace(0, 5, 300)
g = (ggplot(pd.DataFrame({"t": t, "f": f_exp(t, 1)}), aes("t", "f")) + geom_line(color = red, size = 1.8) +
     scale_x_continuous(expand = (0, 0), breaks = []) +
     scale_y_continuous(expand = (0, 0), limits = (0, 1.1), breaks = [1], labels = ["λ"]) +
     labs(x = "t", y = "f(t)") + theme_deck())
save(g, "gen_exponential_pdf_py.png")

# 8. Piecewise exponential (slide 27)
def zp(t): return 0.35 + 1.4 * np.exp(-t / 1.3)
steps = pd.DataFrame({"lo": range(5), "hi": range(1, 6)})
steps["afr"] = [integrate.quad(zp, a, b)[0] / (b - a) for a, b in zip(steps.lo, steps.hi)]
t = np.linspace(0, 5.4, 300)
g = (ggplot() +
     geom_rect(steps, aes(xmin = "lo", xmax = "hi", ymin = 0, ymax = "afr"), fill = red, alpha = 0.15, color = red, size = 0.9) +
     geom_line(pd.DataFrame({"t": t, "z": zp(t)}), aes("t", "z"), color = "black", size = 1.4) +
     scale_x_continuous(expand = (0, 0), breaks = list(range(6)), labels = ["0", "t₁", "t₂", "t₃", "t₄", "t₅"]) +
     scale_y_continuous(expand = (0, 0), limits = (0, 1.8), breaks = []) +
     labs(x = "Time", y = "z(t)") + theme_deck())
save(g, "gen_piecewise_py.png")

# Examples 1-2 (slides 28-29)
lam_p = 4.28e-4
print(f"Example 1: R(730) = {r_exp(730, lam_p):.4f} (scan 0.732); MTTF = {1/lam_p:.1f} h = {1/lam_p/730:.2f} months of 730 h (scan 2336 h = 3.2); "
      f"Pr(fail in next 730 | survived) = {1 - r_exp(730, lam_p):.4f} (scan 0.268)")
l1, l2 = 0.002, 0.003
num = integrate.quad(lambda t: r_exp(t, l2) * f_exp(t, l1), 0, np.inf)[0]
print(f"Example 2 (lambda1 = {l1}, lambda2 = {l2}): integral = {num:.4f}, closed form = {l1/(l1+l2):.4f}")

# 9. Mixture hazard (slide 30)
p, lam1, lam2 = 0.4, 1, 3
def zmix(t):
    return (p * lam1 * np.exp(-lam1 * t) + (1 - p) * lam2 * np.exp(-lam2 * t)) / (p * np.exp(-lam1 * t) + (1 - p) * np.exp(-lam2 * t))
print(f"Example 3: z(0) = {zmix(0):.3f}, z(1) = {zmix(1):.3f}, z(2) = {zmix(2):.3f}, z(5) = {zmix(5):.3f}; MTTF = {p/lam1 + (1-p)/lam2:.4f}")
t = np.linspace(0, 5, 400)
g = (ggplot(pd.DataFrame({"t": t, "z": zmix(t)}), aes("t", "z")) + geom_line(color = red, size = 1.8) +
     scale_x_continuous(expand = (0, 0), breaks = list(range(6))) +
     scale_y_continuous(expand = (0, 0), limits = (0, 2.4), breaks = np.arange(0, 2.01, 0.5)) +
     labs(x = "Time t", y = "z(t)") + theme_deck())
save(g, "gen_mixture_hazard_py.png")
