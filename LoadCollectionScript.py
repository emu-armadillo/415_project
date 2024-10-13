#import packages
from pymongo import MongoClient
import json
'''
    to start mongodb server run in bash as admin:
        net start MongoDB

    to stop mongodb server run in bash as admin:
        net stop MongoDB
'''


# connect to MongoDB server
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("AmazonProject")
collection = db.get_collection("ProductMetaData")

# Drop the collection if it exists
collection.drop()


# Function to parse a single product entry
def parse_product(lines):
    product = {}
    line_iter = iter(lines)  # Create an iterator for lines

    for line in line_iter:
        line = line.strip()
        if line.startswith('Id:'):
            product['Id'] = int(line.split(':')[1].strip())
        elif line.startswith('ASIN:'):
            product['ASIN'] = line.split(':')[1].strip()
        elif line.startswith('title:'):
            product['title'] = line.split(':', 1)[1].strip()
        elif line.startswith('group:'):
            product['group'] = line.split(':')[1].strip()
        elif line.startswith('salesrank:'):
            product['salesrank'] = int(line.split(':')[1].strip())
        elif line.startswith('similar:'):
            similar_items = line.split()
            product['similar'] = {
                'total': int(similar_items[1]),  # Get the total number of similar items
                'items': [similar_items[2:]]        # Get the list of similar items
            }
        elif line.startswith('categories:'):
            category_info = line.split()  # Split the line to get the total number
            product['categories'] = {
                'total': int(category_info[1]),   # Get the total number of categories
                'details': []                    # Initialize list for category details
            }
            # If there are categories, collect the corresponding lines
            if product['categories'].get('total', 0) > 0:
                # Loop over the number of categories
                for i in range(product['categories']['total']):
                    category_line = next(line_iter).strip()
                    product['categories']['details'].append(category_line)

        elif line.startswith('|'):
            product['categories'].append(line.strip())
        elif line.startswith('reviews:'):
            # Reviews header looks like "reviews: total: X downloaded: X avg rating: X"
            review_info = line.split()
            product['reviews'] = {
                'total': int(review_info[2]),          # 'total: X'
                'downloaded': int(review_info[4]),     # 'downloaded: X'
                'avg_rating': float(review_info[7]),   # 'avg rating: X'
                'details': []                          # Initialize list for review details
            }
            # If there are reviews, collect the corresponding lines
            if product['reviews'].get('total', 0) > 0:
                # Loop over the number of reviews
                for j in range(product['reviews']['total']):
                    review_line = next(line_iter).strip()
                    product['reviews']['details'].append(review_line)
    
    return product



# Read the text file and parse the data
with open('sample.txt', 'r') as file:
    lines = []
    for line in file:
        if line.strip() == '' and lines:  # New product starts
            product = parse_product(lines)
            collection.insert_one(product)
            # print(f'{product}\n')           # for debugging
            lines = []  # Reset for next product
        else:
            lines.append(line)

# Insert the last product if file doesn't end with an empty line
if lines:
    product = parse_product(lines)
    collection.insert_one(product)
    # print(f'{product}\n')            # for debugging

# print count of total documents in the collection
print(f'Total documents in {collection.name}: {collection.count_documents({})}\n')
print("Data inserted into MongoDB.")