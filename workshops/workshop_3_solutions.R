
# Load packages
library(dplyr)
library(readr)

# Read in file
la <- read_csv("workshops/la_parishes.csv")

la


la %>% head(3)
head(la, 3)
la %>% 
  head(3)

la %>% 
  tail()


la %>% 
  summarize(mymean = mean(pc_severe),
            mysd = sd(pc_severe),
            note = "I wrote a note to myself")

la %>% 
  head() %>%
  mutate(new = c(1,2,3,4,5,6))


la2 <- la %>%
  head() %>%
  select(parish, coastal)

bind_rows(
  la %>% head(3),
  la %>% tail(3))



