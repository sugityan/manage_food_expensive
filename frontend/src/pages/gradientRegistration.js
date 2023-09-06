import React from 'react';

import Header from '../components/header';
import Sidebar from "../components/sidebar";

function GradientRegistration() {
  return (
    <>
    <Header />
      <div className="flex h-screen">
        <Sidebar />
        <form  className="flex flex-col justify-center gap-4 text-2xl">
          <p>名前　<input type="text" id="name" name="name" required className="border-2" /></p>
          <p>カテゴリー　<input type="text" id="category" name="catgory" required className="border-2" /></p>
          <div className="flex gap-10">
            <p>購入日　<input type="date" id="date" name="date" required /></p>
            <p>賞味期限/消費期限　<input type="date" id="limit" name="limit" required /></p>
          </div>
          <div className="flex gap-10">
            <p>金額　<input typte="number" id="price" name="price" required className="border-2" />円</p>
            <p>
              量　<input type="number" id="amount" name="price" required className="border-2" />
              <select id="unit" name="unit" className="border-2">
                <option>個</option>
                <option>g</option>
                <option>ml</option>
              </select>
            </p>
          </div>
          <div>
            メモ　<input type="text" id="memo" name="memo" className="border-2" />
          </div>
          <p className="flex justify-end"><input type="submit" value="登録" method="POST" className="border-2" /></p>
        </form>
      </div>
    </>
  );
}

export default GradientRegistration;
