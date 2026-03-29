import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

filename = "/Users/judyz/Desktop/PET-4x4/build/merged_15000.csv"
data = pd.read_csv(filename)
sipm = data.loc[:, "sipm0":"sipm15"].copy()

sipm_sum = sipm.sum(axis=1)
sipm = sipm.div(sipm_sum, axis=0).fillna(0)

X = sipm.values
y_true = data.loc[:, ["x(mm)", "y(mm)"]].values

mask = sipm_sum > 0
X = X[mask]
y_true = y_true[mask]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_true, test_size=0.2, random_state=42
)
model = MLPRegressor(
    hidden_layer_sizes=(128, 128),
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42
)

print("Training MLP...")
model.fit(X_train, y_train)

pred = model.predict(X)
pred_x = pred[:, 0]
pred_y = pred[:, 1]
dx = pred_x - y_true[:, 0]
dy = pred_y - y_true[:, 1]

error = np.sqrt(dx**2 + dy**2)

x = y_true[:, 0]
y = y_true[:, 1]

bins = 75

heatmap, xedges, yedges = np.histogram2d(
    x, y, bins=bins, weights=error
)

counts, _, _ = np.histogram2d(x, y, bins=bins)

avg_error = np.divide(
    heatmap, counts,
    out=np.zeros_like(heatmap),
    where=counts > 0
)

output_folder = "/Users/judyz/Desktop/PET-4x4/plots"
os.makedirs(output_folder, exist_ok=True)

plt.figure(figsize=(6, 5))

extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.imshow(
    avg_error.T,
    origin='lower',
    extent=extent,
    cmap='viridis',
    aspect='auto'
)

cbar = plt.colorbar()
cbar.set_label("Distance between Original and Reconstructed Point (mm)")

plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("Accuracy of MLP")

plt.grid(False)

plt.savefig(os.path.join(output_folder, "accuracy_mlp.png"), dpi=300)
plt.show()