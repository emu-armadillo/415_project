'''
Item-based Collaborative Filtering (using ALS)
Use Case: Since your dataset has a similar field (related items for each book), you could use item-based collaborative filtering. ALS can also be applied in an item-item context to recommend products based on similarities between items.
How It Works: ALS can be set up to use item similarities rather than user preferences by focusing on the product ID interactions. You can create a "co-view" or "co-purchase" dataset based on the similar field.
Data Preparation: Convert each similar item list into pairs of item IDs, and calculate a frequency for each pair based on how often they appear together.
Example: After preparing a similarity matrix with item pairs, ALS can use it to recommend items.

3. Content-Based Filtering (Using TF-IDF or Word2Vec)
Use Case: Content-based filtering can be valuable if you want to recommend items based on descriptive fields like title, categories, or reviews.
How It Works: Spark’s MLlib provides text processing with TF-IDF (for term frequency analysis) or Word2Vec (for semantic similarity). By vectorizing textual features, you can recommend items with similar descriptions, categories, or keywords.
Data Preparation: Preprocess text fields like title, categories, or even reviews to create embeddings. Then calculate cosine similarity to recommend similar items.

'''

# record execution time of algorithm for performance evaluation