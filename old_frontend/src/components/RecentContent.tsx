"use client";
import React, { useEffect, useState } from "react";
import { API_ENDPOINT } from "@/config/api";
import { StreamlyticsContent } from "@/type/api";
import { Film, Tv2 } from "lucide-react";

interface RecentContentProps {
  title: string;
  endpoint: string;
  icon: "movie" | "tv";
}

const RecentContent = ({ title, endpoint, icon }: RecentContentProps) => {
  const [netflixData, setNetflixData] = useState<StreamlyticsContent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Get data
  const getData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_ENDPOINT}/${endpoint}`);
      if (!response.ok) throw new Error("Failed to get data");

      const data = await response.json();

      // Transform the data to match our interface
      const validatedData = data
        .map((item: any) => ({
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

  return (
    <div className="space-y-4">
      <div className="flex items-center mb-4">
        {icon === "movie" ? (
          <Film className="w-5 h-5 mr-2 text-red-600" />
        ) : (
          <Tv2 className="w-5 h-5 mr-2 text-red-600" />
        )}
        <h2 className="text-xl font-semibold dark:text-white">{title}</h2>
      </div>
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
