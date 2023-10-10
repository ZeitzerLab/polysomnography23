import pandas as pd

df = pd.read_csv("/home/x-dchawra/polysomnography_2023/csvdata/datafullnight2_SE_waso0.25_0.5_0.75_1_2_3_4_5_6_7_8_9_10.csv")

# Create a new DataFrame with desired columns

columns_to_keep = ["nsrrid"]

# Iterate through the columns and select the desired columns
for col in df.columns:
    print(col)
    if col.startswith("WASO_min") or col.startswith("StoWfreq"):
        columns_to_keep.append(col)

# Create a new DataFrame with the selected columns
new_df = df[columns_to_keep]

# Save the new DataFrame to a new CSV file
new_df.to_csv("new_data.csv", index=False)
