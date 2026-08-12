import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    "/Users/judyz/Desktop/PET-4x4/build/3.05mm/3.05mm.csv"
)
y_center = 0.0      # change this
y_width = 2.0       # thickness of slice (mm)

df_slice = df[
    (df["y(mm)"] >= y_center - y_width/2) &
    (df["y(mm)"] <  y_center + y_width/2)
]
# Z bins (same as before)
n_z_bins = 40
z_bins = np.linspace(-35, 35, n_z_bins + 1)

z_centers = []
mean_lce = []
std_lce = []

# Loop over Z slices 
for i in range(len(z_bins) - 1):

    z_low = z_bins[i]
    z_high = z_bins[i + 1]

    slice_df = df_slice[
        (df_slice["z(mm)"] >= z_low) &
        (df_slice["z(mm)"] < z_high)
    ]

    if len(slice_df) == 0:
        continue

    z_centers.append(0.5 * (z_low + z_high))

    mean_lce.append(slice_df["LCE (%)"].mean())
    std_lce.append(slice_df["LCE (%)"].std())

z_centers = np.array(z_centers)
mean_lce = np.array(mean_lce)
std_lce = np.array(std_lce)

# Plot X–Z slice 
plt.figure(figsize=(8,6))

plt.plot(z_centers, mean_lce, marker='o')

plt.fill_between(
    z_centers,
    mean_lce - std_lce,
    mean_lce + std_lce,
    alpha=0.3
)

plt.xlabel("Z Position (mm)")
plt.ylabel("Mean LCE (%)")
plt.title(f"LCE vs Z at Y = {y_center} ± {y_width/2} mm")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "/Users/judyz/Desktop/PET-4x4/build/3.05mm/lce_vs_z_fixed_y.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
print("Overall Mean LCE:", np.mean(mean_lce))
print("Depth Uniformity (CV):", np.std(mean_lce) / np.mean(mean_lce))