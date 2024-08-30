# 05_training.py
# Training: Probability
# Pairs with R training:
# https://timothyfraser.com/sigma/probability.html
# Tim Fraser

# Getting Started ############################

## Load Packages ############################
# Install main python packages for this script
# !pip install pandas
import pandas as pd # Import pandas functions


# Key Functions #######################################

# pd.concat = bind_rows() equivalent
# pd.assign = mutate() equivalent

mycoffee = pd.concat(
  [
    # Make first data.frame
    pd.DataFrame({
        # Containing these vectors style and price
        'style': ["latte", "cappuccino", "americano"],
        'price': [5, 4, 3] }),
  # Make second data.frame
    pd.DataFrame({
        # Containing these vectors style and price
        'style': ["coffee", "hot cocoa"],
        'price': [3,2],
        'shop': ["Gimme Coffee", "Starbucks"]})
  ]
)

# Add a new vector (must be of same length as data.frame)
# vector is number of those drinks purchased
mycoffee = mycoffee.assign(purchased = [5,4,10,2,1])

# Pandas has a complicated relationship with the summarize() function in dplyr
# You can achieve much of the same functionality using either pd.agg() or just making a new pd.DataFrame()

pd.DataFrame({
  'mean_price': [ mycoffee.price.mean() ],
  'total_purchased': [ mycoffee.purchased.sum() ]
})

# Alternatively, but not exactly equivalently... 
# mycoffee.agg(
#     mean_price=('price', 'mean'),
#     total_purchased=('purchased', 'sum')
# )


# Probability #######################################


## Conditional Probability ##########################

# You’ve been hired by the Hershey’s Chocolate Company 
# to investigate quality control on their Twizzlers sweets packaging line. 
# At the start of an assembly line, you mixed in 8,000 Red Vines 
# with a sample of 10,000 Twizzlers.

# What’s the probability of a packer picking up a Red Vine on the assembly line?

sweets = pd.DataFrame({
# We know there are 10,000 twizzlers
  'twizzlers': [10000],
# and 8,000 redvines
  'redvines': [8000] })
  # So together, there are 18,000 sweets available
  # So there's a 8000-in-18,000 chance of picking a redvine
sweets = sweets.assign(prob1 = sweets.redvines / (sweets.twizzlers + sweets.redvines))
# An alternative way to write this is using lambda.
# Lambda temporalily assigns that data.frame to be a new variable name, to simplify coding.
# For example, here we assign 'd' to be the data.frame.
# sweets = sweets.assign(prob1 = lambda d: d.redvines / (d.twizzlers + d.redvines))

# Check it!
sweets

# After picking 1 Red Vine,
# there's now 1 less Red Vine in circulation
sweets = sweets.assign(redvines = sweets.redvines - 1)
sweets = sweets.assign(total = sweets.twizzlers + sweets.redvines)
# calculate probability of picking a second red vine 
# now that 1 is gone
sweets = sweets.assign(
  prob2 = sweets.redvines / sweets.total
)
# Finally, multiply the first and second probability together
# When it's this AND that, you multiply
sweets = sweets.assign(prob = sweets.prob1 * sweets.prob2)
sweets # view

# Alternatively, if two events are independent (mutually exclusive), 
# meaning they do not affect each other, you add those probabilities together.

# You dump in a 1000 pieces of Black Licorice. 
# If a packer picks up 2 sweets, what’s the probability 
# it’s a piece of Black Licorice or Red Vines?

# Add a column for black licorice
sweets = sweets.assign(black_licorice = [1000])
# Get total
sweets = sweets.assign(total = sweets.twizzlers + sweets.redvines + sweets.black_licorice)
# Recompute probabilities
sweets = sweets.assign(
  prob1 = sweets.redvines / sweets.total,
  prob2 = sweets.black_licorice / sweets.total)
# When it's this OR that, you add probabilities
sweets = sweets.assign(prob3 = sweets.prob1 + sweets.prob2)
    
sweets

# Fun fact: info is very similar to glimpse
# sweets.info()

del mycoffee, sweets


# Total Probabilities #################################################


