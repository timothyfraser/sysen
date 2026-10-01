# 10_workshop.py
# Tim Fraser
# Workshop 10: Physical Acceleration Models

# It mirrors 10_workshop.R section by section.
# Run it from the top of the sysen folder.

# Packages
import numpy as np                     # math (base R in R)
import pandas as pd                    # data wrangling (dplyr + tidyr in R)
import statsmodels.formula.api as smf  # linear models (lm() in R)
from scipy.optimize import minimize    # optimization (optim() in R)
from plotnine import *                 # visualization (ggplot2 in R)
import sys
sys.path.append("functions")
from functions_models import tidy, glance        # broom's tidy() and glance() in R
from functions_distributions import qweibull     # qweibull() in R

# STEP 1: FIND THIS DATA
# STEP 2: LOAD THIS DATA
# STEP 3: MODEL THIS DATA
# STEP 4: PREDICT WITH THIS DATA


alt = pd.DataFrame({
    # Characteristic life in hours
    'c': [1400, 1450, 1500, 1550, 1650],

    # Temperature in Celsius
    'temp': [160, 155, 152, 147, 144],

    # Voltage, in volts
    'volts': [17, 16.5, 14.5, 14, 13],

    # Hours of life spent by time of test
    'time': [1200, 1000, 950, 600, 500],

    # Performance Rating, in Amps
    'rating': [60, 70, 80, 90, 100]})

# Temperature Factor (a standardized unit)
alt['tf'] = 1 / (1 / 11605 * (alt['temp'] + 273.15))

print(alt)










# Line of best fit in ggplot
(ggplot()
 + geom_point(data=alt, mapping=aes(x='temp', y='c'))
 + geom_smooth(data=alt, mapping=aes(x='temp', y='c'),
               method="lm", se=False))


# y = m*x + b
# y-axis = slope m * x-axis + intercept b

# y = beta * x + alpha
# y = alpha + beta * x

m = smf.ols("c ~ temp", data=alt).fit()

# y = 3748.26 + -14.76 * x

def get_y(x):
    return 3748.26 + -14.76 * np.asarray(x)

print(get_y(1))
print(get_y([100, 125]))

print(tidy(m))
print(glance(m))

# r.squared = % of variation in y explained by model
# --- grade of your model.
# 0 = god-awful model
# 0.5 = pretty respectable
# 0.95 = very very happy
# 1.0 = perfect


print(glance(m)[['rsq']])


# What is the acceleration factor for characteristic life
# as temperature increases?
print(tidy(m).query("term == 'temp'"))

print(m.params)
print(m.params.iloc[1])
print(m.params['temp'])

# Make predictions!
# Equivalent options
print(pd.DataFrame({
    'temp': [50, 100, 150],
    'chat': m.predict(pd.DataFrame({'temp': [50, 100, 150]}))}))

print(pd.DataFrame({'temp': [50, 100, 150]})
      .assign(chat=lambda d: m.predict(d)))

dat = pd.DataFrame({'temp': [50, 100, 150]})
print(m.predict(dat))



print(pd.DataFrame({
    'temp': [50, 100, 150],
    'chat': m.predict(pd.DataFrame({'temp': [50, 100, 150]}))}))

print(m.predict(pd.DataFrame({'temp': [0, 200, 300]})))



# Exponential
print(smf.ols("c ~ temp", data=alt).fit().params)

m2 = smf.ols("np.log(c) ~ temp", data=alt).fit()

print(m2.params)









m1 = smf.ols("c ~ temp", data=alt).fit()
print(m1.params)
print(glance(m1)[['rsq']])
# r.squared

m2 = smf.ols("np.log(c) ~ temp", data=alt).fit()
print(m2.params)
print(np.exp(8.794759))

print(np.exp(8.794759 + -0.009739 * 30))
print(glance(m2))


print(pd.DataFrame({'temp': np.arange(0, 200 + 1, 10)})   # seq(0, 200, by = 10) in R
      .assign(chat=lambda d: np.exp(m2.predict(d))))


def chat(temp):
    return np.exp(8.794759 + -0.009739 * temp)

print(chat(temp=32))

# rexp(n = 1000, rate = 0.001) %>% log() %>% hist()

# y = e^(a + beta*x)
# ln(y) = a + beta*x

# [y = alpha + beta*x]
# alpha = intercept
# beta = slope of temperature



# ASIDE: PROJECTS ###########################

print(smf.ols("c ~ temp", data=alt).fit().params)
print(smf.ols("c ~ temp + volts", data=alt).fit().params)
m3 = smf.ols("np.log(c) ~ temp + volts", data=alt).fit()

print(pd.DataFrame({'temp': [0, 50, 100], 'volts': [5, 10, 15]})
      .assign(chat=lambda d: np.exp(m3.predict(d))))


# (tidyr's expand_grid() in R; pandas builds every combination with a cross merge)
dat = (pd.DataFrame({'temp': [0, 50, 100]})
       .merge(pd.DataFrame({'volts': [5, 10, 15]}), how='cross'))
