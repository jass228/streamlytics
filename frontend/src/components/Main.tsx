import React from "react";
import GenreDistribution from "./charts/GenreDistribution";
import CardContent from "./CardContent";
import YearlyTrends from "./charts/YearlyTrends";
import GenreRating from "./charts/GenreRating";
import LanguageMap from "./charts/LanguageMap";
import TopContent from "./TopContent";

const Main = () => {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <CardContent title="Genres Distribution">
          <GenreDistribution />
        </CardContent>
        <CardContent title="Annual trends">
          <YearlyTrends />
        </CardContent>
        <CardContent title="Rating by genre">
          <GenreRating />
        </CardContent>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <CardContent title="Languages Distribution">
          <LanguageMap />
        </CardContent>
        <CardContent title="Top Movies and Series">
          <TopContent />
        </CardContent>
      </div>
    </div>
  );
};

export default Main;
