# cnn_plain_net.R: a plain (non-convolutional) network on the 16 x 16 crack panels.
# Reads workshops/cracks16.csv; prints validation accuracy, escape rate, weights.
library(readr)
library(dplyr)
library(nnet)

cracks = read_csv("workshops/cracks16.csv", show_col_types = FALSE)
pixels = function(d) as.matrix(select(d, starts_with("p"))) / 255   # scale to 0-1
train = filter(cracks, split == "train")
valid = filter(cracks, split == "valid")

set.seed(5300)
net = nnet(x = pixels(train), y = train$label, size = 8, decay = 0.01,
           maxit = 200, MaxNWts = 5000, trace = FALSE)

prob = as.numeric(predict(net, pixels(valid)))
guess = as.integer(prob > 0.5)                                  # threshold 0.5
accuracy = mean(guess == valid$label)
escape = mean(guess[valid$label == 1] == 0)                     # cracked, called sound
cat("validation accuracy:", round(accuracy, 3), "\n")
cat("escape rate:", round(escape, 3), "\n")
cat("weights:", length(net$wts), "\n")
