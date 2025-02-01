"use client";
import { useTheme } from "next-themes";
import React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { genre: "Action", rating: 7.2 },
  { genre: "Drame", rating: 7.8 },
  { genre: "Comédie", rating: 6.9 },
  { genre: "Documentaire", rating: 8.1 },
  { genre: "Thriller", rating: 7.5 },
];

const GenreRating = () => {
  const { theme } = useTheme();
  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="genre"
            padding={{ left: 0, right: 0 }}
            tick={{ fill: theme === "dark" ? "#fff" : "#000" }}
          />
          <YAxis
            domain={[0, 10]}
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
          <Bar dataKey="rating" fill="hsl(var(--chart-1))" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GenreRating;
