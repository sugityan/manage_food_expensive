import React from "react";
import Header from "../components/header";
import Sidebar from "../components/sidebar";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  XAxis,
  YAxis,
} from "recharts";
import { Tooltip, Typography } from "@material-tailwind/react";

const foodcostRanking = "500";
const foodcost = 6000;
const foodlossData = [
  { name: "0", number: 4000 },
  { name: "500", number: 3000 },
  { name: "1000", number: 2000 },
  { name: "2000", number: 1000 },
  { name: "3000", number: 290 },
  { name: "4000", number: 20 },
  { name: "5000", number: 1 },
];

const foodlossPosition = "1000";
const foodloss = 5000;
const foodcostData = [
  { name: "0", number: 1000 },
  { name: "500", number: 3000 },
  { name: "1000", number: 2000 },
  { name: "2000", number: 1000 },
  { name: "3000", number: 290 },
  { name: "4000", number: 20 },
  { name: "5000", number: 1 },
];

const Compare = () => {
  return (
    <>
      <Header />
      <div className="flex h-full w-full">
        <Sidebar />
        <div className="flex w-full">
          <div className="w-1/2 flex flex-col items-center justify-center">
            <div>
              <Typography variant="small">あなたのフードロス金額</Typography>
              <Typography variant="h1" className="mb-10 border-b-2">
                ￥{foodloss}
              </Typography>
            </div>
            <Typography variant="h3">同年代との比較</Typography>
            <BarChart
              width={500}
              height={300}
              data={foodlossData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="number">
                {foodlossData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      foodlossPosition === entry.name ? "#FF0000" : "#0088FE"
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </div>
          <div className="w-1/2 flex flex-col items-center justify-center">
            <div>
              <Typography variant="small">あなたの食費</Typography>
              <Typography variant="h1" className="mb-10 border-b-2">
                ￥{foodcost}
              </Typography>
            </div>
            <Typography variant="h3">同年代との比較</Typography>
            <BarChart
              width={500}
              height={300}
              data={foodcostData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="number">
                {foodcostData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      foodcostRanking === entry.name ? "#FF0000" : "#0088FE"
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </div>
        </div>
      </div>
    </>
  );
};

export default Compare;
