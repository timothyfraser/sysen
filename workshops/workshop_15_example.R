library(tidyverse)
library(broom)
library(rsm)
library(viridis)
library(metR)

link = "https://bit.ly/gingerbread_test3"
cookies = link %>% read_csv()

cookies %>% head()

cookies %>% glimpse()

cookies$batch %>% unique() %>% length()


m0 = cookies %>% 
  lm(formula = yum ~ molasses + ginger + cinnamon + butter + flour)

m0
# yum_predicted = 5.5459 + 5.1184 * molasses +
#  0.56 * ginger +
#  0.27 * cinnamon +
#  0.68 * butter +
#  1.24 * flour


cookies %>% 
  lm(formula = yum ~ molasses + ginger * cinnamon + butter + flour)

# yum_predicted = 5.5459 + 
#  5.11 * molasses +
#  0.59 * ginger +
#  0.33 * cinnamon +
#  0.68 * butter +
#  1.24 * flour +
# -0.025 * ginger * cinnamon


cookies %>% 
  lm(formula = yum ~ molasses + ginger + cinnamon + butter + flour) %>%
  tidy()


cookies %>% 
  lm(formula = yum ~ molasses + ginger + cinnamon + butter + flour) %>%
  tidy()




# First order model - direct effects
cookies %>% 
  lm(formula = yum ~ molasses + ginger)

# Interaction model
cookies %>% 
  lm(formula = yum ~ molasses * ginger)

# First order interaction model
cookies %>% 
  lm(formula = yum ~ molasses + ginger + I(molasses * ginger))

# Second order model
cookies %>% 
  lm(formula = yum ~ molasses + I(molasses^2) + ginger + I(ginger^2))

# Second order interaction model (**Second order model**)
m1 = cookies %>% 
  lm(formula = yum ~ molasses + I(molasses^2) + ginger + I(ginger^2) +
       I(molasses * ginger) )

# Built in function
contour(m1, ~molasses + ginger, image = TRUE)


# As molasses increases, yum increases!!!!

# As ginger increases, yum increases!!

# The effect of an increase in molasses is bigger than
# the effect of an increase in ginger

# the effect of ginger on yum
# DEPENDS on the level of molasses
# AN INTERACTION

# As molasses AND ginger increase, yum increases
m1

mygrid = expand_grid(
  molasses = seq(0, 3, by = 0.25),
  ginger = seq(0, 4, by = 0.25)
) %>%
  mutate(yhat = predict(m1, newdata = tibble(molasses, ginger)))

ggplot() +
  geom_point(data = mygrid, 
             mapping = aes(x = molasses, y = ginger,
                           color = yhat))

ggplot() +
  geom_tile(data = mygrid, 
             mapping = aes(x = molasses, y = ginger,
                           fill = yhat))




# Second order interaction model (**Second order model**)
m1 = cookies %>% 
  lm(formula = yum ~ molasses + I(molasses^2) + ginger + I(ginger^2) +
       I(molasses * ginger) )

mygrid = expand_grid(
  molasses = seq(0, 3, by = 0.25),
  ginger = seq(0, 4, by = 0.25)
) %>%
  mutate(yhat = predict(m1, newdata = tibble(molasses, ginger)))

library(viridis)
library(metR)

ggplot() +
  # Real code
  geom_contour_fill(
    data = mygrid, 
    mapping = aes(x = molasses, y = ginger, z = yhat),
    color = "white", size = 0.75, linetype = "solid",
    alpha = 1) +
  metR::geom_text_contour(
    data = mygrid, 
    mapping = aes(x = molasses, y= ginger, z = yhat), 
    skip = 0, stroke.color = "white", stroke = 0.2,
    label.placer = label_placer_n(1)) +
  # fluff
  scale_fill_viridis(option = "plasma") +
  labs(x = "Molasses (cups)",
       y = "Ginger (tablespoons)",
       title = "Hey come look at my cool contour plot!",
       subtitle = "No really, look at my cool contour plot!",
       caption = "By the way, hello",
       fill = "Predicted\nYum\nFactor") +
  theme_classic(base_size = 14) +
  theme(axis.line = element_blank())




# Second order interaction model (**Second order model**)
m2 = cookies %>% 
  lm(formula = yum ~ molasses + ginger + cinnamon + butter + flour +
       I(molasses^2) + I(ginger^2) + I(cinnamon^2) + 
       I(butter^2) + I(flour^2) +
       molasses * ginger * cinnamon * butter * flour)

m2 %>% glance()

m2 %>% tidy()



mygrid = expand_grid(
  molasses = seq(0, 5, by = 0.5),
  ginger = seq(0, 4, by = 0.5),
  cinnamon = c(0, 1, 2),
  butter = 1,
  flour = 1
) %>%
  mutate(yhat = predict(m2, newdata = tibble(molasses, ginger,
                                             cinnamon, butter,
                                             flour)))


ggplot() +
  # Real code
  geom_contour_fill(
    data = mygrid, 
    mapping = aes(x = molasses, y = ginger, z = yhat),
    color = "white", size = 0.75, linetype = "solid",
    alpha = 1) +
  metR::geom_text_contour(
    data = mygrid, 
    mapping = aes(x = molasses, y= ginger, z = yhat), 
    skip = 0, stroke.color = "white", stroke = 0.2,
    label.placer = label_placer_n(1)) +
  facet_wrap(~cinnamon) +
  
  # fluff
  scale_fill_viridis(option = "plasma") +
  labs(x = "Molasses (cups)",
       y = "Ginger (tablespoons)",
       title = "Hey come look at my cool contour plot!",
       subtitle = "No really, look at my cool contour plot!",
       caption = "By the way, hello",
       fill = "Predicted\nYum\nFactor") +
  theme_classic(base_size = 14) +
  theme(axis.line = element_blank())






