import Header from "../components/header";
import React, { useState } from "react";
import Sidebar from "../components/sidebar";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function GradientChange() {
  const location = useLocation();
  const food = location.state?.food;

  const baseUrl = "http://127.0.0.1:8000";
  const [formData, setFormData] = useState({
    name: food?.name || "",
    category: food?.category || "0",
    date: food?.Date || "",
    limit: food?.expiry_date || "",
    price: food?.price || "",
    amount: food?.amount || "0",
    unit: food?.unit || "個",
    memo: food?.memo || "",
  });
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (event) => {
    console.log(formData.category);
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.put(
        baseUrl + "/food_db",
        {
          FoodID: food.FoodID,
          name: formData.name,
          category: formData.category,
          price: formData.price,
          expiry_date: formData.limit,
          Date: formData.date,
          amount: formData.amount,
          unit: formData.unit,
          memo: formData.memo,
          Remaining: food.Remaining,
          status: food.status,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (response.status === 200) {
        setResult(response.data.result);
        navigate("/home"); // /homeにリダイレクト
      } else {
        console.error("Error sending data:", response.data);
      }
    } catch (error) {
      console.error("There was an error:", error);
    }
  };

  return (
    <>
      <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex justify-center w-screen">
          <form
            onSubmit={handleSubmit}
            action="/"
            className="flex flex-col justify-center gap-4 text-3xl leading-loose"
          >
            <p>
              名前　
              <input
                type="text"
                id="name"
                name="name"
                required
                className="pr-5 pl-5 rounded-full border-2"
                onChange={handleChange}
                value={formData.name}
              />
            </p>
            <p>
              カテゴリー　
              <select
                id="category"
                name="category"
                onChange={handleChange}
                required
                className="pr-5 pl-5 rounded-full border-2"
                value={formData.category}
              >
                <option selected value="">
                  選択してください
                </option>
                <option value="0">肉類・魚介類・卵</option>
                <option value="1">野菜</option>
                <option value="2">果物</option>
                <option value="3">穀類</option>
                <option value="4">乳製品</option>
                <option value="5">調味料</option>
                <option value="6">飲料</option>
                <option value="7">その他</option>
              </select>
            </p>
            <div className="flex gap-10">
              <p>
                購入日　
                <input
                  type="date"
                  id="date"
                  name="date"
                  onChange={handleChange}
                  required
                  className="pr-5 pl-5 rounded-full"
                  value={formData.date}
                />
              </p>
              <p>
                賞味期限／消費期限　
                <input
                  type="date"
                  id="limit"
                  name="limit"
                  onChange={handleChange}
                  required
                  className="pr-5 pl-5 rounded-full"
                  value={formData.limit}
                />
              </p>
            </div>
            <div className="flex gap-10">
              <p>
                金額　
                <input
                  typte="number"
                  id="price"
                  name="price"
                  required
                  className="pr-5 pl-5 rounded-full border-2"
                  onChange={handleChange}
                  value={formData.price}
                />
                円
              </p>
              <p>
                量　
                <input
                  type="number"
                  id="amount"
                  name="amount"
                  required
                  className="pr-8 pl-8 rounded-full border-2"
                  onChange={handleChange}
                  value={formData.amount}
                />
                <select
                  id="unit"
                  name="unit"
                  onChange={handleChange}
                  className="pr-5 pl-5 rounded-full border-2"
                  value={formData.unit}
                >
                  <option value="個">個</option>
                  <option value="g">g</option>
                  <option value="ml">ml</option>
                  <option value="その他">その他</option>
                </select>
              </p>
            </div>
            <div className="w-full">
              メモ　
              <textarea
                id="memo"
                name="memo"
                onChange={handleChange}
                className="pr-5 pl-5 rounded-3xl border-2 w-full"
                value={formData.memo}
              />
            </div>
            <p className="flex justify-end">
              <input
                type="submit"
                value="変更"
                className="pr-5 pl-5 rounded-full border-2"
              />
            </p>
          </form>
        </div>
      </div>
    </>
  );
}

export default GradientChange;
