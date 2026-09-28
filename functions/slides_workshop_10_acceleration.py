# Workshop 10 slides: recompute the three worked acceleration examples (Python twin).
# Source: exec(open('functions/slides_workshop_10_acceleration.py').read())
import numpy as np

def ex1_linear(mttf=4500, AF=35, t=40000):
    lambda_s = 1 / mttf
    lambda_u = lambda_s / AF
    return {"lambda_u": lambda_u, "mttf_u": 1 / lambda_u, "F_U": 1 - np.exp(-lambda_u * t)}

def ex2_exponential(mttf=4500, AF=35, t=40000):
    lambda_s = 1 / mttf
    return {"F_U": 1 - (t / AF) ** (-lambda_s)}

def ex3_af(mttf=4500, p=0.10, t=40000):
    lambda_u = -np.log(1 - p) / t
    lambda_s = 1 / mttf
    return {"lambda_u": lambda_u, "lambda_s": lambda_s, "AF": lambda_s / lambda_u}

if __name__ == "__main__":
    print(ex1_linear(), ex2_exponential(), ex3_af())
