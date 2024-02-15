import pandas as pd
import numpy as np
import os
from nixtlats import TimeGPT

timegpt = TimeGPT(token = 'FGhvofD8JCo3kvfrY6XdCutbRnla7ZKiusXOu8mZBA6ZyPP9XvtxBb7ISNBrw3gJneb0scTwVBoCx0al0zdGucBWPOEmB0p3vObfH9iLieiGU5OmyTIpcs1ommKHxfWfdstmvf9rEI8ZfxI38DI96TK5z3ncflx9DfQydJTDzJ15xpkgOe1ET1pM5SocRvXeztO1VAl9WoKiTM00DTbmSJSnVVe5CSe4SuUt3wNXav27c6xAd82Akuhh52te7SNU')
timegpt.validate_token()


output_dir = "calculated_rows"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "calculated_rows.csv")

# TODO: Find and replace total with gradient
# Use EURUSD csv not sample dataframe
# Save as csv

# Define a function to calculate the sum of the "value" column in a DataFrame
def calculate_total(df):
    # This needs to pass sub df to TimeGpt then find slope of
    # timegpt_fcst_df, time_col='timestamp', target_col='TimeGPT'

    timegpt_fcst_df = timegpt.forecast(df=df, h=5, freq='D', time_col='timestamp', target_col='value')
    # TODO
    x = np.arange(len(timegpt_fcst_df))
    y = timegpt_fcst_df['TimeGPT']
    slope, _ = np.polyfit(x, y, 1)  # Fit a first-degree polynomial (line) to the data
    return slope, timegpt_fcst_df
    # return df['value'].sum()

# Create a sample DataFrame
# data = {
#     'timestamp': pd.date_range(start='2024-01-01', periods=5500),
#     'value': range(0, 5500*3, 3)  # Increasing by 3 for each row
# }
# df = pd.DataFrame(data)

df = pd.read_csv('interpolated_data.csv')

# Initialize the "total" column with zeros
df['slope'] = 0

# Iterate through the DataFrame starting from row 400
for i in range(400, len(df)):
    # Create a new DataFrame containing the previous 399 rows plus the current row
    sub_df = df.iloc[i-5:i+1]

#     print("First row in the DataFrame:", sub_df.iloc[0])
#     print("Last row in the DataFrame:", sub_df.iloc[-1])

    # Calculate the sum of the "value" column using the function
    slope, latest_values = calculate_total(sub_df)

    # Store the total in a new column called "total" in the original DataFrame
    df.loc[i, 'slope'] = slope

    print(latest_values.iloc[1]['TimeGPT'])

    df.loc[i, '1pred'] = latest_values.iloc[0]['TimeGPT']
    df.loc[i, '2pred'] = latest_values.iloc[1]['TimeGPT']
    df.loc[i, '3pred'] = latest_values.iloc[2]['TimeGPT']
    df.loc[i, '4pred'] = latest_values.iloc[3]['TimeGPT']
    df.loc[i, '5pred'] = latest_values.iloc[4]['TimeGPT']

    print(df.iloc[i])
    print("row: ", i)

    # Save the current row to the CSV file (append mode)
    if i == 400:
        df.iloc[i:i+1].to_csv(csv_path, index=False)
    else:
        df.iloc[i:i+1].to_csv(csv_path, mode='a', header=False, index=False)

# Set pandas display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df)  # Check the first few rows of the DataFrame with the "total" column added

# Reset pandas display options to default
pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')