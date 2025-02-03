import React from "react";
import CardContent from "./CardContent";
import GenreDistribution from "./charts/GenreDistribution";
import YearlyTrends from "./charts/YearlyTrends";
import GenreRating from "./charts/GenreRating";
import LanguageMap from "./charts/LanguageMap";
import PopularContent from "./PopularContent";
import { Tv2 } from "lucide-react";

const MainTv = () => {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex items-center mb-4">
        <Tv2 className="w-5 h-5 mr-2 text-red-600" />
        <h2 className="text-xl font-semibold dark:text-white">TV Shows</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <CardContent title="Genres Distribution">
          <GenreDistribution media="tv" />
        </CardContent>
        <CardContent title="Annual trends">
          <YearlyTrends media="tv" />
        </CardContent>
        <CardContent title="Rating by genre">
          <GenreRating media="tv" />
        </CardContent>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <CardContent title="Languages Distribution">
          <LanguageMap media="tv" />
        </CardContent>
        <CardContent title=" Recent Content">
          <PopularContent media="tv" />
        </CardContent>
      </div>
    </div>
  );
};

export default MainTv;
