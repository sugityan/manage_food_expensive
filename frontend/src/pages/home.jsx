import React from "react";

import Sidebar from "../components/sidebar";
import Header from "../components/header";
import ShowPiChart from "../components/showPiChart";
import { Typography } from "@material-tailwind/react";

const Home = () => {
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
          <div className="flex flex-col justify-center items-center gap-2">
            <Typography variant="h3">今月の食費</Typography>
            <Typography variant="h1" className="mb-5">
              ￥{foodPrice}
            </Typography>
            <Typography variant="h3">今月のフードロス</Typography>
            <Typography variant="h1">￥{foodLoss}</Typography>
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
