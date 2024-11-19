import { useState } from 'react';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 w-full bg-slate-50 shadow-md  z-50">
        <nav className="w-full px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo/Title Section */}
            <div className="flex items-center">
              <h1 className="text-xl font-bold tracking-widest uppercase md:text-2xl text-teal-600">
                Co-Purchasing Recommender
              </h1>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:block">
              <div className="flex items-center space-x-4">
                <a href="/Home" 
                  className="px-4 py-2 text-teal-600 bg-white border border-teal-600 rounded-md hover:bg-teal-50 transition-colors duration-200 ease-in-out">Home</a>
                <a href="/about" 
                className="px-4 py-2 text-teal-600 bg-white border border-teal-600 rounded-md hover:bg-teal-50 transition-colors duration-200 ease-in-out">About</a>
              </div>
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="inline-flex items-center justify-center p-2 text-stone-600 hover:text-teal-600"
              >
                <svg
                  className="w-8 h-8"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  {isMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1">
                <a href="/" 
                  className="w-auto px-4 py-2 text-teal-600 bg-white border border-teal-600 rounded-md hover:bg-teal-50 transition-colors duration-200 ease-in-out"
                  >Home</a>
                <a href="/about" 
                  className="w-auto px-4 py-2 text-teal-600 bg-white border border-teal-600 rounded-md hover:bg-teal-50 transition-colors duration-200 ease-in-out"
                  >About</a>
              </div>
            </div>
          )}
        </nav>

      </header>
      {/* Added this div to prevent content from hiding under fixed header */}
      <div className="h-16"></div>
    </>
  );
}