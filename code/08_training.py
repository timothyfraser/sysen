# 08_training.py
# Training: Statistical Process Control
# Pairs with R training:
# https://timothyfraser.com/sigma/statistical-process-control-in-r.html
# Tim Fraser

# Getting Started ############################

# In this workshop, we will learn how to perform  
# statistical process control in R, using statistical tools  
# and ggplot visualizations! Statistical Process Control refers  
# to using statistics to (1) measure variation in product  
# quality over time and (2) identify benchmarks to know  
# when intervention is needed. Let’s get started!

## Install Packages ############################
# Install main python packages for this script
# !pip install pandas
# !pip install sympy
# !pip install math
# !pip install plotnine
# !pip install os
# !pip install sys
# !pip install patchworklib

## Load Packages ############################
import pandas as pd # Import pandas functions
from plotnine import * # import all plotnine visualization functions
import patchworklib as pw # for combining plots
import os
import sys
# Append files in this folder (functions) to the Python Path
sys.path.append(os.path.abspath('functions'))
# Now you can reference them directly
from functions_distributions import *
# Import math functions
import math




## Our Case #############################################

# For today’s workshop, we’re going to think about why  
# quality control matters in a local economy, by examining  
# the case of the Japanese Hot Springs bath economy! 
# Hot springs, or onsen, are a major source of tourism and recreation  
# for families in Japan, bringing residents from across  
# the country every year to often rural communities where  
# the right geological conditions have brought on naturally  
# occurring hot springs. Restaurants, taxi and bus companies,  
# and many service sector firms rely on their local onsen  
# to bring in a steady stream (pun intended) of tourists  
# to the local economy. So, it’s often in the best interest  
# of onsen operators to keep an eye on the temperature,  
# minerals, or other aspects of their hot springs baths to  
# ensure quality control, to keep up their firm (and town’s!)  
# reputation for quality rest and relaxation!

# Onsen-goers often seek out specific types of hot springs,  
# so it’s important for an onsen to actually provide what  
# it advertises! Serbulea and Payyappallimana (2012) describe  
# some of these benchmarks.
# 
# - Temperature: Onsen are divided into “Extra Hot  
#    Springs” (>42 °C), “Hot Springs” (41~34°C), and “Warm
#    Springs” (33~25°C).
# 
# pH: Onsen are classified into “Acidic” (pH < 3), “Mildly  
#    Acidic” (pH 3~6), “Neutral” (pH 6~7.5), “Mildly alkaline”
#    (ph 7.5~8.5), and “Alkaline” (pH > 8.5).
# 
# Sulfur: Sulfur onsen typically have about 2mg of sulfur  
#    per 1kg of hot spring water; sulfur levels must exceed
#    1 mg to count as a Sulfur onsen. (It smells like rotten
#    eggs!)
# 
# These are decent examples of quality control metrics  
# that onsen operators might want to keep tabs on!

## Our Data #############################################33

# You’ve been hired to evaluate quality control at a  
# local onsen in sunny Kagoshima prefecture! Every month,  
# for 15 months, you systematically took 20 random samples  
# of hot spring water and recorded its temperature, pH,  
# and sulfur levels. How might you determine if this onsen  
# is at risk of slipping out of one sector of the market  
# (eg. Extra Hot!) and into another (just normal Hot  
# Springs?).

# Let's import our samples of bathwater over time!
water = pd.read_csv('workshops/onsen.csv')
water.head()
water.info()


# Our dataset contains:
# 
# id: unique identifer for each sample of onsen water.
# 
# time: categorical variable describing date of sample
#     (month 1, month 3, … month 15).
# 
# temp: temperature in celsius.
# 
# ph: pH (0 to 14)
# 
# sulfur: milligrams of sulfur ions.


# 1. Visualizing Quality Control ###########################

# Let’s learn some key techniques for visualizing quality control!

## 1.1 theme_set() ####################################

# First, when you’re about to make a bunch of ggplot visuals,
# it can help to set a common theme across them all with theme_set().

from plotnine import theme_classic, theme, element_text, element_blank, element_rect, theme_set

# Set a global theme
theme_set(
    theme_classic(base_size=14) + 
    theme(
        # Position the legend at the bottom
        legend_position='bottom',
        # Center-align plot title, subtitle, and caption
        plot_title=element_text(ha='center'),  # ha is short for 'horizontal alignment'
        plot_subtitle=element_text(ha='center'),
        plot_caption=element_text(ha='center'),
        # Remove axis ticks and lines
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        # Add a grey border around the plot
        panel_border=element_rect(fill=None, color='grey')
    )
)

