import { Monitor } from "lucide-react";
import React from "react";
import ThemeToggle from "./theme-toggle";
import Link from "next/link";

const Header = () => {
  return (
    <header className="bg-netflix-red p-4 text-white shadow-lg">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <Monitor className="w-8 h-8 mr-2" />
          <Link href="/">
            <h1 className="text-3xl font-bold">Streamlytics</h1>{" "}
          </Link>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/">Movies</Link>
          <Link href="tv">TV Show</Link>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
