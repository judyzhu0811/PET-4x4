import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("build/hits_per_event.csv")
sipm_counts = df.iloc[:, 1:17].values
df["total_pe"] = df.iloc[:,1:17].sum(axis=1)
ratio = df["total_pe"]/2000

plt.figure()
plt.hist(ratio)
plt.savefig("hist.png")
print(np.mean(ratio))