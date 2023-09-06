import React from "react";
import "./App.css";
import { Route, Routes } from "react-router-dom";

import Home from "./pages/home";
import EatoutRegistration from "./pages/eatoutRegistration";
import GradientRegistration from "./pages/gradientRegistration";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/compare" element={<Home />} />
      <Route path="/gradient" element={<Home />} />
      <Route path="/eatoutRegistrate" element={<EatoutRegistration />} />
      <Route path="/gradientRegistrate" element={<GradientRegistration />} />
    </Routes>
  );
}

export default App;
