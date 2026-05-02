import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import AIChat from "./components/AIChat";
import RatingCard from "./components/Rating";
import Home from "./components/Home";
import Recommended from "./components/Recommended";
import Dashboard from "./components/Dashboard"

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        {/* <Route path="/" element={<Navigate to="/rating-graph" replace />} /> */}
        <Route path="/rating/:username" element={<RatingCard />} />
        <Route path="/dashboard/:username" element={<Dashboard />} />
        <Route path="/recommended/:username" element={<Recommended />} />
        <Route path="/ai-chat/:username" element={<AIChat />} />
        <Route path="*" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
