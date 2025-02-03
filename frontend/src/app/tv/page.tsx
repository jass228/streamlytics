import Footer from "@/components/Footer";
import Header from "@/components/Header";
import MainTv from "@/components/MainTv";
import React from "react";

const TvDashboard = () => {
  return (
    <div className="min-h-screen bg-[#ffe3dd] dark:bg-background dark:text-white transition-colors duration-200">
      <Header />
      <MainTv />
      <Footer />
    </div>
  );
};

export default TvDashboard;
