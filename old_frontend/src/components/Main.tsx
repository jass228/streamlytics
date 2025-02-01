import React from "react";
import PopularContent from "./PopularContent";
import GenreDistribution from "./GenreDistribution";

const Main = () => {
  return (
    <main className="container mx-auto py-8 px-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PopularContent />
        <GenreDistribution />
      </div>
    </main>
  );
};

export default Main;
