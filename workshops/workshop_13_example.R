
library(tidyverse)
library(broom)


lattes = "https://bit.ly/workshop_lattes" %>%
  read_csv()

lattes %>% 
  glimpse()


groups = lattes %>%
  group_by(machine,milk,syrup,art) %>%
  summarize(xbar = mean(tastiness),
            s = sd(tastiness),
            n = n()) %>%
  ungroup()

groups %>%
  group_by(machine, milk, syrup) %>%
  summarize(xbar_foamy = xbar[art == "foamy"],
            xbar_heart = xbar[art == "heart"],
            dbar = xbar_foamy - xbar_heart) %>%
  ungroup() %>%
#  summarize(dbbar = mean(dbar))
  summarize(dbbar = mean(xbar_foamy) - mean(xbar_heart) )


stat = groups %>%
  summarize(
    dbbar_foamy_heart = mean(xbar[art == "foamy"]) - 
              mean(xbar[art == "heart"]),
    
    dbbar_torani_monin = mean(xbar[syrup == "torani"]) -
      mean(xbar[syrup == "monin"]),
    
    se = sqrt(  sum(  s^2 / n ))
    )

groups %>%
  summarize(
    se = sqrt(  sum(  s^2 / n ))
  )


stat %>%
  mutate(z = qnorm(0.975),
         lower = dbbar_torani_monin - se * z)



