library(dplyr)
library(readr)
library(ggplot2)
library(broom)
library(rsm)
library(viridis)
library(metR)

link = "https://bit.ly/gingerbread_test3"
cookies = link %>% read_csv()

cookies

cookies %>% head()

cookies %>% glimpse()

cookies$batch %>% unique() %>% length()

cookies$yum %>% range()

m0 = cookies %>% 
  lm(formula = yum ~ molasses + ginger + cinnamon + butter + flour)

m0
# yum_predicted = 5.5459 + 5.1184 * molasses +
#  0.56 * ginger +
#  0.27 * cinnamon +
#  0.68 * butter +
#  1.24 * flour


m0 %>% glance()



# Interaction effects
# Polynomials (squares)



cookies %>% 
  lm(formula = yum ~ molasses + ginger * cinnamon + butter + flour)

# ginger = +0.59961
# cinnamon = +0.33664
# ginger:cinnamon = -0.02585
# As both increase by 1, we expect XXXX less of the outcome.

5.47320 + 5.11842 * 0 + 
  0*0.68424 + 1.24766*0 +
  # effect of ginger
  0.59961 * 1 + 
  # Effect of cinnamon
  0.33664 * 2 + 
  # Effect of both
  -0.02585 * (1 * 2)



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
  lm(formula = yum ~ molasses + I(molasses^2) + 
       ginger + I(ginger^2) +
       I(molasses * ginger) )

m1 %>% glance()
m1

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



mygrid = tidyr::expand_grid(
  molasses = seq(0, 3, by = 0.25),
  ginger = seq(0, 4, by = 0.25)
) %>%
  mutate(yhat = predict(m1, newdata = tibble(molasses, ginger)))


# expand_grid
library(tidyr)

grid = tidyr::expand_grid(
  molasses = seq(from = 0, to = 3, by = 0.1),
  ginger = seq(from = 0,  to = 3, by = 0.1)
) %>%
  mutate(yhat = predict(m1, newdata = tibble(molasses, ginger)))


cookies$molasses %>% range()
cookies$ginger %>% range()

# Quantity of interest: optimal predictors
grid %>%
  filter(yhat == max(yhat))


grid %>%
  mutate(bin = ggplot2::cut_interval(yhat, length = 10)) %>%
  group_by(bin) %>%
  summarize(count = n()) %>%
  ungroup() %>%
  mutate(total = sum(count),
         percent = count / total)




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


# Miniature example
mygrid = expand_grid(
  molasses = seq(0, 3, by = 0.25),
  ginger = seq(0, 4, by = 0.25)
) %>%
  mutate(yhat = predict(m1, newdata = tibble(molasses, ginger)))

library(viridis)
library(metR)

ggplot() +
  geom_contour_fill(
    data = grid, 
    mapping = aes(x = ginger, y = molasses, z = yhat),
    color = "white", size = 0.75, linetype = "solid", alpha = 1
  ) +
  metR::geom_text_contour(
    data = grid,
    mapping = aes(x = ginger, y= molasses, z = yhat),
    skip = 0, stroke.color = "white", stroke = 0.2,
    label.placer = label_placer_n(1)
  ) +
  scale_fill_viridis(option = "plasma")


# Extended example
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