# 1.2. Process Descriptive Statistics ########################

# First, let’s describe our process, using favorite description  
# statistics. We’re going to want to do this a bunch,  
# so why don’t we just write a function for it? Let’s  
# write describe(), which will take a vector x and  
# calculate the mean(), sd(), skewness(), and kurtosis(),  
# and then combine a nice caption describing them.
# 
# (I encourage you to write your own functions like  
# this to help expedite your coding! Start simple!)



# Let's write a describe() function to help us
def describe(x):
  # Testing values
  # x = water.temp  
  
  x = pd.Series(x)

  df = pd.DataFrame({
    'stat_mu': pd.Series( x.mean() ),
    'stat_sd': pd.Series( x.std() ),
    'stat_skew': pd.Series( x.skew() ),
    'stat_kurtosis': pd.Series( x.kurtosis() )
  })
  
  a = 'Process Mean: ' + str(df.stat_mu.round(2)[0]) 
  b = 'SD: ' + str(df.stat_sd.round(2)[0]) 
  c = 'Skewness: ' + str(df.stat_skew.round(2)[0])
  d = 'Kurtosis: ' + str(df.stat_kurtosis.round(2)[0])
  caption = a + ' | ' + b + ' | ' + c + ' | ' + d 
  
  df['caption'] = caption

  return df

# Get caption
tab = describe(water.temp)

# view
tab


# 1.3 Process Overview Visual ######################3

# Your first step should always be to look at the  
# data overall! geom_jitter() and geom_boxplot()
# can help you do this.

# geom_jitter() is a jittered scatterplot, jittering points  
# a little to help with visibility. Since we want to  
# be really precise on our quality control metrics, we  
# could jitter the width a little (width = 0.25), but  
# hold the y-axis (quality metric) constant at height  
# = 0. These are in your x and y axis units, so decide  
# based on your data each time.
# 
# geom_boxplot() makes a boxplot for each group (time)  
# in our data, showing the interquartile range (25th,  
# 50th, and 75th percentiles) of our y variable for each  
# group. Helpful way to view distributions. (Alternatively,  
# you can try geom_violin(), which works the same way.)
# 
# geom_hline() makes a horizontal line at the yintercept;  
# we can tell it to show the mean() of y (in this case,  
# temp).
# 
# geom_histogram() is a histogram! We can use coord_flip()  
# to turn it vertical to match the y-axis.

# The pw.load_ggplot() and | operator from the patchworklib package 
# binds two plots  together into one, giving each a specific proportional  
# width (eg. c(0.25, 0.75) percent, or c(5, 1) would  
# be 5/6 and 1/6.)


# Get grand mean lines
stat = pd.DataFrame({'mu':  pd.Series(water.temp.mean()) })

# view
stat

# Make the initial boxplot...
g1 = (ggplot() +
  # Plot raw points
  geom_jitter(data = water, mapping = aes(x = 'time', y = 'temp'), height = 0, width = 0.25) +
  geom_boxplot(data = water, mapping = aes(x = 'time', y = 'temp', group = 'time')) +
  # Plot grand mean
  geom_hline(data = stat, mapping = aes(yintercept = 'mu' ), color = 'lightgrey', size = 3) +
  # Add our descriptive stats in the caption!
  labs(x = "Time (Subgroup)", y = "Temperature (Celsius)",
       subtitle = "Process Overview",
       caption = tab.caption[0])
  )

# Part 1 of plot 
g1

# Make the histogram, but tilt it on its side
g2 = (ggplot() +
  geom_histogram(
    data = water, mapping = aes(x = 'temp'),
    bins = 15, color = "white", fill = "grey") +
  theme_void() +   # Clear the theme
  coord_flip()  # tilt on its side
  )
# Part 2 of plot
g2

# Then bind them together into 1 plot, 'h'orizontally aligned.

# Let's combine the plots with patchwork
p1 = pw.load_ggplot(g1, figsize =(5,4))
p2 = pw.load_ggplot(g2, figsize = (1,4))

# Bundle them together.
pp = (p1 | p2)

pp.savefig("code/08_process_overview.png", dpi = 200)
# Then navigate to the file to open it.


# We can tell from this visual several things!
# 
# Side Histogram: Our overall distribution is pretty centered.
# 
# Descriptive Statistics: Our distribution has little skew (~0) 
# and has slightly higher-than-average kurtosis (<3) (very centered).
# 
# Line vs. Boxplots: Over time, our samples sure do seem 
# to be getting slightly further from the mean!


