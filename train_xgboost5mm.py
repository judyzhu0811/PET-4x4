import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt
import os

filename = "/Users/judyz/Desktop/PET-4x4 copy/build/hits_per_event.csv"
data = pd.read_csv(filename)

sipm = data.loc[:, "sipm0":"sipm15"].copy()
sipm_sum = sipm.sum(axis=1)
sipm = sipm.div(sipm_sum, axis=0).fillna(0)

X = sipm.values
y = data.loc[:, ["x(mm)", "y(mm)"]].values

mask = sipm_sum > 0
X = X[mask]
y = y[mask]

print("Data loaded:", X.shape)

x_min, x_max = y[:, 0].min(), y[:, 0].max()
y_min, y_max = y[:, 1].min(), y[:, 1].max()
margin = 5.0

central_mask = (
    (y[:, 0] > x_min + margin) &
    (y[:, 0] < x_max - margin) &
    (y[:, 1] > y_min + margin) &
    (y[:, 1] < y_max - margin)
)

X = X[central_mask]
y = y[central_mask]

print("Central volume:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

params = {
    "max_depth": 5,
    "eta": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "eval_metric": "rmse"
}

dtrain_x = xgb.DMatrix(X_train, label=y_train[:, 0])
dtest_x  = xgb.DMatrix(X_test, label=y_test[:, 0])

dtrain_y = xgb.DMatrix(X_train, label=y_train[:, 1])
dtest_y  = xgb.DMatrix(X_test, label=y_test[:, 1])

num_round = 200

bst_x = xgb.train(params, dtrain_x, num_round)
bst_y = xgb.train(params, dtrain_y, num_round)

pred_x = bst_x.predict(dtest_x)
pred_y = bst_y.predict(dtest_y)

dx = pred_x - y_test[:, 0]
dy = pred_y - y_test[:, 1]
r_error = np.sqrt(dx**2 + dy**2)

def actual_fwhm(data, bins=200):
    counts, edges = np.histogram(data, bins=bins)
    half_max = counts.max() / 2.0
    above = np.where(counts >= half_max)[0]

    if len(above) < 2:
        return np.nan

    return edges[above[-1] + 1] - edges[above[0]]

fwhm_x = actual_fwhm(dx)
fwhm_y = actual_fwhm(dy)
fwhm_r = actual_fwhm(r_error)

mse_x = np.mean(dx**2)
mse_y = np.mean(dy**2)
mse_xy = np.mean(dx**2 + dy**2)

bias_x = np.mean(dx)
bias_y = np.mean(dy)

tail_2mm = np.mean(r_error > 2.0)
tail_3mm = np.mean(r_error > 3.0)

print("\n================ RESULTS ================\n")

print(f"MSE_x = {mse_x:.6f}")
print(f"MSE_y = {mse_y:.6f}")
print(f"MSE_xy = {mse_xy:.6f}")

print(f"Bias_x = {bias_x:.6f} mm")
print(f"Bias_y = {bias_y:.6f} mm")

print(f"FWHM_x = {fwhm_x:.6f} mm")
print(f"FWHM_y = {fwhm_y:.6f} mm")
print(f"FWHM_r = {fwhm_r:.6f} mm")

print(f"Tail >2mm = {tail_2mm:.6f}")
print(f"Tail >3mm = {tail_3mm:.6f}")

print("\n=========================================\n")


output_folder = "/Users/judyz/Desktop/PET-4x4 copy/build"
os.makedirs(output_folder, exist_ok=True)

bins = np.linspace(-5, 5, 100)

plt.figure(figsize=(8,5))

plt.hist(dx, bins=bins, alpha=0.6, label=f'ΔX FWHM={fwhm_x:.3f} mm')
plt.hist(dy, bins=bins, alpha=0.6, label=f'ΔY FWHM={fwhm_y:.3f} mm')

plt.xlabel("Reconstruction Error (mm)")
plt.ylabel("Counts")
plt.title("XGBoost Reconstruction Error")
plt.legend()
plt.grid(True)

plt.savefig(os.path.join(output_folder, "xgboost5mm.png"), dpi=300)

plt.figure()

plt.hist(r_error, bins=100)
plt.xlabel("Radial Error (mm)")
plt.ylabel("Counts")
plt.title(f"Radial Error (FWHM={fwhm_r:.3f} mm)")
plt.grid(True)

plt.savefig(os.path.join(output_folder, "xgboost_radial5mm.png"), dpi=300)

plt.show()