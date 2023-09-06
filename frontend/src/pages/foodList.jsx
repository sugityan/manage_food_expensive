import React, { useState } from "react";
import Header from "../components/header";
import Sidebar from "../components/sidebar";
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
  Typography,
} from "@material-tailwind/react";

const FoodList = () => {
  const [registerPopoverInput, setRegisterPopoverInput] = useState(true);

  //   ここで残量が変更された時の処理(未実装)
  const handleRegisterPopoverInput = () => {
    setRegisterPopoverInput(!registerPopoverInput);
  };

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
              {/* 一番上の行 */}
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
              {/* 実際にデータを表示 */}
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
                      <div className="w-full flex justify-between items-center">
                        <div className="w-full">
                          <div className="mb-2 flex items-center justify-between gap-4">
                            {console.log("rendering")}
                            <Typography color="blue-gray" variant="h6">
                              残量
                            </Typography>
                            <Typography color="blue-gray" variant="h6">
                              {food.stock}%
                            </Typography>
                          </div>
                          <Progress value={food.stock} max={100} />
                        </div>
                        <Popover placement="bottom">
                          <PopoverHandler>
                            <Button className="w-40 ml-10">残量設定</Button>
                          </PopoverHandler>
                          {/* 残量の変更をする部分 */}
                          <PopoverContent className="w-96">
                            <Typography
                              variant="h6"
                              color="blue-gray"
                              className="mb-6"
                            >
                              残量を設定してください
                            </Typography>
                            <div className="flex gap-2">
                              <Input label="残量(%)" type="number" />
                              <Button
                                variant="gradient"
                                onClick={() => handleRegisterPopoverInput()}
                              >
                                OK
                              </Button>
                            </div>
                          </PopoverContent>
                        </Popover>
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
