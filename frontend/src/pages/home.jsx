import React, { useState, useEffect } from "react";

import Sidebar from "../components/sidebar";
import Header from "../components/header";
import ShowPiChart from "../components/showPiChart";
import ShowPiChart2 from "../components/showPiChart2";
import { Typography, Button } from "@material-tailwind/react";
import axios from "axios";
import { useNavigate } from "react-router-dom";


const Home = () => {
  const [dataDict, setDataDict] = useState({
    monthly_cost: 0,
    monthly_foodloss: 0,
    cost_graph: [],
    remain_graph: [],
    foodloss_graph: [],
  });
  const navigate = useNavigate();

  const baseUrl = "http://127.0.0.1:8000";

  useEffect(() => {
    const fetchAlertFoods = async () => {
      try {
        const response = await axios.get(baseUrl + "/graph_data", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log("sidebarのget_food_listのレスポンス");
        console.log(response);
        if (response.status === 200) {
          console.log("通信成功");
          console.log(response.data)
          setDataDict(response.data);
          console.log(dataDict.remain_graph)
        } else {
          console.log("バックエンドからのエラー");
        }
      } catch (error) {
        if (error.response.status === 401) {
          console.log("認証エラー");
          localStorage.removeItem("token");
          navigate("/login"); // /homeにリダイレクト
        }
        console.error(error);
      }
    };

    fetchAlertFoods();
  }, []);
  const ShowCostGraph = dataDict.cost_graph !== 0;
  const ShowRemainGraph = dataDict.remain_graph !== 0;
  const ShowFoodlossGraph = dataDict.foodloss_graph !== 0;

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
                  ￥{dataDict.monthly_cost}
                </Typography>
              </div>
              <div className="flex flex-col ">
                <Typography variant="h3">今月のフードロス</Typography>
                <Typography variant="h1">￥{dataDict.monthly_foodloss}</Typography>
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
          {ShowCostGraph ? (
          <ShowPiChart data={dataDict.cost_graph} title="食費(円)" />
          ) :
          <div className="flex justify-center items-center  ">
              <div className="text-center text-blue-600 p-5 border border-blue-500 bg-white rounded-xl shadow-md">
                  <h2 className="text-xl font-semibold mb-2">今月の食費が登録されていません。</h2>
                  <p className="text-sm">食費を登録しよう！</p>
              </div>
          </div>}

          {ShowRemainGraph ? (
          <ShowPiChart2 data={dataDict.remain_graph} title="残量率(%)" />
          ) : 
          <div className="flex justify-center items-center pb-20 ">
              <div className="text-center text-blue-600 p-5 border border-blue-500 bg-white rounded-xl shadow-md">
                  <h2 className="text-xl font-semibold mb-2">残っている食材がありません。</h2>
                  <p className="text-sm">購入した食材を登録しよう！</p>
              </div>
          </div>}

          {ShowFoodlossGraph ? (
          <ShowPiChart2 data={dataDict.foodloss_graph} title="フードロス率(%)" />
          ) :
          <div className="flex justify-center items-center pb-20 ">
              <div className="text-center text-blue-600 p-5 border border-blue-500 bg-white rounded-xl shadow-md">
                  <h2 className="text-xl font-semibold mb-2">今月のフードロスはありません。</h2>
                  <p className="text-sm">この調子！</p>
              </div>
          </div>}
        </div>
      </div>
    </>
  );
};

export default Home;