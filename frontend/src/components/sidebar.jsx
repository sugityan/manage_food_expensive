import React, { useState } from "react";

import {
  Card,
  Typography,
  List,
  ListItem,
  Chip,
  Badge,
  IconButton,
  Popover,
  PopoverContent,
  PopoverHandler,
  Button,
  Input,
} from "@material-tailwind/react";
import {
  ChevronDoubleRightIcon,
  ChevronDoubleLeftIcon,
} from "@heroicons/react/24/solid";
import axios from "axios";

const Sidebar = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  // 初期値はデータ取得の時に設定
  const [remain, setRemain] = useState(null)
  const [registerPopoverInput, setRegisterPopoverInput] = useState(true)
  const baseUrl = "http://127.0.0.1:8000";

  const handleToggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  // ポップオーバーの入力を処理
  // 記録を押したとき(残量変更のみ)
  // TODO: FOODIDの定義
  const handleRegisterInput = async (food) => {
    // apiにremainの内容をpostする処理
      try {
        const response = await axios.patch(baseUrl + `/food_db/${food.FoodID}`, {
          Remaining : remain,
          status: 1
        }, {
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          }
        });
        console.log(response);
        if (response.statusText === "OK") {
          // 記録成功
          console.log("記録完了");
          setRemain(null)
        } else {
          // apiからエラーが返ってくる
          console.log("バックエンドからエラーが帰ってきてるよ");
        }
      } catch (error) {
        console.log("通信失敗");
      }
  };

  // 捨てるボタンを押した場合
  const handleDiscardInput = async (food) => {
    // apiにremainの内容をpostする処理
    try {
      const response = await axios.patch(baseUrl + `/food_db/${food.FoodID}`, {
        Remaining : remain,
        status: 0
      }, {
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        }
      });
      console.log(response);
      if (response.statusText === "OK") {
        // 廃棄成功
        console.log("廃棄・使い切り完了");
        setRemain(null)
      } else {
        // apiからエラーが返ってくる
        console.log("バックエンドからエラーが帰ってきてるよ");
      }
    } catch (error) {
      console.log("通信失敗");
    }
  };

  // データベースから食材リストを取得
  const handleGetFoodList = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.get(baseUrl + "/get_alert_foods", {
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        }
      });
      console.log("sidebarのget_food_listのレスポンス");
      console.log(response);
      if (response.statusText === "OK") {
        foodList = response.data
      }
      
    } catch (error) {
      console.error(error);
    }
  };

  // データベースから取得
  const foodList = [
    { name: "トマト", color: "red", days: "期限切れ" },
    { name: "キャベツ", color: "red", days: "1日" },
    { name: "レタス", color: "blue", days: "2日" },
  ];

  return (
    <Card
      className={`h-screen p-4 shadow-xl shadow-blue-gray-900/5 ${
        showSidebar ? "" : "shadow-none"
      }`}
    >
      <div className="mb-2 p-4 flex items-center">
        {showSidebar && (
          <Typography variant="h5" color="blue-gray">
            Sidebar
          </Typography>
        )}
        <div
          className={showSidebar ? "ml-auto" : "mr-auto"}
          onClick={handleToggleSidebar}
        >
          {/* chromeで出るエラーはもともとのバグっぽい。無視しても正常に動く */}
          {/* もし期限切れがあればbadgeを表示 */}
          <Badge
            overlap="circular"
            invisible={true}
          >
            <IconButton>
              {showSidebar ? (
                <ChevronDoubleLeftIcon className="h-4 w-4" />
              ) : (
                <ChevronDoubleRightIcon className="h-4 w-4" />
              )}
            </IconButton>
          </Badge>
        </div>
      </div>
      {showSidebar && (
        <List>
          {foodList.map((food, index) => (
            // もし最終的な残量率が記録されていれば見えないようにする。
            // また、残量率が記録されていれば、その値を表示する。
            <Popover key={index} placement="right">
              <PopoverHandler>
                <ListItem
                  disabled={food.days === "期限切れ" ? true : false}
                  className={
                    food.days === "期限切れ"
                      ? "red"
                      : food.days === "今日中"
                      ? "yellow"
                      : "blue"
                  }
                >
                  <Typography>{food.name}</Typography>
                  <Chip
                    value={food.days}
                    size="sm"
                    color={food.color}
                    className="ml-auto"
                  />
                </ListItem>
              </PopoverHandler>
              <PopoverContent className="">
                
                  <>
                    <Typography variant="h6" color="blue-gray" className="mb-6">
                      残りどれくらい？
                    </Typography>
                    <div className="flex gap-2">
                      <Input label="残量(%)" type="number" onChange={(event)=>setRemain(event.target.value)} />
                      <Button
                        variant="gradient"
                        onClick={() => handleRegisterInput(food)}
                      >
                        記録
                      </Button>
                      <Button
                        variant="gradient"
                        onClick={() => handleDiscardInput(food)}
                      >
                        捨てる
                      </Button>
                    </div>
                  </>
              </PopoverContent>
            </Popover>
          ))}
        </List>
      )}
    </Card>
  );
};

export default Sidebar;
