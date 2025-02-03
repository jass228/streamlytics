export interface StreamlyticsContent {
  title: string;
  release_date?: string;
  first_air_date?: string;
  rating: string;
  genre: string[];
  tmdb_id: number;
  original_language: string;
  poster_path: string;
}

export interface APIDistributionResponse {
  data: Record<string, number>;
  total: number;
  count: number;
}

interface CountryRating {
  mean: number;
  count: number;
}

export interface APIRatingResponse {
  data: Record<string, CountryRating>;
  total_ratings: number;
  average_rating: number;
}
