import { Monitor } from "lucide-react";
import React from "react";
import ThemeToggle from "./theme-toggle";

const Header = () => {
  return (
    <header className="bg-netflix-red p-4 text-white shadow-lg">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <Monitor className="w-8 h-8 mr-2" />
          <h1 className="text-3xl font-bold">Streamlytics</h1>
        </div>
        <ThemeToggle />
      </div>
    </header>
  );
};

export default Header;
