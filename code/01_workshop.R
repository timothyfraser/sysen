# Lesson 0: Introduction!
# Tim Fraser
# This workshop code summarize basic operations in R.
# Check out timothyfraser.com/sigma for more.

# Let's load some packages
# install.packages("dplyr") # install dplyr
# install.packages("ggplot2") # install ggplot2
library(dplyr) # turn on dplyr
library(ggplot2) # turn on ggplot2

# Comments! 
# This is addition!
1+2

1+2
1*5
2^3
(2*3)
((2*2)+3)

4^0.5
4^(1/2)
4^(1/3)
sqrt(4)





myobject = c(1,2,3,4,5)

myobject

myobject + 1

myobject *2

c("corgi", "dalmatian", "terriers") + 1
c("corgi", "dalmatian", "terriers", 1)



d = data.frame(
  doggies = c("corgis", "dalmatians", "terriers"),
  count = c(5, 3, 2)
)

d$count
d$count + 1
d$count + d$count

d$count = d$count + 1

# Not this!
# d = d$count + 1

# dataframe[row,column]
d[1,1]
d[3,2]
d[3, ]
d[, 2]

# adding columns
d$weight = c(100, 40, 20)

d$weight2 = c(100, 40, NA)

# using dplyr function bind_rows()
bind_rows(
  data.frame(x = c(1,2), y= c(3,4)),
  data.frame(x=  c(3,4), y = c(5,6))
)
bind_rows(
  data.frame(x = c(1,2), y= c(3,4), z= c(3,4)),
  data.frame(x=  c(3,4), y = c(5,6))
)
# from dplyr package
tibble(
  x = c(1,2), y= c(3,4), z= c(3,4)
)


d$weight2 = NULL

d %>% select(-weight2)






c(1,2,3,4)

c("corgi", "dalmatian") * 2

c(1,2,3,4) * 2

c(1,2,3,4) * c(1,2,3,4)

c(1,2,3,4) %*% c(1,2,3,4)


sqrt(64)
64^(1/3)
8^2






coffee = c(2, 4, 5, 6, 7, 3,2, 3,4)
coffee

sales = c(3.4,2.5, 3.2, 6.3, 4, 3, 6, 7, 8)
sales

coffee * 2

# coffees per dollar
coffee / sales
# dollars per coffee
sales / coffee



# Let's try working with data.frames.

data.frame(coffee, sales)

dat = data.frame(coffee = coffee, sales = sales)

dat

# We can index specific values, rows, and columns...
dat[,1]
dat[1,]
dat[1:3,]
dat[, 1:2]




# And we can use dplyr functions to do actions to dataframes.
#    %>%    



select(dat, coffee)
dat %>% select(coffee)

head(dat, 2)
dat %>% select(coffee) %>% head(2)


dat %>% 
  select(coffee) %>% 
  head(2)


dat %>%
  select(coffee) %>%
  slice(1:2)

dat %>%
  select(coffee) %>%
  filter(coffee > 4)


dat %>%
  filter(coffee == 4)
dat %>%
  filter(coffee >= 4)
dat %>%
  filter(coffee <= 4)

dat %>%
  filter(coffee %in% c(4, 5))

dat %>%
  summarize(avg = mean(coffee))

# find the average and the standard deviation - yeah!
dat %>%
  summarize(avg = mean(coffee),
            stdev = sd(coffee))

data.frame( 
  adorable = c(1, 0),
  glasses = c("yes", "no")
)

# get 2000 values
nums = data.frame(x = 1:2000)
nums # only shows first 1000 values
# if you assign you get no output...
num2 = nums %>% slice(1000:1003)


# Clear my environment
rm(list = ls())

# Here's a brief test of using dplyr-style functions
# with dplyr 
# diamonds is a dataset loaded within ggplot2
library(dplyr)
library(ggplot2)

# Get the mean price per diamond cut
diamonds %>%
  group_by(cut) %>%
  summarize(price = mean(price ))

# Arranging
diamonds %>%
  arrange(price) %>%
  head()


# Filtering
diamonds %>%
  filter(carat < 0.23) %>%
  head()


diamonds %>%
  rename(CUT = cut, COLOR='color')


diamonds %>%
  arrange(color)

diamonds %>%
  group_by(cut) %>%
  summarize(price = mean(price))



# We can clean up using rm()
rm(list = ls())
