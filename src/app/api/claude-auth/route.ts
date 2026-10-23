import { NextResponse } from "next/server";
import { authStatus, openLogin } from "@/lib/claude";

export async function GET() {
  return NextResponse.json(await authStatus());
}

/** Opens a terminal running `claude auth login` (local app only: the server listens on 127.0.0.1). */
export async function POST() {
  return NextResponse.json(await openLogin());
}
