import React from 'react';

import Header from "../components/header";
import Sidebar from "../components/sidebar";

function Expences() {
  const expences = [{date: "2023-09-04", shopping: 1000, eatout: 600, sum:1600}, {date: "2023-09-05", shopping: 500, eatout: 1500, sum:2000}]
  const sumOfExpence = 10000
  
  return (
    <>
      <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div font-family="sans-serif" className="flex flex-col w-screen">
          <div className="flex flex-row justify-center w-1/3 mt-20 font-light p-5 rounded-full border-2">
            <p className=" justify-end text-4xl text-gray-500">今月の食費　</p>
            <p className=" text-4xl">¥ {sumOfExpence}</p>
          </div>
          <div className="flex justify-center">
          <table className="w-4/5 mt-20 justify-center text-4xl leading-loose font-light">
            <tr className="text-xl text-gray-500">
                <th align="left">日付</th>
                <th align="left">食材</th>
                <th align="left">外食</th>
                <th align="left">合計</th>
            </tr>
            <React.Fragment className="flex w-screen">
              {expences.map((expence) => {
                return (
                  <tr className="border-t-2">
                    <td type="date">{ expence.date }</td>
                    <td>¥ { expence.shopping }</td>
                    <td>¥ { expence.eatout}</td>
                    <td>¥ { expence.sum}</td>
                  </tr>
                )
              })}
            </React.Fragment>
          </table>
          </div>
        </div>
      </div>
    </>
  );
}

export default Expences;
