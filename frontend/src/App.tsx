import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import AnalyzePage from "./pages/AnalyzePage";
import ClassifyPage from "./pages/ClassifyPage";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/analyze" element={<AnalyzePage />} />
        <Route path="/classify" element={<ClassifyPage />} />
      </Routes>
    </Router>
  );
};

export default App;