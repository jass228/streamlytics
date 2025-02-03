"use client";
import {
  fetchMovieCountryDistribution,
  fetchSerieCountryDistribution,
} from "@/lib/api";
import { APIDistributionResponse } from "@/types/api";
import { ResponsiveChoropleth } from "@nivo/geo";
import { useTheme } from "next-themes";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import countries from "../../data/world_countries.json";
import { Minus, Move, Plus, RefreshCw } from "lucide-react";

const REGIONS = {
  WORLD: { position: [0.5, 0.5], zoom: 100, rotation: [0, 0, 0] },
  EUROPE: { position: [0.6, 0.4], zoom: 250, rotation: [0, 0, 0] },
  ASIA: { position: [0.7, 0.5], zoom: 150, rotation: [0, 0, 0] },
  NORTH_AMERICA: { position: [0.2, 0.4], zoom: 180, rotation: [0, 0, 0] },
  SOUTH_AMERICA: { position: [0.3, 0.7], zoom: 180, rotation: [0, 0, 0] },
  AFRICA: { position: [0.5, 0.6], zoom: 180, rotation: [0, 0, 0] },
  OCEANIA: { position: [0.8, 0.7], zoom: 200, rotation: [0, 0, 0] },
};

interface LanguageMapProps {
  media: string;
}

const LanguageMap = ({ media }: LanguageMapProps) => {
  const { theme } = useTheme();

  // States
  const [movieData, setMovieData] = useState<APIDistributionResponse | null>(
    null
  );
  const [serieData, setSerieData] = useState<APIDistributionResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(true);
  const [zoom, setZoom] = useState(REGIONS.WORLD.zoom);
  const [position, setPosition] = useState({
    x: REGIONS.WORLD.position[0],
    y: REGIONS.WORLD.position[1],
  });
  const [rotation, setRotation] = useState(REGIONS.WORLD.rotation);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedRegion, setSelectedRegion] = useState("WORLD");

  // Callbacks
  const handleZoom = useCallback((delta: number) => {
    setZoom((prevZoom) => Math.max(50, Math.min(400, prevZoom + delta)));
  }, []);

  const handleWheel = useCallback(
    (event: { preventDefault: () => void; deltaY: number }) => {
      event.preventDefault();
      handleZoom(-event.deltaY * 0.5);
    },
    [handleZoom]
  );

  const handleMouseDown = useCallback(
    (event: { preventDefault: () => void; clientX: any; clientY: any }) => {
      event.preventDefault();
      setIsDragging(true);
      setDragStart({ x: event.clientX, y: event.clientY });
    },
    []
  );

  const handleMouseMove = useCallback(
    (event: {
      preventDefault: () => void;
      clientX: number;
      clientY: number;
    }) => {
      if (!isDragging) return;
      event.preventDefault();
      const sensitivity = 0.005;
      const dx = (event.clientX - dragStart.x) * sensitivity;
      const dy = (event.clientY - dragStart.y) * sensitivity;
      setPosition((prev) => ({
        x: prev.x - dx,
        y: prev.y - dy,
      }));
      setDragStart({
        x: event.clientX,
        y: event.clientY,
      });
    },
    [isDragging, dragStart]
  );

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  // Memos
  const movieCountryData = useMemo(
    () =>
      movieData
        ? Object.entries(movieData.data).map(([country, value]) => ({
            id: country,
            value,
          }))
        : [],
    [movieData]
  );

  const serieCountryData = useMemo(
    () =>
      serieData
        ? Object.entries(serieData.data).map(([country, value]) => ({
            id: country,
            value,
          }))
        : [],
    [serieData]
  );

  const domain = useMemo(() => {
    if (!movieCountryData.length) return [0, 0];
    const values = movieCountryData.map((d) => d.value);
    return [Math.min(...values), Math.max(...values)];
  }, [movieCountryData]);

  const domainSeries = useMemo(() => {
    if (!serieCountryData.length) return [0, 0];
    const values = serieCountryData.map((d) => d.value);
    return [Math.min(...values), Math.max(...values)];
  }, [serieCountryData]);

  // Effects
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [movies, series] = await Promise.all([
          fetchMovieCountryDistribution(),
          fetchSerieCountryDistribution(),
        ]);
        setMovieData(movies);
        setSerieData(series);
      } catch (error) {
        console.error("Error loading data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    const element = document.getElementById("map-container");
    if (element) {
      element.addEventListener("wheel", handleWheel, { passive: false });
      return () => element.removeEventListener("wheel", handleWheel);
    }
  }, [handleWheel]);

  if (isLoading || !movieData || !serieData) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        Loading...
      </div>
    );
  }

  // Helpers
  const navigateToRegion = (regionKey: keyof typeof REGIONS) => {
    const region = REGIONS[regionKey];
    setSelectedRegion(regionKey);
    setZoom(region.zoom);
    setPosition({ x: region.position[0], y: region.position[1] });
    setRotation(region.rotation);
  };

  return (
    <div className="relative w-full h-[calc(100vh-4rem)] min-h-[400px] max-h-[600px]">
      <div
        id="map-container"
        className="relative h-[600px] cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <div className="absolute right-4 top-4 z-10 flex flex-col gap-2">
          <button
            onClick={() => handleZoom(20)}
            className="p-2 bg-white dark:text-black rounded-full shadow-lg hover:bg-gray-100 transition-colors"
          >
            <Plus size={20} />
          </button>
          <button
            onClick={() => handleZoom(-20)}
            className="p-2 bg-white dark:text-black rounded-full shadow-lg hover:bg-gray-100 transition-colors"
          >
            <Minus size={20} />
          </button>
          <button
            onClick={() => navigateToRegion("WORLD")}
            className="p-2 bg-white dark:text-black rounded-full shadow-lg hover:bg-gray-100 transition-colors"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        <div className="absolute left-4 top-4 z-10 dark:text-black bg-white px-3 py-1 rounded-full shadow-lg flex items-center gap-2">
          <Move size={16} />
          <span className="text-sm text-gray-600">
            Zoom: {Math.round(zoom)}%
          </span>
        </div>

        <ResponsiveChoropleth
          data={media === "movie" ? movieCountryData : serieCountryData}
          features={countries.features}
          margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
          colors="nivo"
          domain={media === "movie" ? domain : domainSeries}
          unknownColor={theme === "dark" ? "#ffefe4" : "#001e35"}
          label="properties.name"
          valueFormat=".0s"
          projectionScale={zoom}
          projectionTranslation={[position.x, position.y]}
          projectionRotation={rotation}
          enableGraticule={true}
          graticuleLineColor="rgba(0, 0, 0, .2)"
          borderWidth={0.5}
          borderColor="#101b42"
          legends={[
            {
              anchor: "bottom-left",
              direction: "column",
              justify: true,
              translateX: 20,
              translateY: -180,
              itemsSpacing: 0,
              itemWidth: 60,
              itemHeight: 18,
              itemDirection: "left-to-right",
              itemOpacity: 0.85,
              symbolSize: 18,
            },
          ]}
          theme={{
            tooltip: {
              container: {
                color: "#000",
              },
            },
            legends: {
              text: {
                fill: theme === "dark" ? "#fff" : "#000",
              },
            },
          }}
        />
      </div>
    </div>
  );
};

export default LanguageMap;