# LEARNING CHECK 1 ##################################

## QUESTION #############################

# We analyzed temperature variation above, but our hot  
# springs owner wants to know about variation in pH  
# too! Write a function to produce a process overview  
# plot given any 2 vectors (water.time and water.pH,  
# in this case), and visualize the process overview  
# for pH! (You can do it!)


## ANSWER #############################

def ggprocess(x, y, xlab='Subgroup', ylab='Metric'):
  # import pandas as pd
  # import patchworklib as pw
  # from plotnine import *
  
  # Testing values
  # x = water.time; y = water.temp; xlab='Subgroup'; ylab='Metric'; path = "code/08_process_overview_example.png"
  
  # Convert vectors to series, and bundle as data.frame
  data = pd.DataFrame({
    'x': pd.Series(x),
    'y': pd.Series(y) })
  
  
  # Get grand mean lines
  stat = pd.DataFrame({'mu':  pd.Series(data.y.mean()) })
  
  # describe data
  tab = describe(data.y)
  
  # Make the initial boxplot...
  g1 = (ggplot() +
    # Plot raw points
    geom_jitter(data = data, mapping = aes(x = 'x', y = 'y'), height = 0, width = 0.25) +
    geom_boxplot(data = data, mapping = aes(x = 'x', y = 'y', group = 'x')) +
    # Plot grand mean
    geom_hline(data = stat, mapping = aes(yintercept = 'mu' ), color = 'lightgrey', size = 3) +
    # Add our descriptive stats in the caption!
    labs(x = xlab, y = ylab,
         subtitle = "Process Overview",
         caption = tab.caption[0])
  )
  
  # Make the histogram, but tilt it on its side
  g2 = (ggplot() +
    geom_histogram(
      data = data, mapping = aes(x = 'y'),
      bins = 15, color = "white", fill = "grey") +
    theme_void() +   # Clear the theme
    coord_flip()  # tilt on its side
  )
  
  # Then bind them together into 1 plot, horizontally aligned.
  
  # Let's combine the plots with patchwork
  p1 = pw.load_ggplot(g1, figsize =(5,4))
  p2 = pw.load_ggplot(g2, figsize = (1,4))
  
  # Bundle them together.
  pp = (p1 | p2)
  

  return pp

# Try it!
pp = ggprocess(x = water.time, y = water.ph)

pp.savefig("code/08_process_overview_function.png", dpi = 200)

# In comparison to temp, pH is a much more controlled process.
# 
# I encourage you to use this ggprocess() function you just created!
# 


# 2. Average and Standard Deviation Graphs ###############################

## 2.1 Key Statistics   #####################################

# Next, to analyze these processes more in depth, we  
# need to assemble statistics at 2 levels:
# 
# within-group statistics measure quantities of interest  
# within each subgroup (eg. each monthly slice time in  
# our onsen data).
# 
# between-group statistics measure total quantities of  
# interest for the overall process (eg. the overall  
# “grand” mean, overall standard deviation in our onsen  
# data).


## 2.2 Subgroup (Within-Group) Statistics ######################

# Let’s apply these to our onsen data to get statistics
# describing each subgroup’s distribution, 
# a.k.a. short-term or within-group statistics.


# Calculate short-term statistics within each group
  # For each timestpe
# Calculate these statistics of interest!
stat_s = water.groupby('time').apply(lambda g: pd.Series({
  # Return each time
  'time': g['time'].values[0],
  # within group mean
  'xbar': g['temp'].mean(),
  # within-group range
  'r': g['temp'].max() - g['temp'].min(),
  # within group standard deviation
  'sd': g['temp'].std(),
  # within group sample size n
  'nw': g['temp'].count(),
  # within group degrees of freedom 
  'df': g['temp'].count() - 1
}))
stat_s

# Last, we'll calculate sigma_short (within-group variance)
# We're going to calculate the short-term variation parameter sigma_s (sigma_short)
# by taking the square root of the average of the standard deviation
# Essentially, we're weakening the impact of any special cause variation
# so that our sigma is mostly representative of common cause (within-group) variation
stat_s = stat_s.assign(sigma_s = lambda g: (sum(g.sd**2)/len(g.sd**2))**0.5)

# And get standard error (in a way that retains each subgroup's sample size!)
stat_s = stat_s.assign(se = lambda g: g.sigma_s / g.nw**0.5)

