"use client";
import {
  fetchMovieGenreDistribution,
  fetchSerieGenreDistribution,
} from "@/lib/api";
import { APIDistributionResponse } from "@/types/api";
import React, { useEffect, useState } from "react";
import PieVisualization from "./PieVisualization";

/*const data = [
  { name: "Action", value: 789 },
  { name: "Drame", value: 1234 },
  { name: "Comédie", value: 987 },
  { name: "Documentaire", value: 456 },
  { name: "Thriller", value: 678 },
];

const COLORS = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];*/

interface GenreDistributionProps {
  media: string;
}

const GenreDistribution = ({ media }: GenreDistributionProps) => {
  //const { theme } = useTheme();
  const [movieData, setMovieData] = useState<APIDistributionResponse | null>(
    null
  );
  const [serieData, setSerieData] = useState<APIDistributionResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [movies, series] = await Promise.all([
        fetchMovieGenreDistribution(),
        fetchSerieGenreDistribution(),
      ]);
      setMovieData(movies);
      setSerieData(series);
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

  // Transform movies data
  const movieChartData = Object.entries(movieData.data)
    .map(([genre, value]) => ({
      name: genre,
      value,
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 5); // Limit to the first 8 genres for readability

  // Transform tv show data
  const seriesChartData = serieData
    ? Object.entries(serieData.data)
        .map(([genre, value]) => ({
          name: genre,
          value,
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 5)
    : [];

  return (
    <div className="w-full h-[300px]">
      {media === "movie" ? (
        <PieVisualization data={movieChartData} />
      ) : (
        <PieVisualization data={seriesChartData} />
      )}
    </div>
  );
};

export default GenreDistribution;
