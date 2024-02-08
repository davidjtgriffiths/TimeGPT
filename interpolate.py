import pandas as pd

# Read CSV file into a DataFrame
df = pd.read_csv("D1.csv")

# Convert 'date' column to datetime type
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set 'date' column as index
df.set_index('timestamp', inplace=True)

# Interpolate missing values using the 'pad' method to fill forward
df_interpolated = df.interpolate(method='pad')

# Get complete date range
complete_date_range = pd.date_range(start=df_interpolated.index.min(), end=df_interpolated.index.max())

# Create DataFrame with complete date range
df_complete = pd.DataFrame(index=complete_date_range)

# Merge with interpolated DataFrame to add missing rows
df_complete = df_complete.merge(df_interpolated, how='left', left_index=True, right_index=True)

# Interpolate missing values again to ensure all missing days are filled
df_complete['value'] = df_complete['value'].interpolate(method='pad')

# Reset index
df_complete.reset_index(inplace=True)

# Rename index column to 'date'
df_complete.rename(columns={'index': 'timestamp'}, inplace=True)

# Write updated DataFrame to a new CSV file
df_complete.to_csv("interpolated_data.csv", index=False)