# You’ve got 3 bags (E1-to-E3), each containing 3 marbles, 
# each with a different split of red vs. blue marbles.
# If we choose a bag at random and sample a marble at random
# (2 mutually exclusive events), what’s the probability
# that marble will be red ( P(A) )?


# I like to map these out, so I understand visually what all 
# the possible pathways are. Here’s a chart I made (using mermaid),
# where I’ve diagrammed each possible set of actions, like choosing 
# Bag 1 then Marble a (1 pathway), choosing Bag 1 then
# Marble b (a second pathway), etc.

# If we look at the ties to the marbles,
# you’ll see I labeled each tie to a red marble as 1
# and each tie to a blue marble as 0. 
# If we add these pathways up, we’ll get the total probability: 0.67 
# (aka 2/3).

# The key here is knowing that:

# the blue marbles don’t really matter
# we need the probability of choosing a bag
# we need the probability of choosing a red marble in each bag.

# There’s an equal chance of choosing any bag of 3 bags 
# (because random). (If 1 bag were on a really high shelf, 
# then maybe the probabilities would be different, i.e. not random, 
# but let’s assume they’re random this time.)


# there are 3 bags
n_bags = 3

# So....
# In this case, P(Bag1) = P(Bag2) = P(Bag3)
# and P(Bag1) + P(Bag2) + P(Bag3) = 100% = 1.0

# 1/3 chance of picking Bag 1
# written P(Bag1)
pbag1 = 1 / n_bags

# 1/3 chance of picking Bag 2
# written P(Bag2) 
pbag2 = 1 / n_bags

# 1/3 chance of picking Bag 3
# written P(Bag3)
pbag3 = 1 / n_bags

# Check it!
[pbag1, pbag2, pbag3]

# There are 3 marbles in each bag

# Total marbles in Bag 1
m_bag1 = 3
# Total marbles in Bag 2
m_bag2 = 3
# Total marbles in Bag 3
m_bag3 = 3


# So, we can calculate the percentages in each bag.

# percentage of red marbles in Bag 1
# written P(Red|Bag1)
pm_bag1 = 3 / m_bag1

# percentage of red marbles in Bag 2
# written P(Red|Bag2)
pm_bag2 = 1 / m_bag2

# percentage of red marbles in Bag 3
# written P(Red|Bag3)
pm_bag3 = 2 / m_bag3

# Check it!
[pm_bag1, pm_bag2, pm_bag3]

# Selecting Bag 1 and then selecting a Red Marble are interdependent events, so we multiply them.


# For example
# P(Bag1 & Red) = P(Red|Bag1) * P(Bag1)
pm_bag1 * pbag1

# But each pathway (eg. Bag 1 x Marble A) is distinct 
# and independent of the other pathways, so we can add them together.
# P(Bag1 & Red) = P(Red|Bag1) * P(Bag1)
# P(Bag2 & Red) = P(Red|Bag2) * P(Bag2)
# P(Bag3 & Red) = P(Red|Bag3) * P(Bag3)
pm_bag1 * pbag1 + pm_bag2 * pbag2 + pm_bag3 * pbag3


  
  
  
# Could we do this more succinctly?
bags = pd.DataFrame({
  'bag_id' : [1,2,3],
  # For each bag, how many do you get to choose?
  'bags' : [1, 1, 1],
  # For each bag, how many marbles do you get to choose?
  'marbles': [3, 3, 3],
  # For each bag, how many marbles are red?
  'red': [3, 1, 2] 
})

bags

# choosing that bag out of all bags
bags = bags.assign(prob_bag = lambda d: d.bags / sum(d.bags) )
# choosing red out of all marbles in that bag
bags = bags.assign(prob_red = lambda d: d.red / d.marbles)
# choosing BOTH that bag AND a red marble in that bag
bags = bags.assign(prob_bagred = lambda d: d.prob_red * d.prob_bag)
# View it
bags

# Finally, we could just sum the joint probabilities together.
pd.DataFrame({ 'prob_bagred': [ bags.prob_bagred.sum() ] })

# Delete unnecessary data
del bags, n_bags, m_bag1, m_bag2, m_bag3, pbag1, pbag2, pbag3, pm_bag1, pm_bag2, pm_bag3


