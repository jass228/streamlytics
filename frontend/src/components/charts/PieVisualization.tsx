"use clients";
import { useTheme } from "next-themes";
import React from "react";
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const COLORS = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];

interface ChartDataItem {
  name: string;
  value: number;
}

interface PieVisualizationProps {
  data: ChartDataItem[];
}

const PieVisualization = ({ data }: PieVisualizationProps) => {
  const { theme } = useTheme();
  const tooltipStyle = {
    backgroundColor: theme === "dark" ? "hsl(var(--background))" : "white",
    border: "1px solid hsl(var(--border))",
    borderRadius: "var(--radius)",
  };
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={tooltipStyle}
          itemStyle={{
            color: theme === "dark" ? "white" : "black",
          }}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default PieVisualization;
