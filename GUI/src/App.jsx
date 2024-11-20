import React, { useState, useEffect } from "react";
import ProductGrid from "./components/ProductGrid.jsx";

export default function App() {
  const [products, setProducts] = useState([]); // Store fetched products
  const [searchTerm, setSearchTerm] = useState(""); // Search term

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/api/products?search=${searchTerm}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched products:", data); // Debugging: Log fetched data
        setProducts(data); // Update the products state
      } catch (err) {
        console.error("Failed to fetch products:", err);
      }
    };

    fetchProducts();
  }, [searchTerm]);

  return (
    <main className="p-4">
      {/* Product Grid */}
      <ProductGrid products={products} />
    </main>
  );
}
