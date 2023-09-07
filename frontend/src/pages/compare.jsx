import React, { useState, useEffect } from "react";
import axios from "axios";
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


const Compare = () => {
  const [foodcostRanking, setFoodcostRanking] = useState("~3万円");
  const [foodcost, setFoodcost] = useState(5000);
  const [foodcostData, setFoodcostData] = useState([
    {
      "name": "~3万円",
      "number": 0
    },
    {
      "name": "3~4万円",
      "number": 0
    },
    {
      "name": "4~5万円",
      "number": 0
    },
    {
      "name": "5~6万円",
      "number": 0
    },
    {
      "name": "6~8万円",
      "number": 0
    },
    {
      "name": "8~10万円",
      "number": 0
    },
    {
      "name": "10万円~",
      "number": 0
    }
  ]);
  const [foodlossPosition, setFoodlossPosition] = useState("~千円");
  const [foodloss, setFoodloss] = useState(500);
  const [foodlossData, setFoodlossData] = useState([
    {
      "name": "~千円",
      "number": 0
    },
    {
      "name": "1~2千円",
      "number": 0
    },
    {
      "name": "2~3千円",
      "number": 0
    },
    {
      "name": "3~5千円",
      "number": 0
    },
    {
      "name": "5~7千円",
      "number": 0
    },
    {
      "name": "7千~1万円",
      "number": 0
    },
    {
      "name": "1万円~",
      "number": 0
    }
  ]);
  const baseUrl = "http://127.0.0.1:8000";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(baseUrl + "/compare_cost", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const data = response.data;
        console.log(data);

        setFoodcostRanking(data.foodcostRanking);
        setFoodcost(data.foodcost);
        setFoodlossData(data.foodlossData);
        setFoodlossPosition(data.foodlossPosition);
        setFoodloss(data.foodloss);
        setFoodcostData(data.foodcostData);
      } catch (error) {
        console.error("Error fetching the data", error);
      }
    };

    fetchData();
  }, []);

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
                right: 10,
                left: 10,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fontSize: '12px' }} interval={0}/>
              <YAxis />
              <Tooltip />
              <Bar dataKey="number" barSize={30}>
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
              <XAxis dataKey="name" tick={{ fontSize: '12px' }} interval={0}/>
              <YAxis />
              <Tooltip />
              <Bar dataKey="number"barSize={30}>
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