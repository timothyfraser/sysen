# nn_torch_r.R
# The R code of the "Locally with torch" tab in the Neural Networks in R chapter,
# block by block in page order: a reading copy of exactly what the chapter shows.
#
# Run by the course on 2026-10-17 (R 4.5.2, torch 0.17.0, CPU): 728 / 144 / 158 rows,
# 4,801 parameters, best epoch 103, stopped at 123, test RMSE 5.09 MPa vs 10.2 and 6.85.
#
# Run it from a folder that holds workshops/concrete.csv.

# ---- Install torch (one time) ----
# the packages this chapter uses
install.packages(c("dplyr", "readr", "ggplot2", "broom"))
# torch, plus coro (used to loop over torch dataloaders)
install.packages(c("torch", "coro"))
# one-time download of the libtorch engine (~560 MB)
torch::install_torch()

# ---- Set up your local session ----
library(dplyr)   # data wrangling
library(readr)   # reading csvs
library(ggplot2) # visualization
library(broom)   # tidying model output
library(torch)   # neural networks (Run locally)

concrete = read_csv("workshops/concrete.csv")

# ---- Split the data ----
set.seed(5300)

concrete = concrete %>%
  mutate(set = sample(c("train", "valid", "test"), size = n(), replace = TRUE,
                      prob = c(0.70, 0.15, 0.15)))

train = concrete %>% filter(set == "train")
valid = concrete %>% filter(set == "valid")
test  = concrete %>% filter(set == "test")

concrete %>% count(set)

# ---- Standardize, using the training set only ----
inputs = c("cement", "slag", "ash", "water", "superplasticizer", "coarse", "fine", "age")

# means and standard deviations from the TRAINING data only
x_mean = train %>% select(all_of(inputs)) %>% as.matrix() %>% colMeans()
x_sd   = train %>% select(all_of(inputs)) %>% as.matrix() %>% apply(2, sd)
y_mean = mean(train$strength)
y_sd   = sd(train$strength)

# helper functions to turn a data frame into torch tensors
to_x = function(data){
  data %>%
    select(all_of(inputs)) %>%
    as.matrix() %>%
    scale(center = x_mean, scale = x_sd) %>%
    torch_tensor(dtype = torch_float())
}
to_y = function(data){
  ((data$strength - y_mean) / y_sd) %>%
    matrix(ncol = 1) %>%
    torch_tensor(dtype = torch_float())
}

X_train = to_x(train); y_train = to_y(train)
X_valid = to_x(valid); y_valid = to_y(valid)
X_test  = to_x(test);  y_test  = to_y(test)

X_train$shape

# ---- Build the network ----
torch_manual_seed(5300)

model = nn_sequential(
  nn_linear(8, 64),  nn_relu(),   # hidden layer 1: 8 inputs -> 64 features
  nn_linear(64, 64), nn_relu(),   # hidden layer 2: 64 -> 64 features
  nn_linear(64, 1)                # output: a regression on the last 64 features
)

model

# ---- Train it ----
optimizer = optim_adamw(model$parameters, lr = 0.001, weight_decay = 0.0001)

train_loader = dataloader(tensor_dataset(X_train, y_train), batch_size = 32, shuffle = TRUE)

best_valid = Inf   # best validation loss so far
patience = 20      # how many epochs without improvement before we stop
bad_epochs = 0
history = tibble()

for(epoch in 1:500){

  # 1. Training: one pass through the training data
  model$train()
  batch_losses = c()
  coro::loop(for(batch in train_loader){
    optimizer$zero_grad()                          # clear the old slopes
    yhat = model(batch[[1]])                       # predict
    loss = nnf_mse_loss(yhat, batch[[2]])          # compute the loss
    loss$backward()                                # compute the slopes
    optimizer$step()                               # take a step
    batch_losses = c(batch_losses, loss$item())
  })

  # 2. Validation: how are we doing on data we didn't train on?
  model$eval()
  valid_loss = with_no_grad({ nnf_mse_loss(model(X_valid), y_valid)$item() })

  history = history %>%
    bind_rows(tibble(epoch = epoch, train = mean(batch_losses), valid = valid_loss))

  # 3. Early stopping: keep the best weights; stop if no improvement for a while
  if(valid_loss < best_valid){
    best_valid = valid_loss
    bad_epochs = 0
    best_weights = lapply(model$state_dict(), function(t){ t$clone() })
  } else {
    bad_epochs = bad_epochs + 1
    if(bad_epochs >= patience){ break }
  }
}

model$load_state_dict(best_weights)   # go back to the best epoch

# ---- Plot the loss curves ----
history %>%
  ggplot(mapping = aes(x = epoch)) +
  geom_line(mapping = aes(y = train, color = "Training")) +
  geom_line(mapping = aes(y = valid, color = "Validation")) +
  labs(x = "Epoch", y = "Loss (mean squared error, standardized units)", color = NULL)

# ---- Evaluate on the test set ----
# neural network predictions, converted back to MPa
model$eval()
yhat_nn = with_no_grad({ model(X_test) }) %>% as_array() %>% as.vector()
yhat_nn = yhat_nn * y_sd + y_mean

# regressions trained on the same training rows
m1_train = lm(strength ~ cement + slag + ash + water + superplasticizer + coarse + fine + age,
              data = train)
m2_train = lm(strength ~ cement + slag + ash + water + superplasticizer + coarse + fine + log(age),
              data = train)

rmse = function(yhat, y){ sqrt(mean((yhat - y)^2)) }

tibble(
  model = c("Regression", "Regression with log(age)", "Neural network"),
  test_rmse = c(rmse(predict(m1_train, newdata = test), test$strength),
                rmse(predict(m2_train, newdata = test), test$strength),
                rmse(yhat_nn, test$strength))
)

tibble(observed = test$strength, predicted = yhat_nn) %>%
  ggplot(mapping = aes(x = observed, y = predicted)) +
  geom_point(alpha = 0.5) +
  geom_abline(slope = 1, intercept = 0, color = "red") +
  labs(x = "Observed strength (MPa)", y = "Predicted strength (MPa)")
