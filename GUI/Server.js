import express from "express";
import mongoose from "mongoose";
import cors from "cors";

const app = express();
const PORT = 5000;

// Middleware
app.use(express.json());
app.use(cors()); // Enable CORS for all routes

// Update your MongoDB URI as needed
const MONGO_URI =
  "mongodb+srv://Guest:Password@415cluster01.4lf0c.mongodb.net/AmazonCopurchasing?retryWrites=true&w=majority";

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB Atlas"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

// Product schema & model (from ProductMetaData collection)
const ProductSchema = new mongoose.Schema({
  ASIN: String,
  title: String,
  similar: { items: [String] },
  reviews: { avg_rating: Number },
});

const Product = mongoose.model("Product", ProductSchema, "ProductMetaData");

// CleanedItemSet schema & model
const CleanedSchema = new mongoose.Schema({
  _id: String,
  similar_items: [{ asin: String, frequency: Number }]
}, { _id: false });

const CleanedItemSet = mongoose.model("CleanedItemSet", CleanedSchema, "CleanedItemSet");

// Route to fetch products (with optional search and limit)
app.get("/api/products", async (req, res) => {
  try {
    const { search = "", limit = 50 } = req.query;
    const query = search
      ? {
          $or: [
            { title: { $regex: search, $options: "i" } },
            { ASIN: { $regex: search, $options: "i" } },
          ],
        }
      : {};

    const products = await Product.find(query)
      .limit(Number(limit))
      .select("ASIN title similar.items reviews.avg_rating");

    const responseData = products.map((product) => ({
      asin: product.ASIN,
      title: product.title,
      similar: product.similar?.items || [],
      rating: product.reviews?.avg_rating || "N/A",
    }));

    res.json(responseData);
  } catch (err) {
    console.error("Error fetching products:", err);
    res.status(500).json({ error: "Failed to fetch products" });
  }
});

// Helper function to merge similar items from both sources
function mergeSimilarItems(productSimilarAsins, cleanedSimilarItems) {
  // Start with product-based similar ASINs
  const result = productSimilarAsins.map(asin => ({
    asin,
    fromProduct: true
  }));

  // Merge cleaned set similar items
  cleanedSimilarItems.forEach(cleanedItem => {
    const existing = result.find(r => r.asin === cleanedItem.asin);
    if (existing) {
      existing.frequency = cleanedItem.frequency;
      existing.fromCleaned = true;
    } else {
      result.push({
        asin: cleanedItem.asin,
        frequency: cleanedItem.frequency,
        fromCleaned: true
      });
    }
  });

  return result;
}

// Route to fetch a single product by ASIN and combine similar items
app.get("/api/products/:asin", async (req, res) => {
  try {
    const { asin } = req.params;

    // Fetch product and cleaned set in parallel
    const [product, cleanedSet] = await Promise.all([
      Product.findOne({ ASIN: asin }).select("ASIN title similar.items reviews.avg_rating"),
      CleanedItemSet.findOne({ _id: asin }).select("similar_items")
    ]);

    // Validate existence
    if (!product) {
      return res.status(404).json({ error: "Product not found in ProductMetaData." });
    }
    if (!cleanedSet) {
      return res.status(404).json({ error: "No cleaned data found for this product." });
    }

    // Merge similar items
    const combinedSimilar = mergeSimilarItems(
      product.similar?.items || [],
      cleanedSet.similar_items || []
    );

    res.json({
      asin: product.ASIN,
      title: product.title,
      similar: combinedSimilar,
      rating: product.reviews?.avg_rating || "N/A",
    });
  } catch (err) {
    console.error("Error fetching product by ASIN:", err);
    res.status(500).json({ error: "Failed to fetch product" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
