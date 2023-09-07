import axios from "axios";
import React, { useState } from "react";
import Header from "../components/header";
import Sidebar from "../components/sidebar";
import { useNavigate } from "react-router-dom";;


function EatoutRegistration() {
  const baseUrl = "http://127.0.0.1:8000";
  const purpose_dict = {"0":"食堂・レストラン", "1": "飲み会・宴会", "2": "その他"}
  const [formData, setFormData] = useState({
    date: "",
    price: "",
    purpose: "0",
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
        baseUrl + "/shopping",{
          Date: formData.date,
          Purpose: formData.purpose,
          Price: formData.price,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          }
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
          className="flex flex-col justify-center w-2/5 gap-4 text-3xl leading-loose"
        >
          <p>
            日付
            <input
              type="date"
              id="date"
              name="date"
              required
              onChange={handleChange}
            />
          </p>
          <p>
            金額
            <input
              type="number"
              step="1"
              id="price"
              name="price"
              required
              onChange={handleChange}
              className="pr-5 pl-5 rounded-full border-2"
            />
            円
          </p>
          <div>
            用途
            <select
              id="purpose"
              name="purpose"
              onChange={handleChange}
              className="border-2"
            >
                <option value="0">食堂・レストラン</option>
                <option value="1">飲み会・宴会</option>
              <option value="2">その他</option>
            </select>
          </div>
          <p className="flex justify-end">
            <input type="submit" value="登録" className="pr-5 pl-5 rounded-full border-2" />
          </p>
        </form>
        </div>
      </div>
    </>
  );
}

export default EatoutRegistration;
