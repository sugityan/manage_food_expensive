import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import EatoutRegistration from "./pages/eatoutRegistration";
import GradientRegistration from "./pages/gradientRegistration";
import Home from "./pages/home";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/compare" element={<Home />} />
      <Route path="/gradient" element={<Home />} />
      <Route path="/registration/shopping" element={<GradientRegistration />} />
      <Route path="/registration/eatout" element={<EatoutRegistration />} />
    </Routes>
  );
}

export default App;
