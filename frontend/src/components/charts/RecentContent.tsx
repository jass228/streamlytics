"use client";
import React, { useEffect, useState } from "react";
import { API_ENDPOINTS } from "@/config/api";
import { StreamlyticsContent } from "@/types/api";

interface RawContentItem {
  genre: string | string[];
  tmdb_id: number;
  poster_path: string;
  title: string;
  release_date?: string;
  first_air_date?: string;
  rating: number;
  original_language: string;
}

interface RecentContentProps {
  endpoint: string;
}

const RecentContent = ({ endpoint }: RecentContentProps) => {
  const [netflixData, setNetflixData] = useState<StreamlyticsContent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Get data
  const getData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_ENDPOINTS}/${endpoint}`);
      if (!response.ok) throw new Error("Failed to get data");

      const data = await response.json();

      // Transform the data to match our interface
      const validatedData = data
        .map((item: RawContentItem) => ({
          ...item,
          genre:
            typeof item.genre === "string"
              ? item.genre.split(",").map((g) => g.trim())
              : [],
        }))
        .sort((a: StreamlyticsContent, b: StreamlyticsContent) => {
          const dateA = new Date(
            a.release_date || a.first_air_date || ""
          ).getTime();
          const dateB = new Date(
            b.release_date || b.first_air_date || ""
          ).getTime();
          return dateB - dateA;
        });

      setNetflixData(validatedData);
    } catch (error) {
      console.error("Failed to load data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        Loading...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {netflixData.slice(0, 5).map((content, idx) => (
        <div
          key={content.tmdb_id}
          className={`flex items-center space-x-4 ${
            idx !== 4 ? "border-b dark:border-gray-700" : ""
          }' pb-2`}
        >
          <img
            src={`https://image.tmdb.org/t/p/w92${content.poster_path}`}
            alt={content.title}
            className="w-16 h-24 object-cover rounded"
          />
          <div className="flex-grow">
            <h3 className="font-medium dark:text-white">{content.title}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {new Date(
                content.release_date || content.first_air_date || ""
              ).getFullYear()}{" "}
              • {content.rating}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500">
              {content.genre.slice(0, 2).join(", ")}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {content.original_language.toUpperCase()}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RecentContent;
