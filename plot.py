import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/merged_15000.csv")


# Full LXe bounds
x_min, x_max = -35, 35  # mm
y_min, y_max = -35, 35  # mm
n_bins = 70  # change this freely now

# Create bins
x_bins = np.linspace(x_min, x_max, n_bins + 1)
y_bins = np.linspace(y_min, y_max, n_bins + 1)

# Histogram: weighted sum of LCE
H, _, _ = np.histogram2d(
    df["x(mm)"], df["y(mm)"],
    bins=[x_bins, y_bins], 
    weights=df["LCE (%)"]
)

# Histogram: counts
counts, _, _ = np.histogram2d(
    df["x(mm)"], df["y(mm)"],
    bins=[x_bins, y_bins]
)

# Compute average safely
avg_LCE = np.full_like(H, np.nan, dtype=float)
valid = counts > 0
avg_LCE[valid] = H[valid] / counts[valid]

# ---- IMPORTANT FIX: remove noisy bins ----
min_counts = 1   # adjust (5–20 depending on stats)
avg_LCE[counts < min_counts] = np.nan

# ---- IMPORTANT FIX: consistent color scale ----
vmin = np.nanpercentile(avg_LCE, 5)   # robust lower bound
vmax = np.nanpercentile(avg_LCE, 95)  # robust upper bound

# Plot
plt.figure(figsize=(8, 7))
mesh = plt.pcolormesh(
    x_bins, y_bins, avg_LCE.T,
    shading='auto',
    cmap='viridis',
    vmin=vmin,
    vmax=vmax
)

plt.colorbar(mesh, label="LCE (%)")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title(f"LCE Map (bins={n_bins})")

plt.tight_layout()
plt.show()

# ---- DEBUG (optional) ----
print("Min LCE:", np.nanmin(avg_LCE))
print("Max LCE:", np.nanmax(avg_LCE))
print("Mean LCE:", np.nanmean(avg_LCE))
