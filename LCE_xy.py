import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/3.05mm/3.05mm.csv")

x_min, x_max = -35, 35
y_min, y_max = -35, 35

# central z slice
z_center = 19.85   
z_width = 0.5

slice_df = df[
    (df["z(mm)"] >= z_center - z_width) &
    (df["z(mm)"] <= z_center + z_width)
]
mean_lce = slice_df["LCE (%)"].mean()
std_lce = slice_df["LCE (%)"].std()

cv = std_lce / mean_lce

print("Mean LCE (slice):", mean_lce)
print("Uniformity (CV):", cv)

n_bins = 80
x_bins = np.linspace(x_min, x_max, n_bins + 1)
y_bins = np.linspace(y_min, y_max, n_bins + 1)

H, _, _ = np.histogram2d(
    slice_df["x(mm)"],
    slice_df["y(mm)"],
    bins=[x_bins, y_bins],
    weights=slice_df["LCE (%)"]
)

counts, _, _ = np.histogram2d(
    slice_df["x(mm)"],
    slice_df["y(mm)"],
    bins=[x_bins, y_bins]
)

avg_LCE = np.full_like(H, np.nan, dtype=float)
valid = counts > 0
avg_LCE[valid] = H[valid] / counts[valid]
from scipy.ndimage import gaussian_filter

mask = np.isfinite(avg_LCE)

data_filled = np.where(mask, avg_LCE, 0)

smoothed_data = gaussian_filter(data_filled, sigma=1)
smoothed_mask = gaussian_filter(mask.astype(float), sigma=1)

avg_LCE = np.divide(
    smoothed_data,
    smoothed_mask,
    out=np.full_like(smoothed_data, np.nan),
    where=smoothed_mask > 0
)

plt.figure(figsize=(7,6))

plt.pcolormesh(
    x_bins, y_bins, avg_LCE.T,
    shading='auto',
    cmap='viridis'
)
mean_lce = slice_df["LCE (%)"].mean()

plt.text(
    0.05, 0.95,
    f"Mean LCE = {mean_lce:.2f}%",
    transform=plt.gca().transAxes,
    fontsize=12,
    color="white",
    verticalalignment="top",
    bbox=dict(facecolor="black", alpha=0.5, edgecolor="none")
)
plt.colorbar(label="LCE (%)")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("XY LCE Map (center Z slice)")
plt.title(
    f"XY LCE Map (center Z slice)\nUniformity (CV) = {cv:.3f}"
)

plt.tight_layout()
output_path = "/Users/judyz/Desktop/PET-4x4/build/3.05mm/anodewires.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()