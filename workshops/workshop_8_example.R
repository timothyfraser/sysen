
devtools::install_github("timothyfraser/tidyfault")

library(tidyverse)
library(tidyfault)

data("fakenodes")
data("fakeedges")

fakenodes %>% View()

fakeedges %>% View()

# Curate us a data.frame of all our gates
g = curate(nodes = fakenodes, edges = fakeedges)

#gg = list(nodes = fakenodes, edges = fakeedges)

# Get coordinates
gg = illustrate(nodes = fakenodes, edges = fakeedges,
           node_key = "id", type = "both")


gg$nodes
gg$edges

ggplot() +
  geom_line(data = gg$edges,
            mapping = aes(x = x, y = y, group = edge_id)) +
  geom_point(data = gg$nodes,
             mapping = aes(x = x, y = y, 
                           fill = type,
                           shape = type),
             size = 10, color = "white") +
  geom_text(data = gg$nodes,
            mapping = aes(x = x, y = y,
                          label = event)) +
  scale_shape_manual(values = c(21, 22, 23, 24)) +
  theme_void(base_size = 14) +
  theme(legend.position = "bottom") 


g = curate(fakenodes, fakeedges)

g %>% equate()

f = g %>% equate() %>% formulate()

f(A = 0.1, B = 0.3, C = 0.2, D = 0.8)


q = curate(fakenodes, fakeedges) %>%
  concentrate(method = "mocus")

q %>%
  tabulate(formula = f)


tibble(
  A = rnorm(n = 100, mean = 0.1, sd = 0.3),
  B = rnorm(n = 100, mean = 0.5, sd = 0.4),
  C = rnorm(n = 100, mean = 0.3, sd = 0.5),
  D = rnorm(n = 100, mean = 0.2, sd = 0.1),
  T = f(A,B,C,D)
) %>%
  summarize(
    mean = mean(T),
    sd = sd(T),
    se = sd(T) / sqrt(n()),
    lower = qnorm(0.025, mean, sd = se),
    upper = qnorm(0.975, mean, sd = se)
  )

f(A = 0.1, B = 0.3, C = 0.2, D = 0.8)





