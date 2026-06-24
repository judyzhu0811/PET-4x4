import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------
# Output folder
# -------------------------
output_dir = "/Users/judyz/Desktop/PET-4x4/build/"
os.makedirs(output_dir, exist_ok=True)

# -------------------------
# Your datasets
# -------------------------
files = [
    ("3.05", "/Users/judyz/Desktop/PET-4x4/build/3.05mm/3.05mm.csv"),
    ("6.05", "/Users/judyz/Desktop/PET-4x4/build/6.05mm/6.05mm.csv"),
    ("9.05", "/Users/judyz/Desktop/PET-4x4/build/9.05mm/9.05mm.csv"),
    ("12.05", "/Users/judyz/Desktop/PET-4x4/build/12.05mm/12.05mm.csv"),
    ("15.05", "/Users/judyz/Desktop/PET-4x4/build/15.05mm/15.05mm.csv"),
]

# -------------------------
# Storage
# -------------------------
distances = []
mean_lce_list = []
cv_list = []

# -------------------------
# Compute metrics
# -------------------------
for d, file in files:

    df = pd.read_csv(file)

    mean_lce = df["LCE (%)"].mean()
    std_lce = df["LCE (%)"].std()
    cv = std_lce / mean_lce

    distances.append(float(d))
    mean_lce_list.append(mean_lce)
    cv_list.append(cv)

    print(f"{d} mm → Mean LCE = {mean_lce:.3f}, CV = {cv:.3f}")

# -------------------------
# Sort by distance
# -------------------------
sorted_data = sorted(zip(distances, mean_lce_list, cv_list))
distances, mean_lce_list, cv_list = map(list, zip(*sorted_data))

# =========================================================
# PLOT 1: Mean LCE vs Distance
# =========================================================
plt.figure(figsize=(6,4))

plt.plot(distances, mean_lce_list, marker="o")

plt.xlabel("SiPM–Anode Distance (mm)")
plt.ylabel("Mean LCE (%)")
plt.title("Light Collection Efficiency vs Distance")
plt.grid()

plt.tight_layout()

plt.savefig(os.path.join(output_dir, "mean_lce_vs_distance.png"), dpi=300)

plt.show()

# =========================================================
# PLOT 2: CV vs Distance
# =========================================================
plt.figure(figsize=(6,4))

plt.plot(distances, cv_list, marker="o", color="red")

plt.xlabel("SiPM–Anode Distance (mm)")
plt.ylabel("Uniformity (CV)")
plt.title("LCE Uniformity vs Distance")
plt.grid()

plt.tight_layout()

plt.savefig(os.path.join(output_dir, "cv_vs_distance.png"), dpi=300)

plt.show()

# =========================================================
# PLOT 3: Trade-off
# =========================================================
plt.figure(figsize=(6,5))

plt.scatter(cv_list, mean_lce_list)

for i, d in enumerate(distances):
    plt.text(cv_list[i], mean_lce_list[i], f"{d} mm")

plt.xlabel("Uniformity (CV)")
plt.ylabel("Mean LCE (%)")
plt.title("Detector Optimization Trade-off")
plt.grid()

plt.tight_layout()

plt.savefig(os.path.join(output_dir, "tradeoff.png"), dpi=300)

plt.show()