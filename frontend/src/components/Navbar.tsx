import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <nav className="bg-gray-900 text-white p-4 flex gap-4">
      <Link to="/upload" className="hover:underline">Upload</Link>
      <Link to="/analyze" className="hover:underline">Analyze</Link>
      <Link to="/classify" className="hover:underline">Classify</Link>
    </nav>
  );
};

export default Navbar;