import React from "react";
import Header from "../components/header";
import Sidebar from "../components/sidebar";
import {
  Card,
  List,
  ListItem,
  Progress,
  Typography,
} from "@material-tailwind/react";

const FoodList = () => {
  const foodList = [
    {
      name: "トマト",
      category: "野菜",
      purchaseDate: "2023/01/01",
      expiredDate: "2023/01/01",
      price: 100,
      quantity: 1,
      unit: "個",
      memo: "おいしいらしい",
      stock: 80,
    },
    {
      name: "キャベツ",
      category: "野菜",
      purchaseDate: "2023/01/02",
      expiredDate: "2023/01/02",
      price: 200,
      quantity: 2,
      unit: "玉",
      memo: "甘くておいしい",
      stock: 30,
    },
    {
      name: "レタス",
      category: "野菜",
      purchaseDate: "2023/01/03",
      expiredDate: "2023/01/03",
      price: 150,
      quantity: 1,
      unit: "個",
      memo: "シャキシャキしている",
      stock: 40,
    },
  ];

  return (
    <>
      <Header />
      <div className="flex h-screen">
        <Sidebar />
        <div className="w-full">
          <Card>
            <List>
              <ListItem className="bg-gray-100">
                <div className="flex items-center w-full">
                  <div className="w-1/6 font-bold text-center">商品名</div>
                  <div className="w-1/6 font-bold text-center">カテゴリ</div>
                  <div className="w-1/6 font-bold text-center">購入日</div>
                  <div className="w-1/6 font-bold text-center">賞味期限</div>
                  <div className="w-1/6 font-bold text-center">価格</div>
                  <div className="w-1/6 font-bold text-center">数量</div>
                  <div className="w-full font-bold text-center">残量</div>
                </div>
              </ListItem>
              {foodList.map((food, index) => (
                <a href="#" className="text-initial" key={index}>
                  <ListItem>
                    <div className="flex items-center w-full">
                      <div className="w-1/6 text-center">{food.name}</div>
                      <div className="w-1/6 text-center">{food.category}</div>
                      <div className="w-1/6 text-center">
                        {food.purchaseDate}
                      </div>
                      <div className="w-1/6 text-center">
                        {food.expiredDate}
                      </div>
                      <div className="w-1/6 text-center">￥{food.price}</div>
                      <div className="w-1/6 text-center">
                        {food.quantity}
                        {food.unit}
                      </div>
                      <div className="w-full">
                        <div className="mb-2 flex items-center justify-between gap-4">
                          <Typography color="blue-gray" variant="h6">
                            残量
                          </Typography>
                          <Typography color="blue-gray" variant="h6">
                            {food.stock}%
                          </Typography>
                        </div>
                        <Progress value={food.stock} max={100} />
                      </div>
                    </div>
                  </ListItem>
                </a>
              ))}
            </List>
          </Card>
        </div>
      </div>
    </>
  );
};

export default FoodList;
