import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os

csv_path = "/Users/judyz/Desktop/PET-4x4/build/17.05mm/17.05mm.csv"

df = pd.read_csv(csv_path)

y_center = 0.0
y_width = 1.0

slice_df = df[
    (df["y(mm)"] >= y_center - y_width) &
    (df["y(mm)"] <= y_center + y_width)
]

mean_lce = slice_df["LCE (%)"].mean()
std_lce = slice_df["LCE (%)"].std()
cv = std_lce / mean_lce

print("Mean LCE (slice):", mean_lce)
print("Uniformity (CV):", cv)

x_min, x_max = -35, 35
z_min, z_max = -25, 25

n_bins = 40

x_bins = np.linspace(x_min, x_max, n_bins + 1)
z_bins = np.linspace(z_min, z_max, n_bins + 1)

H, _, _ = np.histogram2d(
    slice_df["x(mm)"],
    slice_df["z(mm)"],
    bins=[x_bins, z_bins],
    weights=slice_df["LCE (%)"]
)

counts, _, _ = np.histogram2d(
    slice_df["x(mm)"],
    slice_df["z(mm)"],
    bins=[x_bins, z_bins]
)

avg_LCE = np.full_like(H, np.nan, dtype=float)
valid = counts > 0
avg_LCE[valid] = H[valid] / counts[valid]

mask = np.isfinite(avg_LCE)

data_filled = np.where(mask, avg_LCE, 0)

sigma = 1.2

smoothed_data = gaussian_filter(data_filled, sigma=sigma)
smoothed_mask = gaussian_filter(mask.astype(float), sigma=sigma)

avg_LCE_smooth = np.divide(
    smoothed_data,
    smoothed_mask,
    out=np.full_like(smoothed_data, np.nan),
    where=smoothed_mask > 0
)

output_dir = os.path.dirname(csv_path)

output_path = os.path.join(
    output_dir,
    f"xz_lce.png"
)

plt.figure(figsize=(7,6))

plt.pcolormesh(
    x_bins,
    z_bins,
    avg_LCE_smooth.T,
    shading='auto',
    cmap='viridis'
)

plt.colorbar(label="LCE (%)")

plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")

plt.title(
    f"XZ LCE Map (fixed Y = {y_center} mm)\n"
    f"Uniformity (CV) = {cv:.3f}"
)

plt.figtext(
    0.5, 0.01,
    f"Mean LCE = {mean_lce:.2f}%",
    ha="center",
    fontsize=12,
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print("Saved figure to:", output_path)