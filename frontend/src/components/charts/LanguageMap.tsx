"use client";
import { scaleLinear } from "d3-scale";
import { useTheme } from "next-themes";
import React, { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
} from "react-simple-maps";

const geoUrl =
  "https://raw.githubusercontent.com/subyfly/topojson/refs/heads/master/world-countries.json";

const languageCodes: { [key: string]: { name: string; countries: string[] } } =
  {
    en: { name: "Anglais", countries: ["USA", "GBR", "CAN", "AUS"] },
    es: { name: "Espagnol", countries: ["ESP", "MEX", "ARG", "COL"] },
    fr: { name: "Français", countries: ["FRA", "CAN", "BEL", "CHE"] },
    de: { name: "Allemand", countries: ["DEU", "AUT", "CHE"] },
    it: { name: "Italien", countries: ["ITA", "CHE"] },
    pt: { name: "Portugais", countries: ["PRT", "BRA"] },
    ja: { name: "Japonais", countries: ["JPN"] },
    ko: { name: "Coréen", countries: ["KOR"] },
    hi: { name: "Hindi", countries: ["IND"] },
  };

// Données fictives pour la démo
const mockData = [
  { language: "en", count: 1200 },
  { language: "es", count: 800 },
  { language: "fr", count: 600 },
  { language: "de", count: 400 },
  { language: "it", count: 300 },
  { language: "pt", count: 250 },
  { language: "ja", count: 200 },
  { language: "ko", count: 150 },
  { language: "hi", count: 100 },
];

type LanguageData = {
  language: string;
  count: number;
};

const LanguageMap = () => {
  const { theme } = useTheme();
  const [tooltipContent, setTooltipContent] = useState("");
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  const colorScale = scaleLinear<string>()
    .domain([0, Math.max(...mockData.map((d) => d.count))])
    .range(["#deebf7", theme === "dark" ? "#3182bd" : "#08519c"]);

  const getCountryColor = (countryCode: string) => {
    const language = Object.entries(languageCodes).find(([_, info]) =>
      info.countries.includes(countryCode)
    );

    if (language) {
      const languageData = mockData.find((d) => d.language === language[0]);
      return languageData ? colorScale(languageData.count) : "#F5F5F5";
    }
    return "#F5F5F5";
  };
  return (
    <div className="relative w-full h-[calc(100vh-4rem)] min-h-[400px] max-h-[600px]">
      <ComposableMap
        projection="geoMercator"
        className="w-full h-full"
        projectionConfig={{
          scale: 100,
        }}
      >
        <ZoomableGroup center={[0, 30]} zoom={1}>
          <Geographies geography={geoUrl}>
            {({ geographies }) =>
              geographies.map((geo) => (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  onMouseEnter={() => {
                    const language = Object.entries(languageCodes).find(
                      ([_, info]) =>
                        info.countries.includes(geo.properties.ISO_A3)
                    );
                    if (language) {
                      const languageData = mockData.find(
                        (d) => d.language === language[0]
                      );
                      setTooltipContent(
                        `${geo.properties.NAME}: ${language[1].name} (${
                          languageData?.count || 0
                        } titres)`
                      );
                    }
                  }}
                  onMouseLeave={() => setTooltipContent("")}
                  style={{
                    default: {
                      fill: getCountryColor(geo.properties.ISO_A3),
                      stroke: theme === "dark" ? "#374151" : "#E5E7EB",
                      strokeWidth: 0.5,
                      outline: "none",
                    },
                    hover: {
                      fill: theme === "dark" ? "#4B5563" : "#D1D5DB",
                      stroke: theme === "dark" ? "#374151" : "#E5E7EB",
                      strokeWidth: 0.5,
                      outline: "none",
                    },
                  }}
                />
              ))
            }
          </Geographies>
        </ZoomableGroup>
      </ComposableMap>
      {tooltipContent && (
        <div
          className="absolute bg-popover text-popover-foreground px-2 py-1 rounded shadow-md text-sm pointer-events-none"
          style={{
            left: tooltipPosition.x + 10,
            top: tooltipPosition.y - 40,
            transform: "translateX(-50%)",
          }}
        >
          {tooltipContent}
        </div>
      )}
    </div>
  );
};

export default LanguageMap;
