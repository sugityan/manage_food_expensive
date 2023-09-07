import React from 'react';

import Header from '../components/header';
import Sidebar from "../components/sidebar";

function GradientRegistration() {
  return (
    <>
    <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex justify-center w-screen">
          <form action="/" className="flex flex-col justify-center gap-4 text-3xl leading-loose">
            <p>名前　<input type="text" id="name" name="name" required className="pr-5 pl-5 rounded-full border-2" /></p>
            <p>カテゴリー　<input type="text" id="category" name="catgory" required className="pr-5 pl-5 rounded-full border-2" /></p>
            <div className="flex gap-10">
              <p>購入日　<input type="date" id="date" name="date" className="pr-5 pl-5 rounded-full" required /></p>
              <p>賞味期限／消費期限　<input type="date" id="limit" name="limit" className="pr-5 pl-5 rounded-full" required /></p>
            </div>
            <div className="flex gap-10">
              <p>金額　<input typte="number" id="price" name="price" required className="pr-5 pl-5 rounded-full border-2" />円</p>
              <p>
                量　<input type="number" id="amount" name="price" required className="pr-8 pl-8 rounded-full border-2" />
                <select id="unit" name="unit" className="pr-5 pl-5 rounded-full border-2">
                  <option>個</option>
                  <option>g</option>
                  <option>ml</option>
                </select>
              </p>
            </div>
            <div className="w-full">
              メモ　<textarea id="memo" name="memo" className="pr-5 pl-5 rounded-3xl border-2 w-full" />
            </div>
            <p className="flex justify-end"><input type="submit" value="登録" method="POST" className="pr-5 pl-5 rounded-full border-2" /></p>
          </form>
        </div>
      </div>
    </>
  );
}

export default GradientRegistration;
