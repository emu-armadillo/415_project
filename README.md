# Amazon Co-Purchasing Analysis Project

## Overview
This project analyzes Amazon's co-purchasing patterns and product metadata using big data technologies. The dataset contains information about 548,552 different products including books, music CDs, DVDs, and VHS tapes, along with their reviews and co-purchasing relationships.

## Data Source
- Dataset: Amazon Product Co-Purchasing Network Metadata
- Source: http://snap.stanford.edu/data/amazon-meta.html
- Size: 548,552 products, 534.1k after cleaning
- Types: Books, Music CDs, DVDs, VHS tapes

## Project Objectives
1. Implement a co-purchasing data analytics engine using:
   - MongoDB (NoSQL database)
   - Apache Spark MLlib

2. Complex Query System
   - SQL-like query implementation (non-SQL based)
   - Query format: 'SELECT * FROM U WHERE Condition'
   - Support for:
     - Searchable attributes (value constraints)
     - Non-searchable attributes (derived metrics)
     - Enriched operators (>, >=, =, <, <=)

3. Co-Purchasing Pattern Analysis
   - Split data into training and testing sets
   - Identify frequent co-purchasing patterns
   - Pattern validation across datasets
   - Customer pattern matching
   - Significant pattern identification

## Technologies Used
- MongoDB for data storage and querying
- Apache Spark for data processing
- Python for implementation
- Git for version control


## Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/amazon-co-purchasing-analysis.git
   cd amazon-co-purchasing-analysis
   ```

2. **Install the required dependencies**

3. **Set up MongoDB**
   - Install MongoDB from the [official website](https://www.mongodb.com/try/download/community).
   - Start the MongoDB server:
     ```sh
     net start MongoDB
     ```

4. **Load the dataset into MongoDB**
   - Use the provided script to load data:
     ```sh
     python IngestionScripts/LoadCollection.py
     ```


## Team
* Coug Coders

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.