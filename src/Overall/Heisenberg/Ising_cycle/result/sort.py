import pandas as pd
import re

# Function to extract "some number" from the first column
def extract_number(value):
    match = re.search(r"\[(\d+)", str(value))
    return int(match.group(1)) if match else None

# Generate expected numbers based on the given formula
expected_numbers = [3 + 9 * (i - 1) for i in range(1, 12)]  # From 3 to 96

# Load the CSV file
input_file = "result_base.csv"  # Change to your actual file name
df = pd.read_csv(input_file)

# Extract numbers from the first column
df[" Extracted_Number"] = df.iloc[:, 0].apply(extract_number)

# Create a dictionary of existing rows indexed by extracted number
existing_rows = {num: row for num, row in df.set_index(" Extracted_Number").iterrows()}

# Create a new list for the completed data
completed_data = []

# Iterate over expected numbers and fill missing rows with None
for num in expected_numbers:
    if num in existing_rows:
        ls = existing_rows[num].to_list()
        ls.append(num)
        completed_data.append(ls)  # Existing row
    else:
        completed_data.append(["None"] * len(df.columns))  # Missing row

# Create a new DataFrame
completed_df = pd.DataFrame(completed_data, columns=df.columns)

# Save the completed CSV file
output_file = "result_base.csv"
completed_df.to_csv(output_file, index=False)
