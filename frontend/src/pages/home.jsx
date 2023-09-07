import React from "react";

import Sidebar from "../components/sidebar";
import Header from "../components/header";
import ShowPiChart from "../components/showPiChart";
import { Typography, Button } from "@material-tailwind/react";

const Home = () => {
  console.log(localStorage.getItem("token"));
  const chartData = [
    { name: "Category A", value: 400 },
    { name: "Category B", value: 300 },
    { name: "Category C", value: 200 },
    { name: "Category D", value: 150 },
    { name: "Category E", value: 100 },
  ];

  const foodPrice = 10000;
  const foodLoss = 10000;

  return (
    <>
      <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="grid grid-cols-2 gap-4 w-full">
          <div className="flex flex-col items-center justify-center">
            <div className="flex">
              <div className="flex flex-col mr-10">
                <Typography variant="h3">今月の食費</Typography>
                <Typography variant="h1" className="mb-5">
                  ￥{foodPrice}
                </Typography>
              </div>
              <div className="flex flex-col ">
                <Typography variant="h3">今月のフードロス</Typography>
                <Typography variant="h1">￥{foodLoss}</Typography>
              </div>
            </div>
            <div className="flex gap-10">
              <a href="/eatoutRegistrate" className="mb-5">
                <Button>外食費登録へ</Button>
              </a>
              <a href="/gradientRegistrate">
                <Button>食材登録へ</Button>
              </a>
            </div>
          </div>
          <ShowPiChart data={chartData} title="食費" />
          <ShowPiChart data={chartData} title="残量率" />
          <ShowPiChart data={chartData} title="フードロス率" />
        </div>
      </div>
    </>
  );
};

export default Home;
