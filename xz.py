import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/hits_per_eventxz.csv")

# Full LXe bounds
x_min, x_max = -35, 35  # mm
z_min_csv, z_max_csv = df["z(mm)"].min(), df["z(mm)"].max()

# Ensure increasing bins for histogram2d
if z_min_csv < z_max_csv:
    z_min, z_max = z_min_csv, z_max_csv
    flip_z_axis = False
else:
    z_min, z_max = z_max_csv, z_min_csv
    flip_z_axis = True  # we'll flip axis in plot

n_bins = 50  # adjustable

# Create bins
x_bins = np.linspace(x_min, x_max, n_bins + 1)
z_bins = np.linspace(z_min, z_max, n_bins + 1)

# Weighted histogram (sum of LCE)
H, _, _ = np.histogram2d(
    df["x(mm)"], df["z(mm)"],
    bins=[x_bins, z_bins],
    weights=df["LCE (%)"]
)

# Histogram counts
counts, _, _ = np.histogram2d(
    df["x(mm)"], df["z(mm)"],
    bins=[x_bins, z_bins]
)

# Compute average LCE safely
avg_LCE = np.full_like(H, np.nan, dtype=float)
valid = counts > 0
avg_LCE[valid] = H[valid] / counts[valid]

# Remove noisy bins
min_counts = 1  # adjust depending on statistics
avg_LCE[counts < min_counts] = np.nan

# Robust color scale
if np.any(~np.isnan(avg_LCE)):
    vmin = np.nanpercentile(avg_LCE, 5)
    vmax = np.nanpercentile(avg_LCE, 95)
else:
    vmin, vmax = 0, 100  # fallback if all bins empty

# Plot
plt.figure(figsize=(8, 7))
mesh = plt.pcolormesh(
    x_bins, z_bins, avg_LCE.T,
    shading='auto',
    cmap='viridis',
    vmin=vmin,
    vmax=vmax
)

plt.colorbar(mesh, label="LCE (%)")
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.title(f"LCE Map (bins={n_bins})")

# Flip Z-axis if original data decreasing
if flip_z_axis:
    plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# Debug info
print("Min LCE:", np.nanmin(avg_LCE))
print("Max LCE:", np.nanmax(avg_LCE))
print("Mean LCE:", np.nanmean(avg_LCE))