# Bayes Rule ###############################################

# See chapter for more info.

# Example: Coffee Shop (Incomplete Information)

# A local coffee chain needs your help to analyze
# their supply chain issues.
# They know that their scones help them sell coffee,
# but does their coffee help them sell scones?

# Over the last week,
# when 7 customers bought scones, 
# 3 went on to buy coffee.

# When 3 customers didn’t buy scones,
# just 2 bought coffee.

# In general, 7 out of 10 of customers ever bought scones.

# What’s the probability that a customer will buy a scone,
# given that they just bought coffee?


# We want to know this
p_scone_coffee = pd.NA

# But we know this!
p_coffee_scone = 3/7
p_coffee_no_scone = 2/3
p_scone = 7/10
# AND
# If 7 out of 10 customers ever bought scones,
# then 3 out of 10 NEVER bought scones
p_no_scone = 3 / 10


# Using these 3~4 probabilities, 
# we can deduce the total probability of coffee (the denominator),
# meaning whether you got coffee OR whether you didn’t get coffee.

# Total Prob of Coffee = Getting Cofee + Not getting coffee
p_coffee = p_coffee_scone * p_scone + p_coffee_no_scone * p_no_scone
# Check it!
p_coffee

# So let’s use p_coffee to get the probability of
# getting a scone given that you got coffee!
p_scone_coffee = p_coffee_scone * p_scone / p_coffee
p_scone_coffee # View


# Example: Coffee Shop (Complete Information) ###################

# But, if we do have complete information,
# then we can actually prove Bayes’ Rule quite quickly.

# For example, say those percentages the shop owner gave us 
# were actually meticulously tabulated by a barista. 
# We talk to the barista, and she explains that she can tell us
# right away the proportion of folks who got a scone
# given that they got coffee. 
# She shows us her spreadsheet of orders, 
# listing for each customer, 
# whether they got coffee and whether they got a scone.

orders = pd.DataFrame({
  'coffee': ["yes", "no", "yes", "no", "yes", "yes", "yes", "no", "no", "no"],
  'scone': ["no", "no", "no", "yes", "yes", "yes", "yes", "yes", "yes", "yes"]
  })
  
# We can tabulate these quickly using groupby() with apply(),
# tallying up how many folks did this.

orders.groupby(['coffee', 'scone']).apply(
  lambda x: pd.Series({
    'count':  len(x.coffee)
})
)



# Let's skip to the end and just calculate the proportion directly!
# Out of all people who got coffee, how many got scones?

stat = pd.DataFrame({
    'n_both': [ sum( (orders.scone == 'yes') & (orders.coffee == 'yes')) ],
    'n_coffee': [ sum( (orders.coffee == 'yes'))]
})
stat = stat.assign(proportion = stat.n_both / stat.n_coffee )
stat # view



# Now that we know this, let's prove that Bayes works.

stat = pd.DataFrame({
  # The goal (posterior)
  'p_scone_coffee': [ sum( (orders.scone == 'yes') & (orders.coffee == 'yes')) / sum((orders.coffee == 'yes')) ],
  # The data
  'p_coffee_scone': [ sum((orders.coffee == "yes") & (orders.scone == "yes")) / sum((orders.scone == "yes"))],
  'p_coffee_no_scone': [ sum((orders.coffee == "yes") & (orders.scone == "no")) / sum((orders.scone == "no"))],
  'p_scone': [ sum((orders.scone == "yes")) / sum((orders.coffee == "yes") | (orders.coffee == "no"))],
  'p_no_scone': [ sum((orders.scone == "no")) / sum((orders.coffee == "yes") | (orders.coffee == "no")) ]
})
# Now recalculate the goal, using the data we have collected.
# Does 'bayes' equal 'p_scone_coffee'?
stat = stat.assign(bayes = lambda d: d.p_coffee_scone  * d.p_scone / (d.p_coffee_scone * d.p_scone + d.p_coffee_no_scone * d.p_no_scone) )
stat # view it

# It should! And it does! Tada!

# Extra Examples available in Textbook



globals().clear()