dat['chat'] = np.exp(m3.predict(dat))
dat['label'] = dat['chat'].round()


(ggplot()
 + geom_tile(data=dat, mapping=aes(x='temp', y='volts', fill='chat'))
 + geom_text(data=dat, mapping=aes(x='temp', y='volts', label='label')))




# To be continued on Thursday!! #########################




# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)
    # or dweibull(t, scale = c, shape = m)

# Suppose the lifespans under normal usage are just off by a factor of ~2.5
# then we could project the PDF under normal usage like:

airbags = pd.DataFrame({'t': np.arange(1, 12000 + 1, 20)})   # seq(1, 12000, by = 20) in R
airbags['d_stress'] = d(airbags['t'], c=4100, m=1.25)
airbags['d_usage'] = d(t=airbags['t'] / 2.5, c=4100, m=1.25) / 2.5


(ggplot()
 # Plot the PDF under stress conditions
 + geom_line(data=airbags, mapping=aes(x='t', y='d_stress', color='"Stress"'),
             size=1.5)
 # Plot the PDF under normal usage conditions
 + geom_line(data=airbags, mapping=aes(x='t', y='d_usage', color='"Normal Usage"'),
             size=1, linetype="dashed")
 # Add a nice theme and clear labels
 + theme_classic(base_size=14)
 + labs(x="Airbag Lifespan in hours (t)", y="Probability Density d(t)",
        color="Conditions",
        subtitle="We want Lifespan under Normal Usage,\nbut can only get Lifespan under Stress"))


# Let's write a weibull quantile function
def q(p, c, m):
    return qweibull(p, scale=c, shape=m)

# Get median under stress
median_s = q(0.5, c=4100, m=1.25)
# Get median under normal conditions
median_u = q(0.5, c=4500, m=1.5)

# Calculate it!
af = median_u / median_s
# Check the Acceleration Factor!
print(af)




alt = pd.DataFrame({
    # Characteristic life in hours
    'c': [1400, 1450, 1500, 1550, 1650],
    # Temperature in Celsius
    'temp': [160, 155, 152, 147, 144],
    # Voltage, in volts
    'volts': [17, 16.5, 14.5, 14, 13],
    # Hours of life spent by time of test
    'time': [1200, 1000, 950, 600, 500],
    # Performance Rating, in Amps
    'rating': [60, 70, 80, 90, 100]})
# Temperature Factor (a standardized unit)
alt['tf'] = 1 / (1 / 11605 * (alt['temp'] + 273.15))

print(alt)

g = (ggplot(alt, aes(x='tf', y='np.log(c)'))
     + geom_point(size=5)  # Add scatterplot points
     + geom_smooth(method="lm", se=False)
     # Make line of best fit, using lm() - a linear model
     # we can write 'se = False' (standard error = False) to get rid of the confidence interval
     # Add theme
     + theme_classic(base_size=14)
     # Add labels
     + labs(title="Arrhenius Model, Visualized",
            subtitle="Model Equation:  log(c) = 3.1701 + 0.1518 TF    \nModel Fit: 96%",
            # We can add a line-break in the subtitle by writing \n
            x="Temperature Factor (TF)", y="Characteristic Lifespan log(c)"))
g


m1 = smf.ols("np.log(c) ~ tf", data=alt).fit()
print(glance(m1)[['rsq']])
print(m1.params)
# Interpreting our model
# If the temperature factor tf = 0, we predict log(c) = 3.1701
# If temperature factor tf +1, we predict log(c) increases by beta = deltaH = 0.1518


def c_hat(tf):
    return np.exp(3.1701 + 0.1518 * tf)

print(c_hat(tf=2))
# Or better yet, let's calculate temperature factor 'tf' too,
# so we only have to supply a temperature in Celsius
def tf(temp):
    k = 1 / 11605   # Get Boltzmann's constant
    return 1 / (k * (np.asarray(temp) + 273.15))  # Get TF!

# Now predict c_hat for 30, 60, and 90 degrees celsius!
def c_hat(temp):
    return np.exp(3.1701 + 0.1518 * tf(temp))

print(c_hat([30, 60, 90]))



fakedata = pd.DataFrame({'temp': np.arange(0, 200 + 1, 10)})
fakedata['tf'] = tf(fakedata['temp'])

print(m1.predict(fakedata))

print(np.exp(m1.predict(fakedata)))


# Or do it all at once!
fakedata = pd.DataFrame({'temp': np.arange(0, 200 + 1, 10)})
fakedata['tf'] = tf(fakedata['temp'])
fakedata['c_hat'] = np.exp(m1.predict(fakedata))
print(fakedata)



m2 = smf.ols("np.log(c) ~ tf + np.log(volts)", data=alt).fit()

fakedata = pd.DataFrame({
    # But vary volts
    'volts': np.arange(1, 30 + 1, 1)})
