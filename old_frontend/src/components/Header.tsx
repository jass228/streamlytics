"use client";
import React from "react";
import { Moon, PlayCircle, Sun } from "lucide-react";
import { useTheme } from "@/context/ThemeContext";

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className="bg-netflix-red text-white p-4 shadow-lg">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <PlayCircle className="w-8 h-8 mr-2" />
          <h1 className="text-2xl font-bold">Streamlytics</h1>
        </div>
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-red-700 transition-colors duration-200"
          aria-label={
            theme == "dark" ? "Light mode active" : "Dark mode active"
          }
        >
          {theme === "dark" ? (
            <Sun className="w-6 h-6" />
          ) : (
            <Moon className="w-6 h-6" />
          )}
        </button>
      </div>
    </header>
  );
};

export default Header;
