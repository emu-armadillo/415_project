import React from 'react';
import ProductGrid from './components/ProductGrid.jsx';

const products = [
  // Cars-related items
  {
    id: 1,
    asin: "B001234567",
    title: "Car Seat Cover - Universal Fit",
    similar: ["B001234568", "B001234569"],
    rating: 4.2
  },
  {
    id: 2,
    asin: "B001234568",
    title: "Car Steering Wheel Cover",
    similar: ["B001234567", "B001234570"],
    rating: 4.5
  },
  {
    id: 3,
    asin: "B001234569",
    title: "Car Floor Mats - All Weather",
    similar: ["B001234567", "B001234571"],
    rating: 4.7
  },
  {
    id: 4,
    asin: "B001234570",
    title: "LED Headlights for Cars",
    similar: ["B001234568", "B001234572"],
    rating: 4.3
  },
  {
    id: 5,
    asin: "B001234571",
    title: "Car Cleaning Kit - 10 Pieces",
    similar: ["B001234569", "B001234573"],
    rating: 4.8
  },

  // Fishing-related items
  {
    id: 6,
    asin: "F001234567",
    title: "Fishing Rod and Reel Combo",
    similar: ["F001234568", "F001234569"],
    rating: 4.6
  },
  {
    id: 7,
    asin: "F001234568",
    title: "Fishing Lures Set - 50 Pieces",
    similar: ["F001234567", "F001234570"],
    rating: 4.4
  },
  {
    id: 8,
    asin: "F001234569",
    title: "Waterproof Fishing Tackle Box",
    similar: ["F001234567", "F001234571"],
    rating: 4.7
  },
  {
    id: 9,
    asin: "F001234570",
    title: "Fishing Hat with Neck Flap",
    similar: ["F001234568", "F001234572"],
    rating: 4.2
  },
  {
    id: 10,
    asin: "F001234571",
    title: "Foldable Fishing Chair",
    similar: ["F001234569", "F001234573"],
    rating: 4.9
  },

  // Mixed additional items
  {
    id: 11,
    asin: "B001234572",
    title: "Car Emergency Tool Kit",
    similar: ["B001234567", "B001234568"],
    rating: 4.6
  },
  {
    id: 12,
    asin: "F001234572",
    title: "Fishing Net - Collapsible",
    similar: ["F001234567", "F001234568"],
    rating: 4.3
  },
  {
    id: 13,
    asin: "B001234573",
    title: "Car Wax and Polish Kit",
    similar: ["B001234569", "B001234570"],
    rating: 4.7
  },
  {
    id: 14,
    asin: "F001234573",
    title: "Fishing Gloves - Waterproof",
    similar: ["F001234569", "F001234570"],
    rating: 4.8
  },
  {
    id: 15,
    asin: "F001234574",
    title: "Portable Fish Finder",
    similar: ["F001234567", "F001234568"],
    rating: 4.4
  }
];

export default function App() {
  return (
    <main>
      <ProductGrid products={products} />
    </main>
  );
}
