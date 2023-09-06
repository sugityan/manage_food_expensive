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
        <div className="flex flex-col w-screen">
          <div className="mt-20 text-5xl">
            <h1>今月の食費　¥{sumOfExpence}</h1>
          </div>
          <div className="flex justify-center">
          <table className="w-4/5 mt-20 justify-center text-3xl leading-loose">
            <tr>
                <th align="left">日付</th>
                <th align="left">食材</th>
                <th align="left">外食</th>
                <th align="left">合計</th>
            </tr>
            <React.Fragment className="flex w-screen">
              {expences.map((expence) => {
                return (
                  <tr>
                    <td>{ expence.date }</td>
                    <td>¥{ expence.shopping }</td>
                    <td>¥{ expence.eatout}</td>
                    <td>¥{ expence.sum}</td>
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
