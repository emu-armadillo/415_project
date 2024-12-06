import React, { useState, useEffect } from "react";
import ItemCard from "./ItemCard.jsx";
import Header from "./Header.jsx";

export default function ProductGrid() {
  const [products, setProducts] = useState([]);            // Products fetched from the backend
  const [searchTerm, setSearchTerm] = useState("");         // Track search input
  const [selectedAsin, setSelectedAsin] = useState(null);    // Track selected ASIN
  const [lastSelectedProduct, setLastSelectedProduct] = useState(null); // Persist the last selected product
  const [similarItems, setSimilarItems] = useState([]);      // Track similar items
  const [similarLimit, setSimilarLimit] = useState(5);       // Limit for similar items
  const [outputLimit, setOutputLimit] = useState(10);        // Limit for main search results
  const [isLoading, setIsLoading] = useState(false);         // Loading state for search results
  const [similarLoading, setSimilarLoading] = useState(false); // Loading state for similar items

  // Fetch products based on search term and limit
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(
          `http://localhost:5000/api/products?search=${encodeURIComponent(searchTerm)}&limit=${outputLimit}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched products:", data);
        setProducts(data);
      } catch (err) {
        console.error("Error fetching products:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [searchTerm, outputLimit]);

  const fetchSimilarItems = async (asin) => {
    try {
      setSimilarLoading(true);
      const currentAsin = asin;

      const response = await fetch(`http://localhost:5000/api/products/${currentAsin}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Fetched similar items for ASIN:", currentAsin, data.similar);

      // Fetch details for each similar ASIN to get their titles
      const similarDetails = await Promise.all(
        data.similar.map(async (similarObj) => {
          const similarAsin = similarObj.asin;
          const similarResponse = await fetch(`http://localhost:5000/api/products/${similarAsin}`);
          if (similarResponse.ok) {
            const similarData = await similarResponse.json();
            return {
              asin: similarAsin,
              title: similarData.title || `ASIN: ${similarAsin}`,
            };
          }
          return null;
        })
      );

      const validSimilarItems = similarDetails.filter(item => item !== null);
      setSimilarItems(validSimilarItems);
    } catch (err) {
      console.error("Error fetching similar items:", err);
      setSimilarItems([]);
    } finally {
      setSimilarLoading(false);
    }
  };

  const handleCardClick = (asin) => {
    console.log("Selected ASIN:", asin);
    setSelectedAsin(asin);

    // Update lastSelectedProduct based on the product currently clicked
    const clickedProduct = products.find(p => p.asin === asin);
    if (clickedProduct) {
      setLastSelectedProduct(clickedProduct);
    }

    setSimilarItems([]);
    fetchSimilarItems(asin);
  };

  return (
    <div>
      <Header />

      <div className="p-4">
        {/* Search Bar */}
        <div className="flex flex-col items-center mb-6">
          <input
            type="text"
            placeholder="Search for products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full max-w-md p-4 border rounded-lg shadow-md text-lg"
          />

          {/* Always highlight the last selected product if one exists */}
          {lastSelectedProduct && (
            <div className="mt-4 p-2 border rounded-md shadow-md bg-gray-100 text-gray-700 text-center">
              <p className="font-semibold">Last Selected Product:</p>
              <p>{lastSelectedProduct.title} (ASIN: {lastSelectedProduct.asin})</p>
            </div>
          )}
        </div>

        {/* Results Per Page Dropdown */}
        <div className="mb-6 flex justify-center items-center">
          <label className="mr-2 text-gray-700 font-semibold">
            Results per page:
          </label>
          <select
            value={outputLimit}
            onChange={(e) => setOutputLimit(Number(e.target.value))}
            className="p-2 border rounded-md shadow-md"
          >
            {[10, 20, 30, 40, 50].map((limit) => (
              <option key={limit} value={limit}>
                {limit}
              </option>
            ))}
          </select>
        </div>

        {/* Loading Indicator for Products */}
        {isLoading && <p className="text-center text-gray-500">Loading products...</p>}

        {/* Product Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {products.slice(0, outputLimit).map((product) => (
            <ItemCard
              key={product.asin}
              title={product.title}
              asin={product.asin}
              rating={product.rating}
              isSelected={product.asin === selectedAsin}
              onClick={() => handleCardClick(product.asin)}
            />
          ))}
        </div>

        {/* Divider Line */}
        <div className="flex justify-center my-8">
          <div className="min-w-full border-t-2 border-gray-600"></div>
        </div>

        {/* Similar Items Section */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Recommended Items</h2>

          {/* Dropdown for Similar Limit */}
          <div className="mb-4">
            <label className="mr-2 text-gray-700 font-semibold">
              Show up to:
            </label>
            <select
              value={similarLimit}
              onChange={(e) => setSimilarLimit(Number(e.target.value))}
              className="p-2 border rounded-md shadow-md"
            >
              {[5, 10, 15, 20].map((limit) => (
                <option key={limit} value={limit}>
                  {limit}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Similar Items Display */}
        {similarLoading && <p className="text-center text-gray-500">Loading recommended items...</p>}
        {!similarLoading && similarItems.length > 0 ? (
          <div className="mt-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {similarItems.slice(0, similarLimit).map((item) => (
                <ItemCard
                  key={item.asin}
                  title={item.title}
                  asin={item.asin}
                  rating={"N/A"} // Placeholder rating
                  isSelected={false}
                  onClick={() => handleCardClick(item.asin)}
                />
              ))}
            </div>
          </div>
        ) : (
          !similarLoading && (
            <p className="mr-2 font-bold text-gray-700">
              No similar items found, select another item
            </p>
          )
        )}
      </div>
    </div>
  );
}
