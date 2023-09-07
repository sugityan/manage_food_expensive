import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // useNavigateをインポート
import Header from "../components/header";
import Sidebar from "../components/sidebar";
import { InformationCircleIcon } from "@heroicons/react/24/outline";
import {
  Button,
  Card,
  Input,
  List,
  ListItem,
  Popover,
  PopoverContent,
  PopoverHandler,
  Progress,
  Tooltip,
  Typography,
} from "@material-tailwind/react";
import axios from "axios";

const convertCategory = [
  "その他",
  "野菜",
  "肉",
  "魚",
  "穀物",
  "調味料",
  "加工食品",
  "飲料水",
];

const FoodListHeader = () => {
  return (
    <ListItem className="bg-gray-100">
      <div className="flex items-center w-full">
        <div className="w-1/6 font-bold text-center">商品名</div>
        <div className="w-1/6 font-bold text-center">カテゴリ</div>
        <div className="w-1/6 font-bold text-center">購入日</div>
        <div className="w-1/6 font-bold text-center">賞味期限</div>
        <div className="w-1/6 font-bold text-center">価格</div>
        <div className="w-1/6 font-bold text-center">数量</div>
        <div className="w-1/12 mr-5 font-bold text-center">メモ</div>
        <div className="w-2/5 font-bold text-center">残量</div>
      </div>
    </ListItem>
  );
};

const FoodListItem = ({ food }) => {
  const navigate = useNavigate(); // useNavigateを使用して、navigate関数を取得

  const handleItemClick = () => {
    navigate("/gradientChange", { state: { food } }); // navigate関数を使用して、ページ遷移を行う
  };

  return (
    <ListItem onClick={handleItemClick} className="cursor-pointer">
      <div className="flex items-center w-full">
        <div className="w-1/6 text-center">{food.name}</div>
        <div className="w-1/6 text-center">
          {convertCategory[food.category]}
        </div>
        <div className="w-1/6 text-center">{food.Date}</div>
        <div className="w-1/6 text-center">{food.expiry_date}</div>
        <div className="w-1/6 text-center">￥{food.price}</div>
        <div className="w-1/6 text-center">
          {food.amount}
          {food.unit}
        </div>
        <div className="w-1/12 mr-5 flex justify-center items-center">
          <Tooltip
            placement="bottom"
            className="border border-blue-gray-50 bg-white px-4 py-3 shadow-xl shadow-black/10 "
            content={
              <div className="w-80">
                <Typography
                  variant="small"
                  color="blue-gray"
                  className="font-normal opacity-80"
                >
                  {food.memo}
                </Typography>
              </div>
            }
          >
            <InformationCircleIcon className="h-4 w-4 text-center" />
          </Tooltip>
        </div>
        <div className="w-2/5 flex justify-between items-center">
          <div className="w-full">
            <div className="mb-2 flex items-center justify-between gap-4">
              <Typography color="blue-gray" variant="h6">
                残量
              </Typography>
              <Typography color="blue-gray" variant="h6">
                {food.Remaining}%
              </Typography>
            </div>
            <Progress value={food.Remaining} max={100} />
          </div>
          <Popover placement="bottom">
            <PopoverHandler>
              <Button className="w-40 ml-10">残量設定</Button>
            </PopoverHandler>
            {/* 残量の変更をする部分 */}
            <PopoverContent className="w-96">
              <Typography variant="h6" color="blue-gray" className="mb-6">
                残量を設定してください
              </Typography>
              <div className="flex gap-2">
                <Input label="残量(%)" type="number" />
                <Button variant="gradient">OK</Button>
              </div>
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </ListItem>
  );
};

const FoodList = () => {
  const [foodListData, setFoodListData] = useState(null);

  const baseUrl = "http://127.0.0.1:8000";
  useEffect(() => {
    const fetchFoodList = async () => {
      try {
        const response = await axios.get(baseUrl + "/food_db", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log(response);
        if (response.status === 200) {
          console.log(response.data);
          setFoodListData(response.data);
        } else {
          console.log("バックエンドからのエラー");
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchFoodList();
  }, []);

  useEffect(() => {
    console.log(foodListData);
  }, [foodListData]);

  return (
    <>
      <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="w-full">
          <Card>
            <List>
              <FoodListHeader />
              {foodListData &&
                Object.values(foodListData).map((food, index) => (
                  <FoodListItem key={index} food={food} />
                ))}
            </List>
          </Card>
        </div>
      </div>
    </>
  );
};

export default FoodList;
