import React, { useState } from "react";

import {
  Card,
  Typography,
  List,
  ListItem,
  Chip,
  Badge,
  IconButton,
} from "@material-tailwind/react";
import {
  ChevronDoubleRightIcon,
  ChevronDoubleLeftIcon,
} from "@heroicons/react/24/solid";

const Sidebar = () => {
  const [showSidebar, setShowSidebar] = useState(false);

  // ボタンを押すとshowSidebarの値が反転する
  const handleToggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  const foodList = [
    { name: "トマト", color: "red", days: "期限切れ" },
    { name: "キャベツ", color: "yellow", days: "1日" },
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
          <Badge>
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
            <ListItem
              key={index}
              disabled={food.color !== "red"}
              className={food.color === "red" ? "cursor-pointer" : ""}
              onClick={() => {
                if (food.color === "red") {
                  // red food item clicked
                }
              }}
            >
              <Typography>{food.name}</Typography>
              <Chip
                value={food.days}
                size="sm"
                color={food.color}
                className="ml-auto"
              />
            </ListItem>
          ))}
        </List>
      )}
    </Card>
  );
};

export default Sidebar;
