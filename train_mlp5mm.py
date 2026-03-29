import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

filename = "/Users/judyz/Desktop/PET-4x4/build/merged_15000.csv"
data = pd.read_csv(filename)

sipm = data.loc[:, "sipm0":"sipm15"].copy()

sipm_sum = sipm.sum(axis=1)
sipm = sipm.div(sipm_sum, axis=0).fillna(0)

X = sipm.values

# Outputs
y = data.loc[:, ["x(mm)", "y(mm)"]].values
mask = sipm_sum > 0
X = X[mask]
y = y[mask]

print("Data loaded:", X.shape)

x_min, x_max = y[:, 0].min(), y[:, 0].max()
y_min, y_max = y[:, 1].min(), y[:, 1].max()
margin = 5

central_mask = (
    (y[:, 0] > x_min + margin) & (y[:, 0] < x_max - margin) &
    (y[:, 1] > y_min + margin) & (y[:, 1] < y_max - margin)
)

X = X[central_mask]
y = y[central_mask]

print("Central volume:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
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
pred = model.predict(X_test)

dx = pred[:, 0] - y_test[:, 0]
dy = pred[:, 1] - y_test[:, 1]

def compute_fwhm(data):
    return 2.355 * np.std(data)

print("FWHM X:", compute_fwhm(dx))
print("FWHM Y:", compute_fwhm(dy))
output_folder = "/Users/judyz/Desktop/PET-4x4/plots"
os.makedirs(output_folder, exist_ok=True)

bins = np.linspace(-5, 5, 100)

counts_dx, _ = np.histogram(dx, bins=bins)
counts_dy, _ = np.histogram(dy, bins=bins)

scale_factor = 2 / max(max(counts_dx), max(counts_dy))
counts_dx_scaled = counts_dx * scale_factor
counts_dy_scaled = counts_dy * scale_factor

plt.figure(figsize=(8,5))
plt.bar(bins[:-1], counts_dx_scaled, width=bins[1]-bins[0], alpha=0.6, label='ΔX', align='edge')
plt.bar(bins[:-1], counts_dy_scaled, width=bins[1]-bins[0], alpha=0.6, label='ΔY', align='edge')

mu_dx, sigma_dx = norm.fit(dx)
mu_dy, sigma_dy = norm.fit(dy)
x_vals = np.linspace(-5, 5, 500)

plt.plot(x_vals, norm.pdf(x_vals, mu_dx, sigma_dx) * len(dx) * (bins[1]-bins[0]) * scale_factor,
         '--', label=f'ΔX FWHM={2.355*sigma_dx:.3f} mm')
plt.plot(x_vals, norm.pdf(x_vals, mu_dy, sigma_dy) * len(dy) * (bins[1]-bins[0]) * scale_factor,
         '--', label=f'ΔY FWHM={2.355*sigma_dy:.3f} mm')

plt.xlabel('Difference between Reconstructed and Original X/Y Position (mm)')
plt.ylabel('Counts')
plt.title('MLP 5mm')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, "mlp_5mm.png"), dpi=300)
plt.show()