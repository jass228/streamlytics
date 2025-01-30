import { StreamlyticsContent } from "@/type/api";
import { NextResponse } from "next/server";

const stream: StreamlyticsContent[] = [];

export async function GET() {
  return NextResponse.json(stream);
}
