import React from 'react';
import amazonLogo from '/src/assets/amazonlogo.png';

export default function ItemCard({ title, asin, rating, isSelected, onClick }) {
  return (
    <div
      className={`border p-4 rounded-lg shadow-md hover:shadow-lg cursor-pointer bg-white ${
        isSelected ? 'ring-2 ring-blue-500' : ''
      }`}
      onClick={onClick}
    >
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-lg">{title}</h3>
        <img src={amazonLogo} alt="Amazon Logo" className="w-8 h-8" />
      </div>
      <p>ASIN: {asin}</p>
      <p>Rating: {rating} / 5</p>
    </div>
  );
}
