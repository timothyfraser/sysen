# 10_workshop.py
# Tim Fraser
# Workshop 10: Physical Acceleration Models
# Chapter: Physical Acceleration Models in Python

# Packages
import pandas as pd
import numpy as np
from scipy.stats import weibull_min
from scipy.optimize import minimize
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance
from functions_distributions import dweibull, qweibull

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
    'rating': [60, 70, 80, 90, 100]
})
# Temperature Factor (a standardized unit)
alt = alt.assign(tf=lambda df: 1 / (1 / 11605 * (df['temp'] + 273.15)))

alt









# Line of best fit in plotnine
(ggplot() +
    geom_point(data=alt, mapping=aes(x='temp', y='c')) +
    geom_smooth(data=alt, mapping=aes(x='temp', y='c'),
                method='lm', se=False))


# y = m*x + b
# y-axis = slope m * x-axis + intercept b

# y = beta * x + alpha
# y = alpha + beta * x

# The Python tutorial's lm() is statsmodels OLS with R-style formulas.
m = lm(formula='c ~ temp', data=alt)

# y = 3748.26 + -14.76 * x

def get_y(x):
    return 3748.26 + -14.76 * np.asarray(x)

get_y(1)
get_y([100, 125])

tidy(m)
glance(m)

# rsq = % of variation in y explained by model
# --- grade of your model.
# 0 = god-awful model
# 0.5 = pretty respectable
# 0.95 = very very happy
# 1.0 = perfect


glance(m)[['rsq']]


# What is the acceleration factor for characteristic life
# as temperature increases?
tidy(m).query("term == 'temp'")

m.params
m.params.iloc[1]
m.params['temp']

# Make predictions!
# statsmodels: m.predict(newdata) when the model was fit with a formula
pd.DataFrame({
    'temp': [50, 100, 150],
    'chat': m.predict(pd.DataFrame({'temp': [50, 100, 150]}))
})

dat = pd.DataFrame({'temp': [50, 100, 150]})
dat = dat.assign(chat=m.predict(dat))

dat = pd.DataFrame({'temp': [50, 100, 150]})
m.predict(dat)



pd.DataFrame({
    'temp': [50, 100, 150],
    'chat': m.predict(pd.DataFrame({'temp': [50, 100, 150]}))
})

m.predict(pd.DataFrame({'temp': [0, 200, 300]}))



# Exponential
lm(formula='c ~ temp', data=alt)

alt_log = alt.assign(log_c=lambda df: np.log(df['c']))
m2 = lm(formula='log_c ~ temp', data=alt_log)

m2







m1 = lm(formula='c ~ temp', data=alt)
m1
glance(m1)[['rsq']]
# rsq

m2 = lm(formula='log_c ~ temp', data=alt_log)
m2
np.exp(8.794759)

np.exp(8.794759 + -0.009739 * 30)
glance(m2)


temps = np.arange(0, 201, 10)
pd.DataFrame({
    'temp': temps,
    'chat': np.exp(m2.predict(pd.DataFrame({'temp': temps})))
})


def chat(temp):
    return np.exp(8.794759 + -0.009739 * temp)

chat(temp=32)

# y = e^(a + beta*x)
# ln(y) = a + beta*x

# [y = alpha + beta*x]
# alpha = intercept
# beta = slope of temperature



# ASIDE: PROJECTS ###########################

lm(formula='c ~ temp', data=alt)
lm(formula='c ~ temp + volts', data=alt)
m3 = lm(formula='log_c ~ temp + volts', data=alt_log)

pd.DataFrame({
    'temp': [0, 50, 100],
    'volts': [5, 10, 15],
    'chat': np.exp(m3.predict(pd.DataFrame({
        'temp': [0, 50, 100],
        'volts': [5, 10, 15]
    })))
})


from itertools import product
dat = pd.DataFrame(list(product([0, 50, 100], [5, 10, 15])),
                   columns=['temp', 'volts'])
dat = dat.assign(chat=lambda df: np.exp(m3.predict(df[['temp', 'volts']])))


dat = dat.assign(chat_lab=lambda df: df['chat'].round())
(ggplot() +
    geom_tile(data=dat, mapping=aes(x='temp', y='volts', fill='chat')) +
    geom_text(data=dat, mapping=aes(x='temp', y='volts', label='chat_lab')))




# To be continued on Thursday!! #########################




# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)
    # or weibull_min.pdf(t, m, scale=c)

# Suppose the lifespans under normal usage are just off by a factor of ~2.5
# then we could project the PDF under normal usage like:

airbags = pd.DataFrame({'t': range(1, 12001, 20)})
airbags = airbags.assign(
    d_stress=lambda df: d(df['t'], c=4100, m=1.25),
    d_usage=lambda df: d(t=df['t'] / 2.5, c=4100, m=1.25) / 2.5
)


(ggplot() +
    # Plot the PDF under stress conditions
    geom_line(data=airbags, mapping=aes(x='t', y='d_stress', color='"Stress"'),
              size=1.5) +
    # Plot the PDF under normal usage conditions
    geom_line(data=airbags, mapping=aes(x='t', y='d_usage', color='"Normal Usage"'),
              size=1, linetype='dashed') +
    # Add a nice theme and clear labels
    theme_classic(base_size=14) +
    labs(x='Airbag Lifespan in hours (t)', y='Probability Density d(t)',
         color='Conditions',
         subtitle='We want Lifespan under Normal Usage,\nbut can only get Lifespan under Stress'))


