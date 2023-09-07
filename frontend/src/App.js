import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import EatoutRegistration from "./pages/eatoutRegistration";
import Expences from "./pages/expences";
import GradientRegistration from "./pages/gradientRegistration";
import Home from "./pages/home";
import EatoutRegistration from "./pages/eatoutRegistration";
import GradientRegistration from "./pages/gradientRegistration";
import FoodList from "./pages/foodList";
import Compare from "./pages/compare";
import Login from "./pages/login";
import UserRegister from "./pages/userRegister";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<UserRegister />} />
      <Route path="/home" element={<Home />} />
      <Route path="/expences" element={<Expences />} />
      <Route path="/compare" element={<Compare />} />
      <Route path="/gradient" element={<FoodList />} />
      <Route path="/eatoutRegistrate" element={<EatoutRegistration />} />
      <Route path="/gradientRegistrate" element={<GradientRegistration />} />
    </Routes>
  );
}

export default App;
