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

const Sidebar = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  const [showPopoverInput, setShowPopoverInput] = useState(true);

  const handleToggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  const registerPopoverInput = () => {
    setShowPopoverInput(!showPopoverInput);
  };

  // データベースから取得
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
          {/* chromeで出るエラーはもともとのバグっぽい。無視しても正常に動く */}
          {/* もし期限切れがあればbadgeを表示 */}
          <Badge
            overlap="circular"
            invisible="true
          "
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
                  disabled={food.color !== "red"}
                  className={food.color === "red" ? "cursor-pointer" : ""}
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
                {showPopoverInput ? (
                  <>
                    <Typography variant="h6" color="blue-gray" className="mb-6">
                      どれだけ使えた？
                    </Typography>
                    <div className="flex gap-2">
                      <Input label="残量(%)" type="number" />
                      <Button
                        variant="gradient"
                        onClick={() => registerPopoverInput()}
                      >
                        OK
                      </Button>
                    </div>
                  </>
                ) : (
                  <Typography>登録完了</Typography>
                )}
              </PopoverContent>
            </Popover>
          ))}
        </List>
      )}
    </Card>
  );
};

export default Sidebar;
