import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/15mm/15mm.csv")
x_min, x_max = -35, 35  # mm
y_min, y_max = -35, 35  
n_bins = 45 
x_bins = np.linspace(x_min, x_max, n_bins + 1)
y_bins = np.linspace(y_min, y_max, n_bins + 1)
H, _, _ = np.histogram2d(
    df["x(mm)"], df["y(mm)"],
    bins=[x_bins, y_bins], 
    weights=df["LCE (%)"]
)
counts, _, _ = np.histogram2d(
    df["x(mm)"], df["y(mm)"],
    bins=[x_bins, y_bins]
)
avg_LCE = np.full_like(H, np.nan, dtype=float)
valid = counts > 0
avg_LCE[valid] = H[valid] / counts[valid]
min_counts = 1   
avg_LCE[counts < min_counts] = np.nan
vmin = np.nanpercentile(avg_LCE, 5)   
vmax = np.nanpercentile(avg_LCE, 95)  
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
output_path = "/Users/judyz/Desktop/PET-4x4/build/15mm/xy_lce.png"
plt.savefig(output_path, dpi=300)
plt.show()

print("Min LCE:", np.nanmin(avg_LCE))
print("Max LCE:", np.nanmax(avg_LCE))
print("Mean LCE:", np.nanmean(avg_LCE))
