import React from 'react';

import Header from '../components/header';
import Sidebar from "../components/sidebar";

function EatoutRegistration() {
  return (
    <>
    <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex justify-center w-screen">
          <form  className="flex flex-col justify-center w-1/3 gap-4 text-3xl leading-loose">
            <p>日付　<input type="date" id="date" name="date" required /></p>
            <p>金額　<input typte="number" step="1" id="price" name="price" required className="border-2" />円</p>
            <div>
              用途　<select id="purpose" name="purpose" className="border-2">
                <option>飲み会</option>
                <option>その他</option>
              </select>
            </div>
            <p className="flex justify-end"><input type="submit" value="登録" method="POST" className="border-2" /></p>
          </form>
        </div>
      </div>
    </>
  );
}

export default EatoutRegistration;
