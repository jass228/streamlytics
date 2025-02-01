import Footer from "@/components/Footer";
import Header from "@/components/Header";
import Main from "@/components/Main";
import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#ffe3dd] dark:bg-background dark:text-white transition-colors duration-200">
      <Header />
      <Main />
      <Footer />
    </div>
  );
}
