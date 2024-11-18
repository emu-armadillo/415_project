#import packages
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import gzip
'''
    to start mongodb server run in bash as admin:
        net start MongoDB

    to stop mongodb server run in bash as admin:
        net stop MongoDB

    products in original dataset: 548,552
'''

if __name__ == "__main__":

    # connect to MongoDB server
    client = MongoClient("mongodb://localhost:27017/")
    db = client.get_database("AmazonProject")
    collection = db.get_collection("ProductMetaData")

    # Check if collection exists and has data before dropping
    if collection.count_documents({}) > 0:
        collection.drop()
        print(f"Collection '{collection.name}' dropped.\n")


    # Function to parse a single product entry
    def parse_product(lines):
        product = {}
        line_iter = iter(lines)  # Create an iterator for lines

        for line in line_iter:
            line = line.strip()
            if line.startswith('Id:'):
                product['_id'] = int(line.split(':')[1].strip())  # set the product ID as the MongoDB _id
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

                # Check for discontinued product
            if 'discontinued product' in line.lower():
                return None  # Skip this product
        
        return product


    # Reading from a .gz file
    with gzip.open('../../amazon-meta.txt.gz', 'rt', encoding='utf-8') as file:
        lines = []

        for line in file:
            if line.strip() == '' and lines:  # New product starts
                try:
                    product = parse_product(lines)
                    if product:  # Only insert if product is not None
                        try:
                            collection.insert_one(product)
                        except DuplicateKeyError:
                            print(f"Duplicate product ID found: - skipping")
                except Exception:
                    print(f"Error processing product:")
                lines = []  # Reset for the next product
            else:
                lines.append(line)

    # Insert the last product if the file doesn't end with an empty line
    if lines:
        try:
            product = parse_product(lines)
            if product:  # Only insert if product is not None
                try:
                    collection.insert_one(product)
                except DuplicateKeyError:
                    print(f"Duplicate product ID found: {product['Id']} - skipping")
        except Exception as e:
            print(f"Error processing last product: {lines}\n{e}")


    # print count of total documents in the collection
    print(f'Total documents in {collection.name}: {collection.count_documents({})}\n')
    print("Data inserted into MongoDB.")
