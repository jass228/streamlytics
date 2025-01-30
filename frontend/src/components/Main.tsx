import React from "react";
import PopularContent from "./PopularContent";

const Main = () => {
  return (
    <main className="container mx-auto py-8 px-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PopularContent />
      </div>
    </main>
  );
};

export default Main;
