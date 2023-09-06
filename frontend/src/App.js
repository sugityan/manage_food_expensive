import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import EatoutRegistration from "./pages/eatoutRegistration";
import Expences from "./pages/expences";
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
      <Route path="/expences" element={<Expences />} />
    </Routes>
  );
}

export default App;
