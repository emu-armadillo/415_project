import React, { useState } from 'react';
import ItemCard from './ItemCard.jsx';
import Header from './Header.jsx';

export default function ProductGrid({ products }) {
  const [selectedAsin, setSelectedAsin] = useState(null); // Track the selected ASIN
  const [similarItems, setSimilarItems] = useState([]); // Track similar items
  const [searchTerm, setSearchTerm] = useState(''); // Track search input
  const [searchLimit, setSearchLimit] = useState(10); // Limit for search results (default: 10)
  const [similarLimit, setSimilarLimit] = useState(5); // Limit for similar items (default: 5)

  const handleCardClick = (asin) => {
    setSelectedAsin(asin); // Highlight the selected product
    const selectedProduct = products.find((product) => product.asin === asin);
    if (selectedProduct) {
      // Update the state with similar items
      const similar = products.filter((product) =>
        selectedProduct.similar.includes(product.asin)
      );
      setSimilarItems(similar);
    }
  };

  const filteredProducts = products
    .filter(
      (product) =>
        product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.asin.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .slice(0, searchLimit); // Limit the number of search results

  const displayedSimilarItems = similarItems.slice(0, similarLimit); // Limit the number of similar items

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

          {/* Dropdown for Search Limit */}
          <div className="mt-4">
            <label className="mr-2 text-gray-700 font-semibold">Results per page:</label>
            <select
              value={searchLimit}
              onChange={(e) => setSearchLimit(Number(e.target.value))}
              className="p-2 border rounded-md shadow-md"
            >
              {[10, 20, 30, 40, 50].map((limit) => (
                <option key={limit} value={limit}>
                  {limit}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredProducts.map((product) => (
            <ItemCard
              key={product.id}
              title={product.title}
              asin={product.asin}
              rating={product.rating}
              isSelected={product.asin === selectedAsin} // Highlight selected
              onClick={() => handleCardClick(product.asin)} // Handle click
            />
          ))}
        </div>

        {/* Similar Items Section */}
        {similarItems.length > 0 && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Similar Items</h2>

            {/* Dropdown for Similar Limit */}
            <div className="mb-4">
              <label className="mr-2 text-gray-700 font-semibold">Show up to:</label>
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

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {displayedSimilarItems.map((product) => (
                <ItemCard
                  key={product.id}
                  title={product.title}
                  asin={product.asin}
                  rating={product.rating}
                  isSelected={false} // No highlighting for similar items
                  onClick={() => handleCardClick(product.asin)} // Allow deeper navigation
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
