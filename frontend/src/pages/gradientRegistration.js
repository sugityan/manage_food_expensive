import Header from "../components/header";
import React, { useState } from "react";
import Sidebar from "../components/sidebar";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function GradientRegistration() {
  const baseUrl = "http://127.0.0.1:8000";
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    date: "",
    limit: "",
    price: "",
    amount: "0",
    unit: "個",
    memo: "",
  });
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(
        baseUrl + "/food_db",
        {
          name: formData.name,
          category: formData.category,
          price: formData.price,
          expiry_date: formData.limit,
          Date: formData.date,
          amount: formData.amount,
          unit: formData.unit,
          memo: formData.memo,
          Remaining: 100,
          status: 1,
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
        navigate("/home");
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
        <div className="flex justify-center  w-screen">
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
              />
            </p>
            <p>
              カテゴリー　
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
                className="pr-5 pl-5 rounded-full border-2"
              >
                <option value="">
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
                />
              </p>
            </div>
            <div className="flex gap-10">
              <p>
                金額　
                <input
                  type="number"
                  id="price"
                  name="price"
                  required
                  className="pr-5 pl-5 rounded-full border-2"
                  onChange={handleChange}
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
                />
                <select
                  id="unit"
                  name="unit"
                  onChange={handleChange}
                  className="pr-5 pl-5 rounded-full border-2"
                >
                  <option value="個">個</option>
                  <option value="g">g</option>
                  <option value="ml">ml</option>
                  <option value="その他">その他</option>
                </select>
              </p>
            </div>
            <div className="w-full">
              メモ<br />
              <textarea
                id="memo"
                name="memo"
                rows="1"
                onChange={handleChange}
                className="w-full rounded-md border-2"
              />
            </div>
            <div className="flex justify-center mt-100">
              <button
                type="submit"
                className="w-1/3 text-3xl bg-yellow-500 rounded-lg shadow-lg hover:bg-yellow-600"
              >
                登録
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default GradientRegistration;
