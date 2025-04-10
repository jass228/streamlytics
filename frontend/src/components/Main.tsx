import React from "react";
import GenreDistribution from "./charts/GenreDistribution";
import CardContent from "./CardContent";
import YearlyTrends from "./charts/YearlyTrends";
import GenreRating from "./charts/GenreRating";
import LanguageMap from "./charts/LanguageMap";
import { Film } from "lucide-react";
import PopularContent from "./PopularContent";

const Main = () => {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex items-center mb-4">
        <Film className="w-5 h-5 mr-2 text-red-600" />
        <h2 className="text-xl font-semibold dark:text-white">Movies</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <CardContent title="Genres Distribution">
          <GenreDistribution media="movie" />
        </CardContent>
        <CardContent title="Annual trends">
          <YearlyTrends media="movie" />
        </CardContent>
        <CardContent title="Rating by genre">
          <GenreRating media="movie" />
        </CardContent>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <CardContent title="Languages Distribution">
          <LanguageMap media="movie" />
        </CardContent>
        <CardContent title="Recent Content">
          <PopularContent media="movie" />
        </CardContent>
      </div>
    </div>
  );
};

export default Main;
