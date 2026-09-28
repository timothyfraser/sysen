# Workshop 10 slides: recompute the three worked acceleration examples.
# Source: source("functions/slides_workshop_10_acceleration.R")
# Example 1 (linear acceleration), Example 2 (exponential acceleration),
# Example 3 (acceleration factor needed for a 10% failure budget).

# Example 1: lambda_u = lambda_s / AF; F_U(t) = 1 - exp(-lambda_u t)
ex1_linear = function(mttf = 4500, AF = 35, t = 40000){
  lambda_s = 1 / mttf
  lambda_u = lambda_s / AF
  c(lambda_u = lambda_u, mttf_u = 1 / lambda_u, F_U = 1 - exp(-lambda_u * t))
}

# Example 2: F_U(t_U) = F_S(ln(t_U / AF)) = 1 - (t_U / AF)^(-lambda_s)
ex2_exponential = function(mttf = 4500, AF = 35, t = 40000){
  lambda_s = 1 / mttf
  c(F_U = 1 - (t / AF)^(-lambda_s))
}

# Example 3: AF = lambda_s / lambda_u, with lambda_u = -ln(1 - p) / t
ex3_af = function(mttf = 4500, p = 0.10, t = 40000){
  lambda_u = -log(1 - p) / t
  lambda_s = 1 / mttf
  c(lambda_u = lambda_u, lambda_s = lambda_s, AF = lambda_s / lambda_u)
}

if(sys.nframe() == 0){
  print(ex1_linear()); print(ex2_exponential()); print(ex3_af())
}
