import pandas as pd
import os

# Folder where your CSVs are
folder = "/Users/judyz/Desktop/PET-4x4/build/1mm"

dfs = []

# Loop through files 15000(1).csv → 15000(20).csv
for i in range(1, 41):
    filename = f"15000({i}).csv"
    filepath = os.path.join(folder, filename)
    
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        dfs.append(df)
        print(f"Loaded {filename}")
    else:
        print(f"Missing: {filename}")

# Merge all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save merged file
output_path = os.path.join(folder, "merge.csv")
merged_df.to_csv(output_path, index=False)

print(f"\nMerged file saved as: {output_path}")
print(f"Total rows: {len(merged_df)}")