import pandas as pd
import numpy as np

filename = "/Users/judyz/Desktop/PET-4x4-copy/build/merged_15000.csv"
data = pd.read_csv(filename)

# Inputs: sipm0 to sipm15 + z(mm)
X = data.loc[:, "sipm0":"sipm15"].copy()
X["z(mm)"] = data["z(mm)"]  # add Z as an input feature
X = X.values  # convert to numpy array for XGBoost

# Outputs: x(mm) and y(mm)
y = data.loc[:, ["x(mm)", "y(mm)"]].values
mask = X.sum(axis=1) > 0  # True for rows with nonzero total
X = X[mask]
y = y[mask]

X = X / X.sum(axis=1, keepdims=True)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("First row of X:", X[0])
print("Sum of first row (should be 1.0):", X[0].sum())