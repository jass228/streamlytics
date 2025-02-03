"use client";
import { fetchMovieRatings, fetchSerieRatings } from "@/lib/api";
import { APIRatingResponse } from "@/types/api";
import { useTheme } from "next-themes";
import React, { useEffect, useState } from "react";
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

/*const data = [
  { genre: "Action", rating: 7.2 },
  { genre: "Drame", rating: 7.8 },
  { genre: "Comédie", rating: 6.9 },
  { genre: "Documentaire", rating: 8.1 },
  { genre: "Thriller", rating: 7.5 },
];*/

interface GenreRatingProps {
  media: string;
}

const GenreRating = ({ media }: GenreRatingProps) => {
  const { theme } = useTheme();
  const [movieData, setMovieData] = useState<APIRatingResponse | null>(null);
  const [seriesData, setSeriesData] = useState<APIRatingResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [movies, series] = await Promise.all([
        fetchMovieRatings(),
        fetchSerieRatings(),
      ]);
      setMovieData(movies);
      setSeriesData(series);
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (isLoading || !movieData) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        Loading...
      </div>
    );
  }

  const formatData = (data: APIRatingResponse) => {
    return Object.entries(data.data)
      .map(([country, stats]) => ({
        country,
        rating: Number(stats.mean.toFixed(2)),
        count: stats.count,
      }))
      .sort((a, b) => b.rating - a.rating);
  };

  const movieRatings = formatData(movieData);
  const seriesRatings = seriesData ? formatData(seriesData) : [];

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={media === "movie" ? movieRatings : seriesRatings}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="country"
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
            labelFormatter={(label) => `${label}`}
            formatter={(value, name, item: any) => {
              const content = (
                <>
                  Rating: {value}
                  <br />
                  Count: {item.payload.count}
                </>
              );
              return [content];
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
