# 03_lesson.R

# Let's learn how to use several new dplyr functions,
# and let's learn how to make our own functions.


# New dplyr functions ##############################
library(dplyr)

# Make a data.frame
chairs = data.frame(
  # unique IDs always help
  id = 1:5,
  # how many people used chair each day
  uses = c(1,5,2,3,4),
  # cost of each chair
  cost = c(30, 50, 40, 100, 20)
)

# mutate a data.frame
chairs %>%
  mutate(value = cost / uses / 365.25)

# overwrite a data.frame
chairs = chairs %>%
  mutate(days = c(200, 300, 2, 50, 75))

chairs

# summarize a data.frame
stat = chairs %>%
  summarize(mttf = mean(days))

# Extract a vector from a data.frame
stat$mttf

# Make a second data.frame
more_chairs = data.frame(
  id = c(6,7),
  uses = c(3, 5),
  cost = c(30, 40)
)

# stack two data.frames together
chairs2 = bind_rows(
  chairs,
  more_chairs
)

chairs2

# doesn't work!
# data.frame(
#   hours = 20:25,
#   hours_later5 = hours + 5
# )

# tibble() makes data.frames but can reference previously created vectors
# does work!
tibble(
  hours = 20:25,
  hours_later5 = hours + 5
)

# Can't do this
# tibble(
#   hours = 20:25,
#   hours_later5 = hours + 5,
#   hours = hours_later5
# )

# Can do this
tibble(
  hours = 20:25,
  hours_later5 = hours + 5) %>%
  mutate(hours = hours_later5)


# Making Functions ########################

# the mathetmatical function for pexp() is this
# F(t) = 1 - e^(-t*lambda)
f = function(t, lambda){ 1 - exp(-1*t*lambda) }

# Why do we care?
f(t = 2, lambda = 0.05)
pexp(2, rate = 0.05)

# Can pass vectors to functions
c(2,5,7,5,8) %>% f(lambda = 0.05)

# Get lots of probabilities fast
f(t = c(2,5,7,5,8), lambda = 0.05)

# Can pass functions to tibbles too
tibble(
  t = c(2,5,7,5,8),
  prob = f(t = t, lambda = 0.05)  
)


# inputs --> process --> output
# function(){ }

# Let's make an addone() function
addone = function(a){  a + 1  }
addone(a = 1)
addone(1)

# This works...
addone = function(a){  
  a + 1  
}

# This works too...
addone = function(a){  
  output = a + 1  
  output
}
addone(a = 1)


# This works too...
addone = function(a){  
  output = a + 1  
  return(output)
}
addone(a = 1)

# This won't work - need to return the output
# addone = function(a){  
#   output = a + 1  
# }
# addone(1)


# Can add default arguments/parameters
addone = function(a = 2){   a + 1   }
addone()
addone(a = 3)

# Can add multiple arguments/parameters
addx = function(a, x){  a + x }
addx(a = 1, x = 2)


addx(a = 1, x = 2)


# Can add testing values, as long as you comment them out
addx = function(a, x){
  # testing values
  # a = 2; x = 3
  
  a + x
  
  # remove(a, x)  
}



addx = function(a, x){
  # testing values
  # a = 2; x = 3
  
  a + x
 
}

addx(a = 5, x = 2)



# All done!

# Cleanup!
rm(list = ls())
