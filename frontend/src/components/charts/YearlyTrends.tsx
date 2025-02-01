"use client";
import { useTheme } from "next-themes";
import React from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { year: "2018", films: 1200, series: 450 },
  { year: "2019", films: 1500, series: 600 },
  { year: "2020", films: 2000, series: 800 },
  { year: "2021", films: 2400, series: 1000 },
  { year: "2022", films: 2800, series: 1200 },
  { year: "2023", films: 3200, series: 1400 },
];

const YearlyTrends = () => {
  const { theme } = useTheme();
  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="year"
            padding={{ left: 0, right: 0 }}
            tick={{ fill: theme === "dark" ? "#fff" : "#000" }}
          />
          <YAxis
            padding={{ top: 20, bottom: 20 }}
            tick={{ fill: theme === "dark" ? "#fff" : "#000" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor:
                theme === "dark" ? "hsl(var(--background))" : "white",
              border: "1px solid hsl(var(--border))",
              borderRadius: "var(--radius)",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="films"
            stroke="hsl(var(--chart-1))"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="series"
            stroke="hsl(var(--chart-2))"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default YearlyTrends;
