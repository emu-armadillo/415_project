# python script for cleaning and processing data from amazon-meta.txt file
import pandas as pd

# Step 1: Read the Data
file_path = 'sample.txt'
data = []

# Read the file line by line
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Split the line by tabs, assuming the file is tab-separated
        fields = line.strip().split('\t')
        data.append(fields)

# Step 2: Create a DataFrame
# Assuming the first row contains headers; adjust accordingly
headers = data[0]  # Replace this with your actual header row if different
df = pd.DataFrame(data[1:], columns=headers)

# Step 3: Clean the Data
# Example cleaning steps:
# - Convert appropriate columns to numeric types
# - Remove rows with missing values
# - Drop duplicates

# Example: convert a column to numeric (replace 'sales_rank' with actual column name)
df['sales_rank'] = pd.to_numeric(df['sales_rank'], errors='coerce')

# Remove rows with missing sales rank
df.dropna(subset=['sales_rank'], inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Step 4: Store the Cleaned Data
# Example: Save the cleaned data to a new CSV file
cleaned_file_path = 'cleaned_amazon_meta.csv'
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned and saved to {cleaned_file_path}")

import pandas as pd

# Load the dataset
df = pd.read_csv('books_dataset.csv')  # Change this to your actual file path

# Display initial data
print("Initial data:")
print(df.head())

# Cleaning process
# Assuming 'votes' is the column containing user ratings

# 1. Remove rows where 'votes' is NaN or not a number
df = df[pd.to_numeric(df['votes'], errors='coerce').notnull()]

# 2. Convert 'votes' to integer type (if they are whole numbers)
df['votes'] = df['votes'].astype(int)

# 3. Remove duplicates if any (optional)
df = df.drop_duplicates()

# 4. Remove negative ratings (if applicable)
df = df[df['votes'] >= 0]

# Display cleaned data
print("Cleaned data:")
print(df.head())

# Save the cleaned dataset to a new .txt file
df.to_csv('cleaned_books_dataset.txt', index=False, sep='\t')  # Save as tab-separated text file
