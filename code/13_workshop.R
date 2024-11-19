library(dplyr)
library(ggplot2)
library(broom)

# Load in data!
# If you upload it to your workshops folder, read it in like this...
lattes = read_csv("workshops/lattes.csv")

lattes %>% glimpse()

lattes$machine %>% unique() %>% length()
lattes$milk %>% unique() %>% length()
lattes$syrup %>% unique() %>% length()
lattes$art %>% unique() %>% length()



# Let's make a data.frame 'groups'
groups = lattes %>% 
  # For each unique pairing of treatments tested,
  group_by(machine, milk, syrup, art) %>%
  # Return one row containing these summary statistics
  summarize(xbar = mean(tastiness),
            s = sd(tastiness),
            n = n()) %>%
  ungroup() %>%
  mutate(id = 1:n()) %>%
  ungroup()

groups


myse = groups %>%
  summarize(
    se = sqrt( sum(s^2 / n)  )
  )

#  se = s/sqrt(n)
#  se^2 = s^2 / n


myse$se



stats = groups %>%
  summarize(
    name = "Heart - Foamy",
    xbar1 = mean(xbar[art == "foamy"]),
    xbar2 = mean(xbar[art == "heart"]),
    dbar = xbar2 - xbar1,
    se = myse$se,
    z = qnorm(0.975),
    lower = dbar - se * z,
    upper = dbar + se * z 
  )

stats

ggplot() +
  geom_crossbar(data = stats,
                mapping = aes(x = name, y = dbar, ymin = lower, ymax = upper)) +
  geom_hline(yintercept = 0, linetype = "dashed")


groups
# Interaction Effect
stats = groups %>%
  summarize(
    name = "Heart x Torani (HH) - Foamy x Monin (LL)",
    xbar1 = xbar[art == "foamy" & syrup == "monin" ] %>% mean(),
    xbar2 = xbar[art == "heart" & syrup == "torani"] %>% mean(),
    dbar = xbar2 - xbar1
  )

stats

# Interaction Effect for just Oatmilk
stats = groups %>%
  summarize(
    name = "Heart x Torani x Oat (HHH) - Foamy x Monin x Oat (LLH)",
    xbar1 = xbar[art == "foamy" & syrup == "monin" & milk == "oat"] %>% mean(),
    xbar2 = xbar[art == "heart" & syrup == "torani" & milk == "oat"] %>% mean(),
    dbar = xbar2 - xbar1
  )
stats


# Interaction Effect for just Oatmilk
stats = groups %>%
  summarize(
    name = "Heart x Torani x Oat (HHH) - Foamy x Monin x Skim (LLL)",
    xbar1 = xbar[art == "foamy" & syrup == "monin" & milk == "skim"] %>% mean(),
    xbar2 = xbar[art == "heart" & syrup == "torani" & milk == "oat"] %>% mean(),
    dbar = xbar2 - xbar1
  )
stats


groups
# Interaction Effect
stats = groups %>%
  summarize(
    name_a = "Heart x Torani (HH) \nvs. Foamy x Monin (LL)",
    xbar1 = xbar[art == "foamy" & syrup == "monin" ] %>% mean(),
    xbar2 = xbar[art == "heart" & syrup == "torani"] %>% mean(),
    dbar_heart_torani = xbar2 - xbar1,
    
    name_b = "Heart x Oat (HH) \nvs. Foamy x Skim (LL)",
    xbar3 = xbar[art == "foamy" & milk == "skim" ] %>% mean(),
    xbar4 = xbar[art == "heart" & milk == "oat"] %>% mean(),
    dbar_heart_oat = xbar4 - xbar3
    
  )

stats %>%
  glimpse()


ggdat = tibble(
  x = c(stats$name_a, stats$name_b ),
  y = c(stats$dbar_heart_torani, stats$dbar_heart_oat),
  se = myse$se,
  z = qnorm(0.975),
  lower = y - z * se,
  upper = y + z * se
)

ggplot() +
  geom_crossbar(
    data = ggdat, 
    mapping = aes(x = x, y = y,
                  ymin = lower, ymax = upper),
    fill = "steelblue") +
  geom_hline(yintercept = 0, linetype = "dashed")

