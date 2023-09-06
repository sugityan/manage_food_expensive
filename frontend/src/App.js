import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/', { name: name, email: email });
      setResult(response.data.result);
    } catch (error) {
      console.error("APIからデータの取得に失敗しました:", error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="p-6 bg-green-200 shadow-md rounded-md">
        <input 
          type="text"
          value={name}
          placeholder="Name" 
          onChange={handleNameChange}
          className="p-2 border rounded w-full mb-2"
        />
        <input 
          type="email"
          value={email}
          placeholder="Email" 
          onChange={handleEmailChange}
          className="p-2 border rounded w-full"
        />
        <button 
          onClick={handleSubmit}
          className="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full"
        >
          送信
        </button>
        {result && (
          <p className="mt-4 text-gray-700 font-bold">結果: {result}</p>
        )}
      </div>
    </div>
  );
}

export default App;
