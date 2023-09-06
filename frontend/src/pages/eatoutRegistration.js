import React, { useState } from 'react';
import axios from 'axios';
import Header from '../components/header';
import Sidebar from "../components/sidebar";

function EatoutRegistration() {
  const [formData, setFormData] = useState({
    date: '',
    price: '',
    purpose: '0' 
  });
  const [result, setResult] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/eatout_register', formData);
      
      if (response.status === 200) {
        console.log("Data sent successfully");
        setResult(response.data.result);
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
        <form onSubmit={handleSubmit} className="flex flex-col justify-center gap-4 text-2xl">
          <p>日付<input type="date" id="date" name="date" required onChange={handleChange} /></p>
          <p>金額<input type="number" step="1" id="price" name="price" required onChange={handleChange} className="border-2" />円</p>
          <div>
            用途<select id="purpose" name="purpose" onChange={handleChange} className="border-2">
              <option value="0">飲み会</option> 
              <option value="1">その他</option> 
            </select>
          </div>
          <p className="flex justify-end"><input type="submit" value="登録" className="border-2" /></p>
          
        </form>
        {result && <div className="mt-4 text-xl">{result}</div>}
      </div>
    </>
  );
}

export default EatoutRegistration;
