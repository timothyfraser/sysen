# cnn_torch_py.py
# A small CNN in torch that spots cracked concrete in 64 x 64 greyscale panels.
# Run it from the folder where you want a workshops/ folder to appear:
#   pip install torch numpy pandas pillow
#   python cnn_torch_py.py
import os, time, copy, zipfile, urllib.request
import numpy as np
import pandas as pd
import torch                                           # neural networks
from torch import nn
from torch.utils.data import Dataset, DataLoader
from PIL import Image                                  # reads the png panels

torch.set_num_threads(4)   # keep some of your laptop free

# ---- Get the panels (once) ----
url = "https://github.com/timothyfraser/sysen/releases/download/cracks-v1/cracks64.zip"
folder = "workshops/cracks64"
if not os.path.isdir(folder + "/train"):
    os.makedirs(folder, exist_ok = True)
    urllib.request.urlretrieve(url, "workshops/cracks64.zip")
    with zipfile.ZipFile("workshops/cracks64.zip") as z:
        z.extractall(folder)

# ---- Read each folder as a dataset ----
# one folder per label; class order is alphabetical, so label 0 = cracked, 1 = sound
class PanelFolder(Dataset):
    def __init__(self, root, augment = False):
        self.classes = sorted(os.listdir(root))
        self.samples = [(os.path.join(root, c, f), i)
                        for i, c in enumerate(self.classes)
                        for f in sorted(os.listdir(os.path.join(root, c)))]
        # panels are already 64 x 64 greyscale; pixels become numbers from 0 to 1
        self.x = torch.stack([
            torch.from_numpy(np.array(Image.open(p).convert("L"), dtype = np.float32) / 255).unsqueeze(0)
            for p, _ in self.samples])
        self.y = torch.tensor([y for _, y in self.samples])
        self.augment = augment
    def __len__(self):
        return len(self.samples)
    def __getitem__(self, i):
        x = self.x[i]
        if self.augment:                               # random flips, only for training
            if torch.rand(1).item() < 0.5: x = torch.flip(x, dims = [2])
            if torch.rand(1).item() < 0.5: x = torch.flip(x, dims = [1])
        return x, self.y[i]

train_data = PanelFolder(folder + "/train", augment = True)
valid_data = PanelFolder(folder + "/valid")
test_data  = PanelFolder(folder + "/test")
print(train_data.classes)   # ['cracked', 'sound']
print(len(train_data), len(valid_data), len(test_data))

# ---- The network ----
torch.manual_seed(5300)
model = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size = 3, padding = 1),  nn.ReLU(), nn.MaxPool2d(2),  # 64x64 -> 32x32
    nn.Conv2d(16, 32, kernel_size = 3, padding = 1), nn.ReLU(), nn.MaxPool2d(2),  # 32x32 -> 16x16
    nn.Conv2d(32, 64, kernel_size = 3, padding = 1), nn.ReLU(), nn.MaxPool2d(2),  # 16x16 -> 8x8
    nn.Flatten(),                                                                 # 64 x 8 x 8 = 4,096 numbers
    nn.Linear(64 * 8 * 8, 64), nn.ReLU(),
    nn.Linear(64, 1)                                                              # one output
)

# ---- Data loaders ----
train_loader = DataLoader(train_data, batch_size = 64, shuffle = True)
valid_loader = DataLoader(valid_data, batch_size = 256)
test_loader  = DataLoader(test_data,  batch_size = 256)

# ---- Training ----
# 1 if cracked (label 0), 0 if sound (label 1), shaped as a column
def to_target(y):
    return (y == 0).float().unsqueeze(1)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr = 0.001, weight_decay = 0.0001)

# average loss over a whole data loader, without training
def evaluate_loss(loader):
    model.eval()
    losses = []
    with torch.no_grad():
        for xb, yb in loader:
            losses.append(loss_fn(model(xb), to_target(yb)).item())
    return np.mean(losses)

# probability of "cracked" for every panel in a data loader, plus the truth
def predict_probs(loader):
    model.eval()
    probs, labels = [], []
    with torch.no_grad():
        for xb, yb in loader:
            probs.extend(torch.sigmoid(model(xb)).flatten().tolist())
            labels.extend(yb.tolist())
    return pd.DataFrame({"prob": probs,
                         "truth": np.where(np.array(labels) == 0, "cracked", "sound")})

# share of truly cracked panels the model lets through at a threshold
def escape_rate(results, threshold = 0.5):
    return np.mean(results.loc[results["truth"] == "cracked", "prob"] <= threshold)

best_valid = float("inf"); patience = 5; bad_epochs = 0
history = []
start = time.time()
for epoch in range(1, 31):
    model.train()
    batch_losses = []
    for xb, yb in train_loader:
        optimizer.zero_grad()
        logits = model(xb)
        loss = loss_fn(logits, to_target(yb))
        loss.backward()
        optimizer.step()
        batch_losses.append(loss.item())
    valid_loss = evaluate_loss(valid_loader)
    valid_escape = escape_rate(predict_probs(valid_loader))
    history.append({"epoch": epoch, "train": np.mean(batch_losses), "valid": valid_loss})
    print(f"Epoch {epoch} train {np.mean(batch_losses):.3f} valid {valid_loss:.3f} "
          f"escape {valid_escape:.3f} seconds {time.time() - start:.0f}")
    if valid_loss < best_valid:
        best_valid = valid_loss; bad_epochs = 0
        best_weights = copy.deepcopy(model.state_dict())
    else:
        bad_epochs += 1
        if bad_epochs >= patience:
            break
model.load_state_dict(best_weights)   # go back to the best epoch
history = pd.DataFrame(history)

# ---- Escapes and false alarms on the validation panels, at 0.5 ----
valid_results = predict_probs(valid_loader)
valid_results["predicted"] = np.where(valid_results["prob"] > 0.5, "cracked", "sound")
print(pd.crosstab(valid_results["truth"], valid_results["predicted"]))
print("escape rate", escape_rate(valid_results))
print("false alarm rate", np.mean(valid_results.loc[valid_results["truth"] == "sound", "prob"] > 0.5))

# ---- The test panels, once, at the end ----
test_results = predict_probs(test_loader)
test_results["predicted"] = np.where(test_results["prob"] > 0.5, "cracked", "sound")
print(pd.crosstab(test_results["truth"], test_results["predicted"]))
