"""
    Generate recommendations for a specific product using similar items and category matching
    
    Strategy:
    1. First get directly similar items
    2. Then get items from the same deepest category
    3. Combine and rank based on available metrics (salesrank, reviews)
"""

# record execution time of algorithm for performance evaluation

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, array, lit, size, when, collect_list
import time

if __name__ == "__main__":
    # Example usage with a specific ASIN
    target_asin = "0827229534"  # ASIN for "Patterns of Preaching: A Sermon Sampler" book
                                # similar: 
                                # Witness of Preaching, 
                                # The Four Pages of the Sermon: A Guide to Biblical Preaching
                                # Performing the Word: Preaching As Theatre, 
                                # Interpreting the Gospel: An Introduction to Preaching
                                # The Preaching Life
    num_recommendations = 5

    start_time = time.time()

    # Create Spark session with MongoDB connector
    spark = SparkSession.builder \
        .appName("Product Recommendations") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/AmazonProject.ProductMetaData") \
        .getOrCreate()

    # Read from MongoDB collection
    df = spark.read.format("mongo").load()

    # Get target product details
    target_product = df.filter(col("ASIN") == target_asin).first()
    if not target_product:
        raise ValueError("Target product not found")

    # Step 1: Get directly similar items
    similar_products = None
    if target_product.similar and target_product.similar.items:
        similar_asins = target_product.similar.items[0]
        similar_products = df.filter(col("ASIN").isin(similar_asins))

    # Step 2: Get products from the same deepest category
    category_products = None
    if target_product.categories and target_product.categories.details:
        # Get the deepest category (usually the last one in the list)
        target_category = target_product.categories.details[-1]
        
        # Use explode to check category membership
        category_products = df.select(
            "*",
            explode("categories.details").alias("category")
        ).filter(
            (col("category") == target_category) &
            (col("ASIN") != target_asin)  # Exclude target product
        ).dropDuplicates(["ASIN"])  # Remove duplicates if a product appears multiple times

    # Step 3: Combine recommendations
    recommendations = []
    
    # Add similar products first (they're directly related)
    if similar_products:
        similar_recs = similar_products.select(
            "ASIN",
            "title",
            "salesrank",
            col("reviews.avg_rating").alias("avg_rating")
        ).collect()
        recommendations.extend([
            {
                "asin": row["ASIN"],
                "title": row["title"],
                "salesrank": row["salesrank"] if row["salesrank"] else None,
                "avg_rating": float(row["avg_rating"]) if row["avg_rating"] else None,
                "source": "similar"
            } for row in similar_recs
        ])

    # Add category products if we need more recommendations
    if category_products and len(recommendations) < num_recommendations:
        needed_recs = num_recommendations - len(recommendations)
        category_recs = category_products.orderBy(
            # Prioritize products with better sales rank and ratings
            col("salesrank").asc(),
            col("reviews.avg_rating").desc()
        ).limit(needed_recs).select(
            "ASIN",
            "title",
            "salesrank",
            col("reviews.avg_rating").alias("avg_rating")
        ).collect()
        
        recommendations.extend([
            {
                "asin": row["ASIN"],
                "title": row["title"],
                "salesrank": row["salesrank"] if row["salesrank"] else None,
                "avg_rating": float(row["avg_rating"]) if row["avg_rating"] else None,
                "source": "category"
            } for row in category_recs
        ])

    execution_time = time.time() - start_time

    # print results
    results = {
        "target_asin": target_asin,
        "target_title": target_product.title,
        "recommendations": recommendations[:num_recommendations],
        "execution_time": execution_time,
        "metadata": {
            "similar_items_found": len([r for r in recommendations if r["source"] == "similar"]),
            "category_items_found": len([r for r in recommendations if r["source"] == "category"]),
            "target_category": target_product.categories.details[-1] if target_product.categories else None
        }
    }

    
    """
    Print the recommendations in a formatted way
    """
    if "error" in results:
        print(f"\nError: {results['error']}")
        spark.stop()
        exit(1)

    print(f"\nRecommendations for: {results['target_title']} (ASIN: {results['target_asin']})")
    print("\nTop recommended products:")
    
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"\n{i}. {rec['title']} (ASIN: {rec['asin']})")
        print(f"   Source: {rec['source']}")
        if rec['salesrank']:
            print(f"   Sales Rank: {rec['salesrank']}")
        if rec['avg_rating']:
            print(f"   Average Rating: {rec['avg_rating']:.1f}")

    print(f"Similar items found: {results['metadata']['similar_items_found']}")
    print(f"Category items found: {results['metadata']['category_items_found']}")
    print(f"Target category: {results['metadata']['target_category']}")
    print(f"\nExecution time: {results['execution_time']:.2f} seconds")


    # Clean up
    spark.stop()