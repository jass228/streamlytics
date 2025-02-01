import Header from "@/components/Header";
import Main from "@/components/Main";
import { ThemeProvider } from "@/context/ThemeContext";

export default function Home() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-100 dark:bg-netflix-dark dark:text-white transition-colors duration-200">
        <Header />
        <Main />
      </div>
    </ThemeProvider>
  );
}
