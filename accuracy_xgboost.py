import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor

filename = "/Users/judyz/Desktop/PET-4x4/build/1mm/merge.csv"
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
xgb_base = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror',
    random_state=42,
    n_jobs=-1
)

model = MultiOutputRegressor(xgb_base)

print("Training XGBoost...")
model.fit(X_train, y_train)

pred = model.predict(X)

dx = pred[:, 0] - y_true[:, 0]
dy = pred[:, 1] - y_true[:, 1]

error = np.sqrt(dx**2 + dy**2)

x = y_true[:, 0]
y = y_true[:, 1]
bins = 80

heatmap, xedges, yedges = np.histogram2d(
    x, y, bins=bins, weights=error
)

counts, _, _ = np.histogram2d(x, y, bins=bins)

avg_error = np.divide(
    heatmap, counts,
    out=np.zeros_like(heatmap),
    where=counts > 0
)

extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

output_folder = "/Users/judyz/Desktop/PET-4x4/build/1mm"
os.makedirs(output_folder, exist_ok=True)

plt.figure(figsize=(6, 5))

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
plt.title("Accuracy of XGBoost")

plt.grid(False)

plt.savefig(os.path.join(output_folder, "accuracy_xgboost.png"), dpi=300)
plt.show()