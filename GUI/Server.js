import express from "express";
import mongoose from "mongoose";
import cors from "cors"; // Import CORS middleware

const app = express();
const PORT = 5000;

// Middleware
app.use(express.json());
app.use(cors()); // Enable CORS for all routes

const MONGO_URI =
  "mongodb+srv://Guest:Password@415cluster01.4lf0c.mongodb.net/AmazonCopurchasing?retryWrites=true&w=majority";

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB Atlas"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

const ProductSchema = new mongoose.Schema({
  ASIN: String,
  title: String,
  similar: { items: [String] },
  reviews: { avg_rating: Number },
});

const Product = mongoose.model("Product", ProductSchema, "ProductMetaData");

// Example route with CORS enabled
app.get("/api/products", async (req, res) => {
  try {
    const { search = "" } = req.query;
    const query = search
      ? {
          $or: [
            { title: { $regex: search, $options: "i" } },
            { ASIN: { $regex: search, $options: "i" } },
          ],
        }
      : {};
    const products = await Product.find(query).limit(50).select("ASIN title similar.items reviews.avg_rating");
    res.json(
      products.map((product) => ({
        asin: product.ASIN,
        title: product.title,
        similar: product.similar?.items || [],
        rating: product.reviews?.avg_rating || "N/A",
      }))
    );
  } catch (err) {
    console.error("Error fetching products:", err);
    res.status(500).json({ error: "Failed to fetch products" });
  }
});

// Fetch a single product by ASIN
app.get("/api/products/:asin", async (req, res) => {
  try {
    const { asin } = req.params;

    // Find the product by ASIN
    const product = await Product.findOne({ ASIN: asin }).select(
      "ASIN title similar.items reviews.avg_rating"
    );

    if (!product) {
      return res.status(404).json({ error: "Product not found" });
    }

    res.json({
      asin: product.ASIN,
      title: product.title,
      similar: product.similar?.items || [],
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
