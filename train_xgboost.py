import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# -------------------------
# Load data
# -------------------------
filename = "/Users/judyz/Desktop/PET-4x4/build/1mm/merge.csv"
data = pd.read_csv(filename)

sipm = data.loc[:, "sipm0":"sipm15"].copy()
sipm_sum = sipm.sum(axis=1)
sipm = sipm.div(sipm_sum, axis=0).fillna(0)

X = sipm.values  
y = data.loc[:, ["x(mm)", "y(mm)"]].values

mask = sipm_sum > 0
X = X[mask]
y = y[mask]

print("Data loaded. X shape:", X.shape, "y shape:", y.shape)

# -------------------------
# Select central volume
# -------------------------
x_min, x_max = y[:, 0].min(), y[:, 0].max()
y_min, y_max = y[:, 1].min(), y[:, 1].max()
margin = 0  # mm

central_mask = (
    (y[:, 0] > x_min + margin) & (y[:, 0] < x_max - margin) &
    (y[:, 1] > y_min + margin) & (y[:, 1] < y_max - margin)
)

X_central = X[central_mask]
y_central = y[central_mask]

print("Central volume selected:", X_central.shape)

# -------------------------
# Split train/test
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_central, y_central, test_size=0.2, random_state=42
)

# -------------------------
# Prepare DMatrix for XGBoost
# -------------------------
dtrain_x = xgb.DMatrix(X_train, label=y_train[:, 0])
dtest_x = xgb.DMatrix(X_test, label=y_test[:, 0])
dtrain_y = xgb.DMatrix(X_train, label=y_train[:, 1])
dtest_y = xgb.DMatrix(X_test, label=y_test[:, 1])

# -------------------------
# XGBoost parameters
# -------------------------
params = {
    "max_depth": 5,
    "eta": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "eval_metric": "rmse"
}
num_round = 300

# -------------------------
# Train X model
# -------------------------
evals_x = [(dtrain_x, 'train'), (dtest_x, 'test')]
evals_result_x = {}
bst_x = xgb.train(params, dtrain_x, num_round, evals=evals_x, evals_result=evals_result_x, verbose_eval=False)

# -------------------------
# Train Y model
# -------------------------
evals_y = [(dtrain_y, 'train'), (dtest_y, 'test')]
evals_result_y = {}
bst_y = xgb.train(params, dtrain_y, num_round, evals=evals_y, evals_result=evals_result_y, verbose_eval=False)

# -------------------------
# Predict
# -------------------------
pred_x = bst_x.predict(dtest_x)
pred_y = bst_y.predict(dtest_y)

dx = pred_x - y_test[:, 0]
dy = pred_y - y_test[:, 1]

# -------------------------
# FWHM calculation
# -------------------------
def compute_fwhm(data):
    return 2.355 * np.std(data)

print("FWHM X (mm):", compute_fwhm(dx))
print("FWHM Y (mm):", compute_fwhm(dy))

# -------------------------
# Output folder
# -------------------------
output_folder = "/Users/judyz/Desktop/PET-4x4/build/1mm"
os.makedirs(output_folder, exist_ok=True)

# -------------------------
# ΔX/ΔY histogram
# -------------------------
plt.figure(figsize=(8, 5))
bins = np.linspace(-5, 5, 100)  
counts_x, _ = np.histogram(dx, bins=bins)
counts_y, _ = np.histogram(dy, bins=bins)

scale_factor = 2 / max(max(counts_x), max(counts_y))
counts_x_scaled = counts_x * scale_factor
counts_y_scaled = counts_y * scale_factor

plt.bar(bins[:-1], counts_x_scaled, width=bins[1]-bins[0], alpha=0.6, label='ΔX', align='edge')
plt.bar(bins[:-1], counts_y_scaled, width=bins[1]-bins[0], alpha=0.6, label='ΔY', align='edge')

mu_x, sigma_x = norm.fit(dx)
mu_y, sigma_y = norm.fit(dy)
x_vals = np.linspace(-5, 5, 500)

plt.plot(x_vals, norm.pdf(x_vals, mu_x, sigma_x) * len(dx) * (bins[1]-bins[0]) * scale_factor,
         '--', label=f'ΔX FWHM={2.355*sigma_x:.3f} mm')
plt.plot(x_vals, norm.pdf(x_vals, mu_y, sigma_y) * len(dy) * (bins[1]-bins[0]) * scale_factor,
         '--', label=f'ΔY FWHM={2.355*sigma_y:.3f} mm')
plt.xlabel('Difference between reconstructed and original X/Y position (mm)')
plt.ylabel('Counts')
plt.title('XGBoost ΔX/ΔY Histogram')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'xgboost.png'), dpi=300)

# -------------------------
# Loss vs Epoch plot
# -------------------------
plt.figure()
plt.plot(np.array(evals_result_x['train']['rmse'])**2, label='Train X')
plt.plot(np.array(evals_result_x['test']['rmse'])**2, label='Test X')
plt.plot(np.array(evals_result_y['train']['rmse'])**2, '--', label='Train Y')
plt.plot(np.array(evals_result_y['test']['rmse'])**2, '--', label='Test Y')

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss vs Epoch (XGBoost)")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, "loss_epoch_xgboost.png"), dpi=300)
plt.show()