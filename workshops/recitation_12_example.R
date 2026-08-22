# recitation_12

library(tidyverse) # read_csv(), mutate(), summarize()
library(broom) # tidy()

file = "https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/jp_matching_experiment.csv"
jp = file %>% 
  read_csv()

jp$year %>% unique()

jp %>%
  filter(year == 2011 | year == 2017) %>%
  head()

jp %>%
  filter(year == 2011 & year == 2017) %>%
  head()

jp %>%
  filter(year %in% c(2011, 2017)) %>% 
  head()

jp %>%
  filter(year == 2017) %>%
  filter(pref == "Fukushima")

jp %>%
  filter(year == 2017) %>%
  filter(pref == "Fukushima" | pref == "Miyagi")


jp %>%
  filter(year %in% c(2011, 2017)) %>%
  summarize(t.test(income_per_capita ~ year) %>% tidy())


jp %>%
  filter(pref %in% c("Fukushima", "Miyagi")) %>%
  summarize(t.test(pop_women ~ pref) %>% tidy())


jp %>%
  filter(pref %in% c("Fukushima", "Miyagi")) %>%
  summarize(t.test(pop_women ~ pref) %>% tidy())


jp %>% 
  glimpse()






jp$pref %>% unique()
