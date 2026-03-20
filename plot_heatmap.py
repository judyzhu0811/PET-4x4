"""
#importing
import csv
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import keras
import pandas as pd
#getting X data
#file = open('/content/drive/MyDrive/output_nt_Hits_1_layer_5mm.csv')
file = open('/Users/judyz/Desktop/PET-4x4 copy/build/hits_per_event.csv')
csvreader = csv.reader(file)
#first row isn't needed
line_count = 0;
original_X = []
for row in csvreader:
  if line_count >= 1:
    original_X.append([int(i) for i in row])
  line_count += 1


#getting Y data
original_y = []
for i in range(-122, 1):
  for j in range(-122, 1):
    original_y.append([i*0.2, j*0.2])

#reconstructing
num_X = np.array(original_X).reshape(123,123,9)
num_y = np.array(original_y).reshape(123,123,2)
bottom_right_X = []
bottom_right_y = []
for i in range(-122, 0):
  for j in range(-122, 1):
    tmp_X = copy.deepcopy(num_X[i+122][j+122])
    tmp_y = copy.deepcopy(num_y[i+122][j+122])
    #mirroring
    tmp_y[0] = -tmp_y[0]
    for k in range(3):
      tmp_X[3*k], tmp_X[3*k+2] = tmp_X[3*k+2], tmp_X[3*k]
    bottom_right_X.append(tmp_X)
    bottom_right_y.append(tmp_y)

bottom_right_X = np.array(bottom_right_X).reshape(122,123,9)
bottom_right_y = np.array(bottom_right_y).reshape(122,123,2)

top_left_X = []
top_left_y = []
for i in range(-122, 1):
  for j in range(-122, 0):
    tmp_X = copy.deepcopy(num_X[i+122][j+122])
    tmp_y = copy.deepcopy(num_y[i+122][j+122])
    #mirroring
    tmp_y[1] = -tmp_y[1]
    for k in range(3):
      tmp_X[k], tmp_X[k+3*2] = tmp_X[k+3*2], tmp_X[k]
    top_left_X.append(tmp_X)
    top_left_y.append(tmp_y)

top_left_X = np.array(top_left_X).reshape(123,122,9)
top_left_y = np.array(top_left_y).reshape(123,122,2)

top_right_X = []
top_right_y = []
for i in range(-122, 0):
  for j in range(-122, 0):
    tmp_X = copy.deepcopy(top_left_X[i+122][j+122])
    tmp_y = copy.deepcopy(top_left_y[i+122][j+122])
    #mirroring
    tmp_y[0] = -tmp_y[0]
    for k in range(3):
      tmp_X[3*k], tmp_X[3*k+2] = tmp_X[3*k+2], tmp_X[3*k]
    top_right_X.append(tmp_X)
    top_right_y.append(tmp_y)

top_right_X = np.array(top_right_X).reshape(122,122,9)
top_right_y = np.array(top_right_y).reshape(122,122,2)

#converting to numpy array
X = np.concatenate((num_X.reshape(15129, 9), bottom_right_X.reshape(15006, 9), top_left_X.reshape(15006, 9), top_right_X.reshape(14884, 9)))
y = np.concatenate((num_y.reshape(15129, 2), bottom_right_y.reshape(15006, 2), top_left_y.reshape(15006, 2), top_right_y.reshape(14884, 2)))

xaxis = np.linspace(-24.4, 24.4, 245)
yaxis = np.linspace(-24.4, 24.4, 245)
zaxis = np.zeros((245, 245))

for i in range(len(X)):
    zaxis[122+round(y[i][0]*5)][122-round(y[i][1]*5)] = np.sum(X[i]) / 250000 * 100

plt.figure(figsize=(8, 6))
plt.pcolormesh(xaxis, yaxis, zaxis, shading='auto', cmap='viridis')
plt.colorbar(label='Efficiency (%)')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title('Light Efficiency of PET cell')
plt.savefig("light_efficiency_1mm.png")

# ===================== NEW CODE: SIMULATION CONSISTENCY CHECK =====================

import pandas as pd
import matplotlib.pyplot as plt

# Load CSV from Geant4 output
df = pd.read_csv("/Users/judyz/Desktop/PET-4x4 copy/build/hits_per_event.csv")
print(df.head())  # quick check of columns

# ---- 1. Check uniformity of emission positions ----
fig, axes = plt.subplots(1, 3, figsize=(15,4))
axes[0].hist(df["x(mm)"], bins=50, color='C0')
axes[0].set_title("X position distribution")
axes[0].set_xlabel("X (mm)")
axes[0].set_ylabel("Counts")

axes[1].hist(df["y(mm)"], bins=50, color='C1')
axes[1].set_title("Y position distribution")
axes[1].set_xlabel("Y (mm)")

axes[2].hist(df["z(mm)"], bins=50, color='C2')
axes[2].set_title("Z position distribution")
axes[2].set_xlabel("Z (mm)")

plt.tight_layout()
plt.show()

# ---- 2. 2D position distribution (X vs Y) ----
plt.figure(figsize=(6,5))
plt.hist2d(df["x(mm)"], df["y(mm)"], bins=50, cmap='viridis')
plt.colorbar(label="Event count")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("2D Emission Position Distribution")
plt.show()

# ---- 3. LCE distribution ----
plt.figure(figsize=(6,4))
plt.hist(df["LCE (%)"], bins=50, color='orange')
plt.xlabel("LCE (%)")
plt.ylabel("Counts")
plt.title("Light Collection Efficiency Distribution")
# Overlay cathode/anode wires (example positions)
# Adjust the coordinates to match your detector geometry in mm
cathode_x = np.linspace(-35, 35, 11)  # 11 wires along X
cathode_y = np.linspace(-35, 35, 11)  # 11 wires along Y
for x in cathode_x:
    plt.axvline(x, color='red', linestyle='--', alpha=0.5)
for y in cathode_y:
    plt.axhline(y, color='red', linestyle='--', alpha=0.5)

anode_x = np.linspace(-34, 34, 68)  # 68 top wires along X
anode_y = np.linspace(-34, 34, 68)  # 68 top wires along Y
for x in anode_x[::5]:  # maybe just every 5th wire to avoid clutter
    plt.axvline(x, color='blue', linestyle=':', alpha=0.5)
for y in anode_y[::5]:
    plt.axhline(y, color='blue', linestyle=':', alpha=0.5)

plt.show()

# ---- 4. LCE vs position (X, Y) ----
plt.figure(figsize=(6,5))
plt.scatter(df["x(mm)"], df["y(mm)"], c=df["LCE (%)"], cmap="viridis", s=10)
plt.colorbar(label="LCE (%)")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("LCE vs Emission Position")
plt.show()

# ---- 5. SiPM hit distribution ----
sipm_columns = [f"sipm{i}" for i in range(16)]
df[sipm_columns].hist(bins=50, figsize=(12,6))
plt.suptitle("SiPM Hit Distributions")
plt.show()
"""

"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/hits_per_event.csv")

# Full LXe bounds from construction.cc
x_min, x_max = -35, 35  # mm
y_min, y_max = -35, 35  # mm
n_bins = 75  # grid resolution

# Create bins
x_bins = np.linspace(x_min, x_max, n_bins+1)
y_bins = np.linspace(y_min, y_max, n_bins+1)

# Use histogram2d to sum LCE per bin and count events
H, _, _ = np.histogram2d(df["x(mm)"], df["y(mm)"], bins=[x_bins, y_bins], weights=df["LCE (%)"])
counts, _, _ = np.histogram2d(df["x(mm)"], df["y(mm)"], bins=[x_bins, y_bins])

# Average LCE per bin
avg_LCE = np.divide(H, counts, out=np.zeros_like(H), where=counts>0)

# Plot heatmap
plt.figure(figsize=(8,7))
plt.pcolormesh(x_bins, y_bins, avg_LCE.T, shading='auto', cmap='viridis')
plt.colorbar(label="LCE (%)")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("Light Collection Efficiency - Full LXe Region")
plt.show()
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("/Users/judyz/Desktop/PET-4x4/build/40mm (50,000).csv")

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
