import React from "react";
import RecentContent from "./RecentContent";
import { TrendingUp } from "lucide-react";

const PopularContent = () => {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <div className="flex items-center mb-4">
        <TrendingUp className="w-5 h-5 mr-2 text-netflix-red" />
        <h2 className="text-xl font-semibold dark:text-white">
          Recent Content
        </h2>
      </div>
      <div className="flex flex-col md:flex-row gap-6">
        <RecentContent title="Movies" endpoint="movies" icon="movie" />
        <RecentContent title="TV Shows" endpoint="series" icon="tv" />
      </div>
    </div>
  );
};

export default PopularContent;
