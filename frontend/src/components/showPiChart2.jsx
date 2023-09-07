import { Typography } from "@material-tailwind/react";
import React from "react";
import { PieChart, Pie, Cell, Label, Legend, Tooltip } from "recharts";

const ShowPiChart2 = ({ data, title }) => {
  const COLORS = ["#808080", "#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#F5FFFA", "9370DB", "008080", "#DC143C"];
  const Category = ["肉類・魚介類・卵", "野菜", "果物", "穀類", "乳製品", "調味料", "飲料", "その他", "外食"];
  const label = ({ cost }) => {
    return `${cost}%`;
  };
  return (
    <div className="flex flex-col justify-center items-center">
      <Typography variant="h5">{title}</Typography>
      <PieChart width={400} height={300}>
        <Pie
          dataKey="cost"
          isAnimationActive={true}
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={80}
          fill="#8884d8"
          label={label}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.category % COLORS.length]} />
          ))}
          <Label
            valueKey="cost"
            position="center"
            content={({ value }) => `${value}円`}
          />
        </Pie>
        <Legend
          payload={data.map((entry, index) => ({
            value: Category[entry.category % Category.length],
            type: 'circle',
            color: COLORS[entry.category % COLORS.length], // カスタムカラー
          }))}
        />
        <Tooltip formatter={(value) => [`${value}%`]} />
      </PieChart>
    </div>
  );
};

export default ShowPiChart2;
