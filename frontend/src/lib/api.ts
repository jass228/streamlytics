import { API_ENDPOINTS } from "@/config/api";
import { APIDistributionResponse, APIRatingResponse } from "@/types/api";

// Genre Distribution
export async function fetchMovieGenreDistribution(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/movies/genres`
  );
  const data = await response.json();
  return data;
}

export async function fetchSerieGenreDistribution(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/series/genres`
  );
  const data = await response.json();
  return data;
}

// Country Distribution
export async function fetchMovieCountryDistribution(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/movies/countries`
  );
  const data = await response.json();
  return data;
}

export async function fetchSerieCountryDistribution(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/series/countries`
  );
  const data = await response.json();
  return data;
}

// Years Trends
export async function fetchMovieYearlyTrends(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/movies/yearly`
  );
  const data = await response.json();
  return data;
}

export async function fetchSerieYearlyTrends(): Promise<APIDistributionResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/distribution/series/yearly`
  );
  const data = await response.json();
  return data;
}

// Ratings
export async function fetchMovieRatings(): Promise<APIRatingResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/ratings/movies/countries`
  );
  const data = await response.json();
  return data;
}

export async function fetchSerieRatings(): Promise<APIRatingResponse> {
  const response = await fetch(
    `${API_ENDPOINTS}/stats/ratings/series/countries`
  );
  const data = await response.json();
  return data;
}
