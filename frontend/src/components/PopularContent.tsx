import React from "react";
import RecentContent from "./charts/RecentContent";

interface PopularContentProps {
  media: string;
}

const PopularContent = ({ media }: PopularContentProps) => {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <div className="flex flex-col md:flex-row">
        {media === "movie" ? (
          <RecentContent endpoint="movies" />
        ) : (
          <RecentContent endpoint="series" />
        )}
      </div>
    </div>
  );
};

export default PopularContent;
