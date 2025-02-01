import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Star } from "lucide-react";

const topContent = [
  {
    title: "Stranger Things",
    rating: 8.7,
    genre: "Science Fiction",
    year: 2016,
    type: "Série",
  },
  {
    title: "La Casa de Papel",
    rating: 8.3,
    genre: "Action",
    year: 2017,
    type: "Série",
  },
  {
    title: "The Crown",
    rating: 8.6,
    genre: "Drame",
    year: 2016,
    type: "Série",
  },
  {
    title: "Dark",
    rating: 8.8,
    genre: "Science Fiction",
    year: 2017,
    type: "Série",
  },
  {
    title: "Narcos",
    rating: 8.8,
    genre: "Crime",
    year: 2015,
    type: "Série",
  },
];

const TopContent = () => {
  return (
    <div className="w-full overflow-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Titre</TableHead>
            <TableHead>Note</TableHead>
            <TableHead>Genre</TableHead>
            <TableHead>Année</TableHead>
            <TableHead>Type</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {topContent.map((content) => (
            <TableRow key={content.title}>
              <TableCell className="font-medium">{content.title}</TableCell>
              <TableCell>
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  {content.rating}
                </div>
              </TableCell>
              <TableCell>{content.genre}</TableCell>
              <TableCell>{content.year}</TableCell>
              <TableCell>{content.type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default TopContent;
