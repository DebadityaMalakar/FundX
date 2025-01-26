import React, { useState, useEffect } from 'react';
import "../tailwind.css"
const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [currentPath, setCurrentPath] = useState('');

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setIsMobile(true);
      } else {
        setIsMobile(false);
        setIsOpen(false);
      }
    };

    handleResize();

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    setCurrentPath(window.location.pathname);
  }, []);

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Business', path: '/business' },
    { name: 'Contact', path: '/contact' },
  ];

  return (
    <nav className="bg-black-700 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-white text-lg font-bold">
          <img src="/favicon.ico" alt="" />
        </div>

        {/* Hamburger Menu Icon (visible on mobile) */}
        {isMobile && (
          <button
            onClick={toggleMenu}
            className="text-white focus:outline-none"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Three equal-length lines */}
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </button>
        )}

        {/* Navigation Links (visible on desktop or when menu is open on mobile) */}
        <div
          className={`${
            isMobile ? (isOpen ? 'flex' : 'hidden') : 'flex'
          } flex-col md:flex-row md:space-x-4 mt-4 md:mt-0 space-y-2 md:space-y-0`}
        >
          {navLinks.map((link) => (
            <a
              key={link.path}
              href={currentPath === link.path ? '#' : link.path}
              className={`text-white hover:text-gray-400 ${
                currentPath === link.path ? 'font-bold' : ''
              }`}
            >
              {link.name}
            </a>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;