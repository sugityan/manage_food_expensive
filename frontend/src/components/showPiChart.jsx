import { Typography } from "@material-tailwind/react";
import React from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";

const ShowPiChart = ({ data, title }) => {
  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

  return (
    <div className="flex flex-col justify-center items-center">
      <Typography variant="h5">{title}</Typography>
      <PieChart width={400} height={300}>
        <Pie
          dataKey="cost"
          isAnimationActive={false}
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={80}
          fill="#8884d8"
          label
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default ShowPiChart;
