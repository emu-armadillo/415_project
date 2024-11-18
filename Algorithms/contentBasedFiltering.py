'''
3. Content-Based Filtering (Using TF-IDF or Word2Vec)
Use Case: Content-based filtering can be valuable if you want to recommend items based on descriptive fields like title, categories, or reviews.
How It Works: Sparks MLlib provides text processing with TF-IDF (for term frequency analysis) or Word2Vec (for semantic similarity). By vectorizing textual features, you can recommend items with similar descriptions, categories, or keywords.
Data Preparation: Preprocess text fields like title, categories, or even reviews to create embeddings. Then calculate cosine similarity to recommend similar items.

'''


from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.linalg import Vectors
from pyspark.ml import Pipeline
from pyspark.sql.types import FloatType

def create_spark_session():
    return SparkSession.builder \
        .appName("Content-Based Filtering") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/AmazonProject.ProductMetaData") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()

def preprocess_text_features(df):
    # Clean and combine features
    return df.select(
        "ASIN",
        "title",
        array_join("categories.details", " ").alias("category_text")
    ).na.fill("") \
    .withColumn(
        "combined_features",
        regexp_replace(
            concat_ws(" ", 
                lower(col("title")), 
                lower(col("category_text"))
            ),
            "[^a-zA-Z0-9\\s]", " "
        )
    )

def create_feature_pipeline():
    tokenizer = Tokenizer(inputCol="combined_features", outputCol="words")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
    countVectorizer = CountVectorizer(inputCol="filtered_words", outputCol="raw_features", 
                                    minDF=2.0, maxDF=0.95)
    idf = IDF(inputCol="raw_features", outputCol="features")
    
    return Pipeline(stages=[tokenizer, remover, countVectorizer, idf])

def cosine_similarity_udf(v1, v2):
    if v1 is None or v2 is None:
        return 0.0
    norm1 = Vectors.norm(v1, 2)
    norm2 = Vectors.norm(v2, 2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(v1.dot(v2) / (norm1 * norm2))

def get_similar_items(transformed_df, target_asin, top_n=5):
    # Register UDF
    similarity_udf = udf(lambda x, y: cosine_similarity_udf(x, y), FloatType())
    
    # Get target item features
    target_item = transformed_df.filter(col("ASIN") == target_asin).select("features").first()
    if not target_item:
        return None
    
    target_features = target_item["features"]
    
    # Calculate similarities
    return transformed_df.filter(col("ASIN") != target_asin) \
        .withColumn("similarity", similarity_udf(col("features"), lit(target_features))) \
        .select("ASIN", "title", "similarity") \
        .filter(col("similarity").isNotNull()) \
        .orderBy(desc("similarity")) \
        .limit(top_n) \
        .cache()

def main():
    spark = create_spark_session()
    
    # Read and cache initial dataframe
    df = spark.read.format("mongo").load().cache()
    
    # Process features
    processed_df = preprocess_text_features(df).cache()
    
    # Create and fit pipeline
    pipeline = create_feature_pipeline()
    model = pipeline.fit(processed_df)
    
    # Transform and cache features
    transformed_df = model.transform(processed_df).cache()
    
    # Get recommendations
    target_asin = "0895872218"
    similar_items = get_similar_items(transformed_df, target_asin)
    
    if similar_items:
        print(f"\nTop 5 similar items for ASIN {target_asin}:")
        similar_items.show(truncate=False)
    else:
        print(f"No similar items found for ASIN {target_asin}")
    
    # Cleanup
    spark.stop()

if __name__ == "__main__":
    main()