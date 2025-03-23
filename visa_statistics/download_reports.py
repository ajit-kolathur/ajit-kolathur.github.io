import os
import requests
from datetime import datetime

# Define the base URL and output directory
BASE_URL = "https://travel.state.gov/content/dam/visas/Statistics/Non-Immigrant-Statistics/MonthlyNIVIssuances/Excel"
OUTPUT_DIR = "NIV_Reports"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define month names and corresponding fiscal months
MONTHS = [
    ("OCTOBER", 10),
    ("NOVEMBER", 11),
    ("DECEMBER", 12),
    ("JANUARY", 1),
    ("FEBRUARY", 2),
    ("MARCH", 3),
    ("APRIL", 4),
    ("MAY", 5),
    ("JUNE", 6),
    ("JULY", 7),
    ("AUGUST", 8),
    ("SEPTEMBER", 9),
]

# Get the current date
now = datetime.now()

# Calculate the starting fiscal year (assuming data is available from FY2019 onwards)
start_fiscal_year = 2023

# Define the report types
report_types = [
    "NIV Issuances by Nationality and Visa Class",
    "NIV Issuances by Post and Visa Class"
]

# Function to download a file
def download_file(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Report not found at {url} (HTTP {response.status_code})")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Iterate over each fiscal year and month
for fiscal_year in range(start_fiscal_year, now.year + 1):
    for month_name, month_number in MONTHS:
        # Determine the calendar year
        if month_number >= 10:  # OCT, NOV, DEC belong to the previous calendar year
            calendar_year = fiscal_year - 1
        else:
            calendar_year = fiscal_year

        # Skip future months
        if calendar_year == now.year and month_number > now.month:
            break

        # Iterate over each report type
        for report_type in report_types:
            # Construct the filename and URL
            filename = f"{month_name}%20{calendar_year}%20-%20{report_type}.xlsx"
            url = f"{BASE_URL}/FY{fiscal_year}/{filename}"

            # Define the local file path
            file_path = os.path.join(OUTPUT_DIR, filename.replace("%20", "_"))

            # Check if the file already exists
            if os.path.exists(file_path):
                print(f"Already exists: {file_path}")
            else:
                # Attempt to download the file
                download_file(url, file_path)