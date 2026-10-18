# cnn_torch_r.R
# A small CNN in torch that spots cracked concrete in 64 x 64 greyscale panels.
#
# Run by the course on 2026-10-17 (R 4.5.2, torch 0.17.0, CPU): validation escape rate 0.6% (3 of 500), test 0 escapes.
#
# Run it from the folder where you want a workshops/ folder to appear:
#   install.packages(c("torch", "coro", "png", "dplyr", "tibble"))
#   torch::install_torch()   # one-time download of about 560 MB; restart R afterwards
#   Rscript cnn_torch_r.R

library(dplyr)
library(tibble)
library(torch)

torch_set_num_threads(4)   # keep some of your laptop free

# ---- Get the panels (once) ----
url = "https://github.com/timothyfraser/sysen/releases/download/cracks-v1/cracks64.zip"
folder = "workshops/cracks64"
if(!dir.exists(paste0(folder, "/train"))){
  dir.create(folder, recursive = TRUE, showWarnings = FALSE)
  download.file(url, "workshops/cracks64.zip", mode = "wb")
  unzip("workshops/cracks64.zip", exdir = folder)
}

# ---- Read each folder as a dataset ----
# one folder per label; class order is alphabetical, so label 1 = cracked, 2 = sound
panel_folder = dataset(
  name = "panel_folder",
  initialize = function(root, augment = FALSE){
    self$classes = sort(list.files(root))
    files = lapply(self$classes, function(c){ sort(list.files(file.path(root, c), full.names = TRUE)) })
    self$paths = unlist(files)
    # panels are already 64 x 64 greyscale; png::readPNG gives pixels from 0 to 1
    pixels = simplify2array(lapply(self$paths, png::readPNG))      # 64 x 64 x panels
    self$x = torch_tensor(aperm(pixels, c(3, 1, 2)), dtype = torch_float())$unsqueeze(2)  # panels x 1 x 64 x 64
    self$y = torch_tensor(rep(seq_along(self$classes), times = lengths(files)), dtype = torch_long())
    self$augment = augment
  },
  .length = function(){
    length(self$paths)
  },
  .getitem = function(i){
    x = self$x[i, , , ]                                # 1 x 64 x 64
    if(self$augment){                                  # random flips, only for training
      if(torch_rand(1)$item() < 0.5){ x = torch_flip(x, dims = 3) }
      if(torch_rand(1)$item() < 0.5){ x = torch_flip(x, dims = 2) }
    }
    list(x = x, y = self$y[i])
  }
)

train_data = panel_folder(paste0(folder, "/train"), augment = TRUE)
valid_data = panel_folder(paste0(folder, "/valid"))
test_data  = panel_folder(paste0(folder, "/test"))
print(train_data$classes)   # "cracked" "sound"
print(c(length(train_data), length(valid_data), length(test_data)))

# ---- The network ----
torch_manual_seed(5300)
model = nn_sequential(
  nn_conv2d(1, 16, kernel_size = 3, padding = 1),  nn_relu(), nn_max_pool2d(2),  # 64x64 -> 32x32
  nn_conv2d(16, 32, kernel_size = 3, padding = 1), nn_relu(), nn_max_pool2d(2),  # 32x32 -> 16x16
  nn_conv2d(32, 64, kernel_size = 3, padding = 1), nn_relu(), nn_max_pool2d(2),  # 16x16 -> 8x8
  nn_flatten(),                                                                   # 64 x 8 x 8 = 4,096 numbers
  nn_linear(64 * 8 * 8, 64), nn_relu(),
  nn_linear(64, 1)                                                                # one output
)

# ---- Data loaders ----
train_loader = dataloader(train_data, batch_size = 64, shuffle = TRUE)
valid_loader = dataloader(valid_data, batch_size = 256)
test_loader  = dataloader(test_data,  batch_size = 256)

# ---- Training ----
# 1 if cracked (label 1), 0 if sound (label 2), shaped as a column
to_target = function(y){ (y == 1)$to(dtype = torch_float())$unsqueeze(2) }

optimizer = optim_adamw(model$parameters, lr = 0.001, weight_decay = 0.0001)

# average loss over a whole data loader, without training
evaluate_loss = function(loader){
  model$eval()
  losses = c()
  with_no_grad({
    coro::loop(for(batch in loader){
      loss = nnf_binary_cross_entropy_with_logits(model(batch$x), to_target(batch$y))
      losses = c(losses, loss$item())
    })
  })
  mean(losses)
}

# probability of "cracked" for every panel in a data loader, plus the truth
predict_probs = function(loader){
  model$eval()
  probs = c(); labels = c()
  with_no_grad({
    coro::loop(for(batch in loader){
      probs = c(probs, as.vector(as_array(torch_sigmoid(model(batch$x)))))
      labels = c(labels, as.vector(as_array(batch$y)))
    })
  })
  tibble(prob = probs, truth = if_else(labels == 1, "cracked", "sound"))
}

# share of truly cracked panels the model lets through at a threshold
escape_rate = function(results, threshold = 0.5){
  mean(results$prob[results$truth == "cracked"] <= threshold)
}

best_valid = Inf; patience = 5; bad_epochs = 0
history = tibble()
start = Sys.time()
for(epoch in 1:30){
  model$train()
  batch_losses = c()
  coro::loop(for(batch in train_loader){
    optimizer$zero_grad()
    logits = model(batch$x)
    loss = nnf_binary_cross_entropy_with_logits(logits, to_target(batch$y))
    loss$backward()
    optimizer$step()
    batch_losses = c(batch_losses, loss$item())
  })
  valid_loss = evaluate_loss(valid_loader)
  valid_escape = escape_rate(predict_probs(valid_loader))
  history = history %>%
    bind_rows(tibble(epoch = epoch, train = mean(batch_losses), valid = valid_loss))
  cat("Epoch", epoch, "train", round(mean(batch_losses), 3), "valid", round(valid_loss, 3),
      "escape", round(valid_escape, 3),
      "seconds", round(as.numeric(difftime(Sys.time(), start, units = "secs"))), "\n")
  if(valid_loss < best_valid){
    best_valid = valid_loss; bad_epochs = 0
    best_weights = lapply(model$state_dict(), function(t){ t$clone() })
  } else {
    bad_epochs = bad_epochs + 1
    if(bad_epochs >= patience){ break }
  }
}
model$load_state_dict(best_weights)   # go back to the best epoch

# ---- Escapes and false alarms on the validation panels, at 0.5 ----
valid_results = predict_probs(valid_loader) %>%
  mutate(predicted = if_else(prob > 0.5, "cracked", "sound"))
print(count(valid_results, truth, predicted))
cat("escape rate", escape_rate(valid_results), "\n")
cat("false alarm rate", mean(valid_results$prob[valid_results$truth == "sound"] > 0.5), "\n")

# ---- The test panels, once, at the end ----
test_results = predict_probs(test_loader) %>%
  mutate(predicted = if_else(prob > 0.5, "cracked", "sound"))
print(count(test_results, truth, predicted))
