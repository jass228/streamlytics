import React, { ReactNode } from "react";
import { Card } from "./ui/card";

interface CardContentProps {
  title: string;
  children: ReactNode;
}

const CardContent = ({ title, children }: CardContentProps) => {
  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      {children}
    </Card>
  );
};

export default CardContent;