# Calculate 6-sigma control limits!
stat_s = stat_s.assign(upper = lambda g: g.xbar.mean() + 3*g.se)
stat_s = stat_s.assign(lower = lambda g: g.xbar.mean() - 3*g.se)

stat_s # view result!




## 2.3 Total Statistics (Between Groups) ###################3

# To get between-group estimates....
stat_t = pd.DataFrame({
  'xbbar': [ stat_s.xbar.mean() ],
  'rbar' : [ stat_s.r.mean() ],
  'sdbar' : [ stat_s.sd.mean() ],
  # We can also recalculate sigma_short here too
  'sigma_s': (sum(stat_s.sd**2) / len(stat_s.sd**2))**0.5,
    # Or we can calculate overall standard deviation 
  'sigma_t': water.temp.std()
})


# So, now that we have estimated within-group, common cause variation via  
# σ short (sigma_s) and the standard error (se), what can we say about our process?

stat_t
stat_s





## 2.4 Average and Standard Deviation Charts  #############################

# The preferred method for measuring within-group variability  
# is the standard deviation, rather than the range, so  
# we generally recommend (a) Average ( X̄ ) and Standard  
# Deviation ( S ) charts over (b) Average ( X̄ ) and  
# Range ( R ) charts.


labels = pd.DataFrame({
  'time': [ stat_s.time.max(), stat_s.time.max(), stat_s.time.max() ],
  'type': ['xbbar', 'upper', 'lower'],
  'name': ['mean', '+3 s', '-3 s'],
  'value': [stat_s.xbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
})
labels['value'] = round(labels.value, 2)
labels['text'] = labels.name + " = " + labels.value.astype(str)

(ggplot() +
  geom_hline(
    data = stat_t,
    mapping = aes(yintercept = 'xbbar'), color = "lightgrey") +
  geom_ribbon(
    data = stat_s, 
    mapping = aes(x = 'time', ymin = 'lower', ymax = 'upper'),
    fill = "steelblue", alpha = 0.2) +
  geom_line(
    data = stat_s, 
    mapping = aes(x = 'time', y = 'xbar'), size = 1) +
  geom_point(
    data = stat_s,
    mapping = aes(x = 'time', y = 'xbar'), size = 5)  +
  geom_label(
    data = labels, 
    mapping = aes(x = 'time', y = 'value', label = 'text'),
    # notice that hjust = 1 is instead in python 'ha = "right"'
    ha = 'right') +
   labs(x = "Time (Subgroups)", y = "Average",
         subtitle = "Average and Standard Deviation Chart")
)

# This tells us that excitingly, our onsen temperatures  
# are quite firmly within range. While the average  
# varies quite a bit, it remains comfortably within  
# 3 standard deviations of the mean.


# LEARNING CHECK 2 ################################################

## QUESTION ######################################################

# Well, that was nifty, but can we do it all  
# over again for pH? Make some rad upper and lower  
# confidence intervals for X̄ for pH!


## ANSWER ######################################################

# Calculate these statistics of interest!

# Heck, let's make ourselves a get_stat_s() function.

def get_stat_s(x, y):
  # Put x and y into a data.frame
  data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
  
  stat_s = data.groupby('x').apply(lambda g: pd.Series({
    # Return each time
    'time': g['x'].values[0],
    # within group mean
    'xbar': g['y'].mean(),
    # within-group range
    'r': g['y'].max() - g['y'].min(),
    # within group standard deviation
    'sd': g['y'].std(),
    # within group sample size n
    'nw': g['y'].count(),
    # within group degrees of freedom 
    'df': g['y'].count() - 1
  }))

  
  # Last, we'll calculate sigma_short (within-group variance)
  stat_s = stat_s.assign(sigma_s = lambda g: (sum(g.sd**2)/len(g.sd**2))**0.5)
  
  # And get standard error (in a way that retains each subgroup's sample size!)
  stat_s = stat_s.assign(se = lambda g: g.sigma_s / g.nw**0.5)
  
  # Calculate 6-sigma control limits!
  stat_s = stat_s.assign(upper = lambda g: g.xbar.mean() + 3*g.se)
  stat_s = stat_s.assign(lower = lambda g: g.xbar.mean() - 3*g.se)

  return stat_s

# Calculate within-group stats!
stat_s = get_stat_s(x = water.time, y = water.ph)


stat_s # view result!


# Let's write ourselves a get_labels() function, that process a stat_s dataframe.

def get_labels(data):
  labels = pd.DataFrame({
    'time': [ stat_s.time.max(), stat_s.time.max(), stat_s.time.max() ],
    'type': ['xbbar', 'upper', 'lower'],
    'name': ['mean', '+3 s', '-3 s'],
    'value': [stat_s.xbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = round(labels.value, 2)
  labels['text'] = labels.name + " = " + labels.value.astype(str)
  return labels

# Generate labels!
labels = get_labels(stat_s)

# Let's write ourselves a get_stat_t() function...

def get_stat_t(x, y):
  # To get between-group estimates....
  stat_t = pd.DataFrame({
    'xbbar': [ stat_s.xbar.mean() ],
    'rbar' : [ stat_s.r.mean() ],
    'sdbar' : [ stat_s.sd.mean() ],
    # We can also recalculate sigma_short here too
    'sigma_s': (sum(stat_s.sd**2) / len(stat_s.sd**2))**0.5,
      # Or we can calculate overall standard deviation 
    'sigma_t': water.temp.std()
  })

  return stat_t

# Calculate an extra quantity
extra = pd.DataFrame({'xbbar': [stat_s.xbar.mean()] })

(ggplot() +
  geom_hline(
    data = extra,
    mapping = aes(yintercept = 'xbbar'), color = "lightgrey") +
  geom_ribbon(
    data = stat_s, 
    mapping = aes(x = 'time', ymin = 'lower', ymax = 'upper'),
    fill = "steelblue", alpha = 0.2) +
  geom_line(
    data = stat_s, 
    mapping = aes(x = 'time', y = 'xbar'), size = 1) +
  geom_point(
    data = stat_s,
    mapping = aes(x = 'time', y = 'xbar'), size = 5)  +
  geom_label(
    data = labels, 
    mapping = aes(x = 'time', y = 'value', label = 'text'),
    # notice that hjust = 1 is instead in python 'ha = "right"'
    ha = 'right') +
   labs(x = "Time (Subgroups)", y = "Average",
         subtitle = "Average and Standard Deviation Chart")
)


# This tells us that excitingly, 
# our onsen temperatures are quite firmly within range. 
# While the average varies quite a bit,
# it remains comfortably within 3 standard deviations of the mean.


# We could also make a jumbo function to do all of this!


def ggavgsd(x, y):
  # Put x and y into a data.frame
  data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
  
  stat_s = data.groupby('x').apply(lambda g: pd.Series({
    # Return each time
    'time': g['x'].values[0],
    # within group mean
    'xbar': g['y'].mean(),
    # within-group range
    'r': g['y'].max() - g['y'].min(),
    # within group standard deviation
    'sd': g['y'].std(),
    # within group sample size n
    'nw': g['y'].count(),
    # within group degrees of freedom 
    'df': g['y'].count() - 1
  }))

  # Last, we'll calculate sigma_short (within-group variance)
  stat_s = stat_s.assign(sigma_s = lambda g: (sum(g.sd**2)/len(g.sd**2))**0.5)
  
  # And get standard error (in a way that retains each subgroup's sample size!)
  stat_s = stat_s.assign(se = lambda g: g.sigma_s / g.nw**0.5)
  
  # Calculate 6-sigma control limits!
  stat_s = stat_s.assign(upper = lambda g: g.xbar.mean() + 3*g.se)
  stat_s = stat_s.assign(lower = lambda g: g.xbar.mean() - 3*g.se)

  # Generate labels!
  labels = pd.DataFrame({
    'time': [ stat_s.time.max(), stat_s.time.max(), stat_s.time.max() ],
    'type': ['xbbar', 'upper', 'lower'],
    'name': ['mean', '+3 s', '-3 s'],
    'value': [stat_s.xbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = round(labels.value, 2)
  labels['text'] = labels.name + " = " + labels.value.astype(str)


  # Calculate the grand mean
  extra = pd.DataFrame({'xbbar': [stat_s.xbar.mean()] })

  # Generate plot
  gg = (ggplot() +
    geom_hline(
      data = extra,
      mapping = aes(yintercept = 'xbbar'), color = "lightgrey") +
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = 'time', ymin = 'lower', ymax = 'upper'),
      fill = "steelblue", alpha = 0.2) +
    geom_line(
      data = stat_s, 
      mapping = aes(x = 'time', y = 'xbar'), size = 1) +
    geom_point(
      data = stat_s,
      mapping = aes(x = 'time', y = 'xbar'), size = 5)  +
    geom_label(
      data = labels, 
      mapping = aes(x = 'time', y = 'value', label = 'text'),
      # notice that hjust = 1 is instead in python 'ha = "right"'
      ha = 'right') +
     labs(x = "Time (Subgroups)", y = "Average",
           subtitle = "Average and Standard Deviation Chart")
    )
  
  return gg

# Run it!
ggavgsd(x = water.time, y = water.ph)




# 3. Moving Range Charts ############################################


## 3.1 Individual and Moving Range Charts

# Suppose we only had 1 observation per subgroup! 
# There’s no way to calculate standard deviation for that 
# - after all, there’s no variation within each subgroup! 
# Instead, we can generate an individual and moving range chart.


# Suppose we sample just the first out of each our months.
indiv = water[water['id'].isin([1, 21, 41, 61, 81, 101, 121, 141])]

# The average moving range ̄mRbar aptly refers to  
# the average of the moving Range mR, the difference  
# in values over time. We can calculate the moving  
# range using the diff() function on a vector like  
# temp, shown below. abs() converts each value to  
# be positive, since ranges are always 0 to infinity.

# Let's see our original values
indiv.temp

# diff() gets range between second and first, 
# third and second, and so on
indiv.temp.diff().abs()



# Just like all statistics, mRbar too has its own  
# distribution, containing a range of slightly higher  
# and lower ̄mR statistics we might have gotten had  
# our sample been just slightly different due to  
# chance. As a result, we will want to estimate a  
# confidence interval around ̄mR, but how are we  
# to do that if we have no statistic like σ to  
# capture that variation?

# Well, good news: We can approximate σs by taking  
# the ratio of ̄mRbar over a factor called d2. What  
# is d2? I’m glad you asked!

# σ short ~  mRbar / d2



## 3.2 Factors d2 and Friends ############################3
# 
# As discussed above, any statistics has a latent  
# distribution of other values you might have gotten  
# for your statistic had your sample been just slightly  
# different due to random error. Fun fact: we can  
# actually see those distributions pretty easily thanks  
# to simulation!
# 
# Suppose we have a subgroup of size n = 1, so  
# we calculate a moving range of length 1.
# 
# This subgroup and its moving range is just one of  
# the possible subgroups we could have encountered by  
# chance, so we can think of it as a random draw  
# from an archetypal normal distribution (mean = 0  
# and sd = 1).
# 
# If we take enough samples of moving ranges from  
# that distribution, we can plot the distribution. Below,  
# we take n = 10000 samples with rnorm() and plot  
# the vector with hist().
# 
# We find a beautiful distribution of moving range  
# statistics for n=1 size subgroups.

mrsim = rnorm(n = 10000).diff().abs().dropna()
hist(mrsim)


# Much like k factors in the exponential distribution (we'll learn these soon),  
# we can use this distribution of mR stats to produce  
# a series of factors that can help us estimate any  
# upper or lower confidence interval in a moving range  
# distribution.

# For example, we can calculate:

# d2, the mean of this archetypal mR distribution.

# d3, the standard deviation of this mR distribution.

# Technically, d2 is a ratio, which says that in  
# a distribution with a standard deviation of 1, the  
# mean mR is d2. In other words, d2 = (mRbar,n=1)/(σ,n=1). 

# So, if we have observed  
# a real life average moving range mRbar Robserved, n = 1,  
# we can use this d2 factor to convert out of units  
# of 1 σ, n = 1 into units the σshort of  
# our observed data!

# For example, the mean of our vector mrsim, for subgroup size n = 1, 
# says that d2 (mean of these mR stats) is...
mrsim.mean()


# While d3 (standard deviation is...)
mrsim.std()


# But why stop there? We can calculate loads of other
# interesting statistics!
# For example, these statistics 
# estimate the median, upper 90, and upper 95% of the distribution! 
mrsim.quantile(q = [0.5, 0.9, 0.95]).round(3)



## 3.3 Estimating σ short for Moving Range Statistics ##################3


# Let’s apply our new knowledge about d2 
# to calculate some upper bounds ( +3σ )
# for our average moving range estimates!

# Get moving range over time
istat_s = pd.DataFrame({
  'time': indiv.time.iloc[1:],
  'mr': indiv.temp.diff().abs().dropna()
})
# Get average moving range
istat_s['mrbar'] = istat_s.mr.mean()
# Get d2 statistic
istat_s['d2'] = rnorm(n = 10000, mean = 0, sd = 1).diff().abs().dropna().mean()
# Approximate sigma s
istat_s['sigma_s'] = istat_s.mrbar / istat_s.d2
# Our subgroup size was 1, right?
istat_s['n'] = 1
# so this means that sigma_s just equals the standard error here
istat_s['se'] = istat_s.sigma_s / istat_s.n**0.5
# compute upper 3-se bound
istat_s['upper'] = istat_s.mrbar + 3 * istat_s.se
# and lower ALWAYS equals 0 for moving range
istat_s['lower'] = 0

# Why stop there? Let’s visualize it!

# Generate labels!
labels = pd.DataFrame({
  'time': [ istat_s.time.max(), istat_s.time.max(), istat_s.time.max() ],
  'name': ['mean', '+3 s', 'lower'],
  'value': [istat_s.mrbar.mean(), istat_s.upper.max(), istat_s.lower.min()]
})
labels['value'] = round(labels.value, 2)
labels['text'] = labels.name + " = " + labels.value.astype(str)


# Calculate the grand mean
extra = pd.DataFrame({'mrbar': [istat_s.mrbar.mean()] })

# Generate plot
gg = (ggplot() +
  geom_hline(
    data = extra,
    mapping = aes(yintercept = 'mrbar'), color = "lightgrey") +
  geom_ribbon(
    data = istat_s, 
    mapping = aes(x = 'time', ymin = 'lower', ymax = 'upper'),
    fill = "steelblue", alpha = 0.2) +
  geom_line(
    data = istat_s, 
    mapping = aes(x = 'time', y = 'mr'), size = 1) +
  geom_point(
    data = istat_s,
    mapping = aes(x = 'time', y = 'mr'), size = 5)  +
  geom_label(
    data = labels, 
    mapping = aes(x = 'time', y = 'value', label = 'text'),
    # notice that hjust = 1 is instead in python 'ha = "right"'
    ha = 'right') +
   labs(x = "Time (Subgroups)", y = "Moving Range",
         subtitle = "Moving Range Chart")
  )



# 4. Constants #####################################3

## 4.1 Find any dx Factor   ####################

# While our book writes extensively about d2 and  
# other dwhatever factors, it’s not strictly necessary  
# to calculate them unless you need them. Usually,  
# we do this when we can’t calculate the standard  
# deviation normally (eg. when we have only moving  
# range statistics or only a subgroup sample size  
# of n=1). If you’re working with full data from  
# your process though, you can easily calculate σshort  
# right from the empirical data, without ever needing  
# to use dx factors.
# 
# But let’s say you did need a dx factor for a  
# subgroup range of a given sample size n = 1, 2,  
# 3.... n. Could we calculate some kind of function  
# to give us it?
# 
# Funny you should ask! I’ve written a little helper  
# function you can use.

def dn(n, reps = 10000):
  # testing values
  # n = 3; reps = 10000

  sims = pd.DataFrame({'rep':  pd.Series(range(reps))+1, 'n': n })

  # For each replicate, simulate the ranges of n values
  sims = sims.groupby('rep').apply(lambda g: pd.Series({ 
    'r': rnorm(n = g.n, mean = 0, sd = 1).quantile(q = [0,1]).diff().abs().dropna()
    })
    # Pivot result into a data.frame
  ).explode('r')
  
  # Calculate
  stats = pd.DataFrame({
    # mean range
    'd2': sims.mean(),
    # standard deviation of ranges
    'd3': sims.std()
  })
  # and constants for obtaining lower and upper ci for rbar
  stats['D3'] = 1 - 3*stats.d3/stats.d2  
  stats['D4'] = 1 + 3*stats.d3/stats.d2  
  # Sometimes D3 goes negative; we need to bound it at zero
  # For any cases where D3 goes negative, bound it at zero.
  stats['D3'][stats['D3'] < 0] = 0
  
  return stats



# Let's try it, where subgroup size is n = 2
dn(n = 2)


# Let's get the constants we need too.
# Each of our samples has a sample size of 20
d = dn(n = 20)

# Check it!
d


## 4.2 Using dx factors ###########################

# Using dn(), we can make a quick approximation for the
# upper and lower control limits for the grand range Rbar 
# as well (as opposed to the grand moving range mRbar )

# Make group-wise calculations...
stat_w = water.groupby('time').apply(lambda g: pd.Series({
  # get withingroup range
  'r': g.temp.quantile(q=[0,1]).diff().abs().dropna(),
  # get subgroup size
  'n_w': g.temp.shape[0]
  # pivot result longer
})).explode(['r', 'n_w']
  # assign the time back as a column
  ).assign(
  time = lambda x: x.index)

# Let's get average within group range for temperature...
stat = pd.DataFrame({
  'rbar': [ stat_w.r.mean() ], # get rbar...
  'n_w':  stat_w.n_w.unique().astype(int) }) # assuming constant subgroup size...

# Check it!
stat

# We find that dn() gives us constants D3 and D4... 
mydstat = dn(n = stat.n_w[0] )


#And use these constants to estimate the upper and lower CI for rbar!
stat['rbar_lower'] = stat.rbar[0] * mydstat.D3[0]
stat['rbar_upper'] = stat.rbar[0] * mydstat.D4[0]

# So quick! You could use these values to make a range chart now.

del stat, stat_w



# 4.3 Finding any bx Factor ############################

# We might also want to know how much the standard  
# deviation could possibly vary due to sampling error.  
# To figure this out, we’ll simulate many many standard  
# deviations from a normal distribution, like in dn(),  
# for a given subgroup size n.
# 
# Then, we can calculate some quantities of interest  
# like C4 (the mean standard deviation from an archetypal  
# normal distribution), B3 (a multiplier for getting  
# the lower control limit for 3 sigmas), and B4 (a  
# multiplier for getting the upper control limit for  
# 3 sigmas.)



def bn(n, reps = 10000):
  # testing values
  # n = 3; reps = 10000

  sims = pd.DataFrame({'rep':  pd.Series(range(reps))+1, 'n': n })

  # For each replicate, simulate the ranges of n values
  sims = sims.groupby('rep').apply(lambda g: pd.Series({ 
    's': rnorm(n = g.n, mean = 0, sd = 1).std()
    })
    # Pivot result into a data.frame
  ).explode('s')
  
  # Calculate
  stats = pd.DataFrame({
    # mean range
    'b2': sims.mean(),
    # standard deviation of ranges
    'b3': sims.std()
  })
  
  stats['C4'] = stats.b2 # sometimes called C4
  stats['A3'] = 3 / (stats.b2 * n**0.5)
  # and constants for obtaining lower and upper ci for rbar
  stats['B3'] = 1 - 3*stats.b3/stats.b2  
  stats['B4'] = 1 + 3*stats.b3/stats.b2  
  # Sometimes B3 goes negative; we need to bound it at zero
  # For any cases where D3 goes negative, bound it at zero.
  stats['B3'][stats['B3'] < 0] = 0
  
  return stats


# Let's apply this to our temp vector.

# First, we’ll calculate the standard deviation within each subgroup,
# saved in stat_w under s.


# Let's get within group standard deviation
stat_w = water.groupby('time').apply(lambda g: pd.Series({
  's': g.temp.std(),
  'n_w': g.temp.shape[0]
}))

# Second, we’ll calculate the average standard deviation across subgroups,
# saved in stat under sbar.

# Let's get average within group standard deviation for temperature...
stat = pd.DataFrame({
  'sbar': [ stat_w.s.mean() ], # get sbar...
  'n_w':  stat_w.n_w.unique().astype(int) }) # assuming constant subgroup size...

stat # view

# Third, we'll get our constants B3 and B4!

# For a subgroup size of 20...
stat.n_w

# Get B constants!
mybstat = bn(n = stat.n_w[0])

# Check them!
mybstat

# Finally, let’s calculate our control limits!

# Bundle together our columns...
stat = pd.concat([stat.reset_index(drop=True), mybstat.reset_index(drop = True)], axis = 1)

# Calculate 3 sigma control limits
stat['sbar_lower'] = stat.sbar * stat.B3
stat['sbar_upper'] = stat.sbar * stat.B4

# Now you’re all ready to make a control chart 
# showing variation in the standard deviation!
stat



# LEARNING CHECK 3 ############################################

## QUESTION ####################################################

# Using our dn() function above, 
# compile for yourself a short table of the  
# d2 and d3 factors for subgroups sized 2 to 10.

# yes, it will take a while to load
dx = pd.concat(
  [dn(2), dn(3), dn(4), dn(5),
   dn(6), dn(7), dn(8), dn(9), dn(10)], 
    axis = 0, ignore_index = True)
dx['n'] = [2,3,4,5,6,7,8,9,10]

# Look at that cool table!
dx



# Conclusion #######################################


# All done! Great work!


# Cleanup
globals().clear()
