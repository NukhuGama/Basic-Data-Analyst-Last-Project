import pandas as pd

# Load the datasets
df_day = pd.read_csv('Bike Sharing Dataset/day.csv')
df_hour = pd.read_csv('Bike Sharing Dataset/hour.csv')

# Add missing 'hr' column to df_day (if not already present)
df_day['hr'] = pd.NA

# Concatenate the datasets vertically (along rows)
df_combined = pd.concat([df_day, df_hour], ignore_index=True)

# Get the column order
cols = df_combined.columns.tolist()

# Move 'hr' column to index 5 (6th column)
# First, remove 'hr' from the column list
cols.remove('hr')
# Then, insert 'hr' at the 6th position (index 5)
cols.insert(5, 'hr')

# Reorder the columns of df_combined
df_combined = df_combined[cols]

# Optionally, save the combined dataset to a new CSV
df_combined.to_csv('combined_dataset_dayhour.csv', index=False)

# Display the combined dataset
print(df_combined)


# # Load the datasets
# df_day = pd.read_csv('Bike Sharing Dataset/day.csv')
# df_hour = pd.read_csv('Bike Sharing Dataset/hour.csv')

# df_day['hr'] = pd.NA

# # Concatenate the datasets vertically (along rows)
# df_combined = pd.concat([df_day, df_hour], ignore_index=True)

# # Optionally, save the combined dataset to a new CSV
# df_combined.to_csv('combined_dataset_dayhour.csv', index=False)

# # Display the combined dataset
# print(df_combined)





