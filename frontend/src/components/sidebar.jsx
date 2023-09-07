import React, { useState, useEffect } from "react";
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
  const [remain, setRemain] = useState("");
  const [foodList, setFoodList] = useState(null);
  const baseUrl = "http://127.0.0.1:8000";

  const handleToggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  const handleRegisterInput = async (food) => {
    try {
      console.log("HERE");
      console.log(remain);
      const response = await axios.put(
        baseUrl + `/alert_food_fix`,
        // baseUrl + `/food_db_new`,
        {
          FoodID: food.foodID,
          remaining: remain,
          status: 1,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      console.log(response);

      if (response.status === 200) {
        console.log("記録完了");
        setRemain(response.data["remaining"]);
      } else {
        console.log("バックエンドからエラーが帰ってきてるよ");
      }
    } catch (error) {
      console.log("food:" + food.foodID);
      console.log("remain:" + remain);
      console.log("通信失敗");
    }
  };

  const handleDiscard = async (food) => {
    try {
      const response = await axios.put(
        baseUrl + `/alert_food_fix`,
        {
          FoodID: food.foodID,
          remaining: food.Remaining,
          status: 0,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      console.log(response);
      if (response.status === 200) {
        console.log("廃棄・使い切り完了");
        window.location.reload();
        setRemain();
      } else {
        console.log("バックエンドからエラーが帰ってきてるよ");
      }
    } catch (error) {
      console.log("通信失敗");
      console.error(error);
    }
  };

  useEffect(() => {
    const fetchAlertFoods = async () => {
      try {
        const response = await axios.get(baseUrl + "/get_alert_foods", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log("sidebarのget_food_listのレスポンス");
        console.log(response);
        if (response.status === 200) {
          console.log("通信成功");
          console.log(response.data);
          setFoodList(response.data);
        } else {
          console.log("バックエンドからのエラー");
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchAlertFoods();
  }, []);

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
          <IconButton>
            {showSidebar ? (
              <ChevronDoubleLeftIcon className="h-4 w-4" />
            ) : (
              <ChevronDoubleRightIcon className="h-4 w-4" />
            )}
          </IconButton>
        </div>
      </div>
      {showSidebar && (
        <List>
          {foodList ? (
            foodList.map((food, index) => (
              <Popover key={index} placement="right">
                <PopoverHandler>
                  <ListItem
                    disabled={food.Remaining_days === "期限切れ" ? false : true}
                  >
                    <Typography>{food.name}</Typography>
                    <Chip
                      value={food.Remaining_days}
                      size="sm"
                      color={
                        food.Remaining_days === "期限切れ"
                          ? "red"
                          : food.Remaining_days === "今日中"
                          ? "yellow"
                          : "blue"
                      }
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
                      <Input
                        // label={`記録されている残量：${food.Remaining}%`}
                        label={`残量を入力してください`}
                        type="number"
                        value={remain}
                        onChange={(event) => setRemain(event.target.value)}
                      />
                      <Button
                        variant="gradient"
                        size="sm"
                        onClick={() => handleRegisterInput(food)}
                      >
                        記録
                      </Button>
                      <Button
                        variant="gradient"
                        size="sm"
                        onClick={() => handleDiscard(food)}
                      >
                        捨てる
                      </Button>
                    </div>
                  </>
                </PopoverContent>
              </Popover>
            ))
          ) : (
            <Typography>Loading...</Typography>
          )}
        </List>
      )}
    </Card>
  );
};

export default Sidebar;
