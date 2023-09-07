import React, { useState, useEffect } from "react";

import Sidebar from "../components/sidebar";
import Header from "../components/header";
import ShowPiChart from "../components/showPiChart";
import { Typography, Button } from "@material-tailwind/react";
import axios from "axios";


const Home = () => {
  const [dataDict, setDataDict] = useState({
    monthly_cost: 0,
    monthly_foodloss: 0,
    cost_graph: [],
    remain_graph: [],
    foodloss_graph: [],
  });

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
          <ShowPiChart data={dataDict.cost_graph} title="食費" />
          ) :
            <div style={{textAlign: 'center', color: 'red'}}>
            <h2 class="heading-016">今月の食費が登録されていません。食費を登録しよう！</h2>
            </div>}
          {ShowRemainGraph ? (
          <ShowPiChart data={dataDict.remain_graph} title="残量率" />
          ) : 
            <div style={{textAlign: 'center', color: 'red'}}>
            <h2 class="heading-016">残っている食材がありません。購入した食材を登録しよう！</h2>
            </div>}
          {ShowFoodlossGraph ? (
          <ShowPiChart data={dataDict.foodloss_graph} title="フードロス率" />
          ) :
            <div style={{textAlign: 'center', color: 'red'}}>
            <h2 class="heading-016">今月のフードロスはありません。この調子！</h2>
            </div>}
        </div>
      </div>
    </>
  );
};

export default Home;