import { useState } from 'react';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 w-full bg-slate-50 shadow-md z-50">
        <nav className="w-full px-4">
          <div className="flex items-center justify-between h-14">
            {/* Title Section */}
            <div className="flex items-center">
              <h1 className="text-lg font-bold tracking-wide uppercase md:text-xl text-black">
                Coug Coder Co-Purchasing Recommender
              </h1>
            </div>

            {/* Home Button */}
            <div>
              <a
                href="/"
                className="px-4 py-2 bg-gray-600 text-white rounded-md shadow-md hover:bg-Blue-700 transition"
              >
                Home
              </a>
            </div>
          </div>
        </nav>
      </header>

      {/* Prevent content from hiding under fixed header */}
      <div className="h-14"></div>
    </>
  );
}