# Let's write a weibull quantile function
def q(p, c, m):
    return weibull_min.ppf(p, m, scale=c)

# Get median under stress
median_s = q(0.5, c=4100, m=1.25)
# Get median under normal conditions
median_u = q(0.5, c=4500, m=1.5)

# Calculate it!
af = median_u / median_s
# Check the Acceleration Factor!
af



alt = pd.DataFrame({
    'c': [1400, 1450, 1500, 1550, 1650],
    'temp': [160, 155, 152, 147, 144],
    'volts': [17, 16.5, 14.5, 14, 13],
    'time': [1200, 1000, 950, 600, 500],
    'rating': [60, 70, 80, 90, 100]
})
alt = alt.assign(tf=lambda df: 1 / (1 / 11605 * (df['temp'] + 273.15)))

alt

alt_plot = alt.assign(log_c=lambda df: np.log(df['c']))
g = (ggplot(alt_plot, aes(x='tf', y='log_c')) +
     geom_point(size=5) +
     geom_smooth(method='lm', se=False) +
     theme_classic(base_size=14) +
     labs(title='Arrhenius Model, Visualized',
          subtitle='Model Equation:  log(c) = 3.1701 + 0.1518 TF    \nModel Fit: 96%',
          x='Temperature Factor (TF)', y='Characteristic Lifespan log(c)'))
g


m1 = lm(formula='log_c ~ tf', data=alt_plot)
glance(m1)[['rsq']]
m1
# Interpreting our model
# If the temperature factor tf = 0, we predict log(c) = 3.1701
# If temperature factor tf +1, we predict log(c) increases by beta = deltaH = 0.1518


def c_hat(tf):
    return np.exp(3.1701 + 0.1518 * tf)

c_hat(tf=2)
# Or better yet, let's calculate temperature factor 'tf' too,
# so we only have to supply a temperature in Celsius
def tf(temp):
    k = 1 / 11605   # Get Boltzmann's constant
    return 1 / (k * (temp + 273.15))  # Get TF!

# Now predict c_hat for 30, 60, and 90 degrees celsius!
def c_hat(temp):
    return np.exp(3.1701 + 0.1518 * tf(temp))

c_hat(np.array([30, 60, 90]))



fakedata = pd.DataFrame({
    'temp': np.arange(0, 201, 10)
})
fakedata = fakedata.assign(tf=lambda df: tf(df['temp']))

m1.predict(fakedata)

np.exp(m1.predict(fakedata))


# Or do it all at once!
pd.DataFrame({
    'temp': np.arange(0, 201, 10),
    'tf': tf(np.arange(0, 201, 10)),
    'c_hat': np.exp(m1.predict(pd.DataFrame({'tf': tf(np.arange(0, 201, 10))})))
})



alt_eyring = alt_plot.copy()
alt_eyring['log_volts'] = np.log(alt_eyring['volts'])
m2 = lm(formula='log_c ~ tf + log_volts', data=alt_eyring)

fakedata = pd.DataFrame({
    'temp': 30,
    'tf': tf(30),
    'volts': np.arange(1, 31, 1)
})
fakedata = fakedata.assign(log_volts=lambda df: np.log(df['volts']))
fakedata = fakedata.assign(c_hat=lambda df: np.exp(m2.predict(df[['tf', 'log_volts']])))

(fakedata
 .pipe(lambda df: ggplot(df, aes(x='volts', y='c_hat')) +
       geom_line() +
       geom_point() +
       theme_classic(base_size=14) +
       labs(title='Eyring Model of Effect of Voltage on Lifespan (30 Deg. Celsius)',
            subtitle='Equation: c = e^(5.0086 + 0.1027 TF - 0.1837 * log(volts))',
            x='Voltage (volts)', y='Predicted Characteristic Life (c-hat)')))


# patsy formulas can't see the name `np`; log the column first (Python tutorial style).
alt_rating = alt.assign(log_rating=lambda df: np.log(df['rating']))
lm(formula='log_rating ~ time', data=alt_rating)

alt_vt = alt.assign(
    log_rating=lambda df: np.log(df['rating']),
    volts_time=lambda df: df['volts'] * df['time']
)
lm(formula='log_rating ~ volts_time', data=alt_vt)



alt_m3 = alt_plot.assign(
    log_volts=lambda df: np.log(df['volts']),
    volts_time=lambda df: df['volts'] * df['time']
)
m3 = lm(formula='log_c ~ tf + log_volts + volts_time', data=alt_m3)
# Really good fit!
glance(m3)





# Let's write the Weibull density and failure function, as always...
def d(t, c, m):
    return (m / t) * (t / c)**m * np.exp(-1 * ((t / c)**m))

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
fb(t=1000, tb=100, a=20, c=2000, m=1.5)



pd.DataFrame({
    'var': ['a', 'b'],
    'value': [123123, 234234]
})

dat = pd.DataFrame({
    't': [5, 15, 25],
    'r1': [32, 27, 30],
    'r2': [34, 17, 22],
    'r3': [50, 34, 15]
})




# The last chunk of the R workshop uses a `wheels` table that was never
# defined in this file (a live-class leftover). Skip it, or bring your own
# crosstab of failures-by-time at three temperatures, then run MLE the way
# the Python tutorial does: minimize the negative joint log-likelihood.
