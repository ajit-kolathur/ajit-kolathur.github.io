import os
import pandas as pd
import json
from glob import glob
import re
import gzip

# Directory where the Excel files are stored
data_dir = "NIV_Reports"

# Lists to hold DataFrames for each report type
nationality_dfs = []
post_dfs = []

# Regular expression pattern to extract month and year from filename
pattern = re.compile(r'(\w+)_(\d{4})')

# Dictionary to map month names to month numbers
month_map = {month: index for index, month in enumerate([
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
], start=1)}

# Iterate over all Excel files in the directory
for file_path in glob(os.path.join(data_dir, "*.xlsx")):
    # Extract filename
    filename = os.path.basename(file_path)
    
    # Determine the report type based on the filename
    if "Nationality" in filename:
        report_type = "Nationality"
    elif "Post" in filename:
        report_type = "Post"
    else:
        continue  # Skip files that don't match expected patterns

    # Extract month and year from the filename
    match = pattern.search(filename)
    if match:
        month_name, year = match.groups()
        month = month_map.get(month_name.upper(), None)
        if month is None:
            print(f"Unknown month name '{month_name}' in file '{filename}'. Skipping.")
            continue
    else:
        print(f"Filename '{filename}' does not match expected pattern. Skipping.")
        continue

    # Load the Excel file into a DataFrame, skipping the first row
    df = pd.read_excel(file_path, skiprows=1)
    
    # Add 'Year' and 'Month' columns to the DataFrame
    df['Year'] = int(year)
    df['Month'] = month

    # Append the DataFrame to the appropriate list
    if report_type == "Nationality":
        nationality_dfs.append(df)
    elif report_type == "Post":
        post_dfs.append(df)

# Combine all DataFrames for each report type
combined_nationality_df = pd.concat(nationality_dfs, ignore_index=True) if nationality_dfs else pd.DataFrame()
combined_post_df = pd.concat(post_dfs, ignore_index=True) if post_dfs else pd.DataFrame()

# Set date field
# Ensure 'Month' and 'Year' are integers
combined_nationality_df['Year'] = combined_nationality_df['Year'].astype(int)
combined_nationality_df['Month'] = combined_nationality_df['Month'].astype(int)
combined_post_df['Year'] = combined_post_df['Year'].astype(int)
combined_post_df['Month'] = combined_post_df['Month'].astype(int)

# Create the Date column (using the first of the month as the day)
combined_nationality_df['Date'] = pd.to_datetime(
    combined_nationality_df[['Year', 'Month']].assign(DAY=1)
).dt.strftime('%Y-%m-%d')
combined_post_df['Date'] = pd.to_datetime(
    combined_post_df[['Year', 'Month']].assign(DAY=1)
).dt.strftime('%Y-%m-%d')



# Export combined DataFrames to JSON files
# Write compressed JSON to .json.gz file
def save_as_gzipped_json(df, filename):
    with gzip.open(filename, 'wt', encoding='utf-8') as f:
        json.dump(df.to_dict(orient="records"), f, indent=4)

# Assuming you've already created these DataFrames:
# combined_nationality_df and combined_post_df

save_as_gzipped_json(combined_nationality_df.sort_values(['Date', 'Nationality']), "combined_nationality_data.json.gz")
save_as_gzipped_json(combined_post_df.sort_values(['Date', 'Post']), "combined_post_data.json.gz")