# Hold temperature constant
fakedata['temp'] = 30
fakedata['tf'] = tf(fakedata['temp'])
# Predict c_hat
fakedata['c_hat'] = np.exp(m2.predict(fakedata))

(ggplot(fakedata, aes(x='volts', y='c_hat'))
 + geom_line()
 + geom_point()
 + theme_classic(base_size=14)
 + labs(title="Eyring Model of Effect of Voltage on Lifespan (30 Deg. Celsius)",
        subtitle="Equation: c = e^(5.0086 + 0.1027 TF - 0.1837 * log(volts))",
        x="Voltage (volts)", y="Predicted Characteristic Life (c-hat)"))


print(smf.ols("np.log(rating) ~ time", data=alt).fit().params)


print(smf.ols("np.log(rating) ~ I(volts * time)", data=alt).fit().params)



m3 = smf.ols("np.log(c) ~ tf + np.log(volts) + I(volts * time)", data=alt).fit()
# Really good fit!
print(glance(m3))





# Let's write the Weibull density and failure function, as always...
def d(t, c, m):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

def f(t, c, m):
    return 1 - np.exp(-1 * ((t / c)**m))

def fb(t, tb, a, c, m):
    # Change in probability of failure
    delta_failure = f(t=t + a * tb, c=c, m=m) - f(t=a * tb, c=c, m=m)
    # Reliability after burn-in period
    reliability = 1 - f(t=a * tb, c=c, m=m)
    # conditional probability of failure
    return delta_failure / reliability

# 1000 hours after burn-in
# with a burn-in period of 100 hours
# an acceleration factor of 20
# characteristic life c = 2000 hours
# and
# shape parameter m = 1.5
print(fb(t=1000, tb=100, a=20, c=2000, m=1.5))



# (dplyr's tribble() in R; in pandas, list the rows)
print(pd.DataFrame([
    ["a", 123123],
    ["b", 234234]], columns=["var", "value"]))

dat = pd.DataFrame([
    [5, 32, 34, 50],
    [15, 27, 17, 34],
    [25, 30, 22, 15]], columns=["t", "r1", "r2", "r3"])




# Let's write our crosstable's likelihood function
def ll(par, t, x1, x2, x3):
    t = np.asarray(t, dtype=float)
    # Get total failures
    r1 = np.sum(x1)
    r2 = np.sum(x2)
    r3 = np.sum(x3)
    # Record total sample size in each
    n1 = 200
    n2 = 175
    n3 = 300
    tmax = np.max(t)  # Record last time step

    # Get the product of the log-densities at each time step, for all failures then
    prob_d1 = np.sum(np.log(d(t, c=par[0], m=par[3])) * x1)
    prob_d2 = np.sum(np.log(d(t, c=par[1], m=par[3])) * x2)
    prob_d3 = np.sum(np.log(d(t, c=par[2], m=par[3])) * x3)

    # For the last time step, get the probability of each remaining unit surviving
    prob_r1 = np.log(r(t=tmax, c=par[0], m=par[3])**(n1 - r1))
    prob_r2 = np.log(r(t=tmax, c=par[1], m=par[3])**(n2 - r2))
    prob_r3 = np.log(r(t=tmax, c=par[2], m=par[3])**(n3 - r3))

    # Get joint log-likelihood, across ALL vectors
    return prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3

# NOTE: the R version references a `wheels` data frame that is never defined,
# so this block errors in R too. (It also calls a reliability function `r()`
# that this workshop never writes.) We keep the code so you can see the
# pattern, but only run it if you have loaded a `wheels` data frame
# (columns t, temp_100, temp_150, temp_200) and written `r()` yourself.
# See 10_lesson.py for a complete, runnable version of this MLE.
if "wheels" in globals():

    # And let's run MLE!
    # R's optim(..., control = list(fnscale = -1)) MAXIMIZES the log-likelihood.
    # scipy's minimize() minimizes, so we hand it the NEGATIVE log-likelihood.
    mle = minimize(
        lambda par: -ll(par, t=wheels['t'],
                        x1=wheels['temp_100'],
                        x2=wheels['temp_150'],
                        x3=wheels['temp_200']),
        x0=[1000, 1000, 1000, 1],
        method="Nelder-Mead")
    # Check out our 3 characteristic life parameters,
    # for temp_100, temp_150, and temp_200, and our shared shape parameter!
    print(mle.x)



# Remember our function to calculate temperature factors
def tf(temp):
    return 1 / ((1 / 11605) * (np.asarray(temp) + 273.15))

# (This part needs `mle` from the block above, so it is guarded too.)
if "wheels" in globals():

    # Let's collect our parameter estimates
    param = pd.DataFrame({
        # For each temperature
        'temp': [100, 150, 200],
        # report the MLE c estimates
        'c': mle.x[0:3],
        # and the shared MLE m estimate
        'm': mle.x[3]})
    # and Calculate TF (for each temperature...)
    # This will be our independent variable
    param['tf'] = tf(param['temp'])

    # Check it!
    print(param)
