import { NextResponse } from "next/server";
import { authStatus, logout, openLogin } from "@/lib/claude";

export async function GET() {
  return NextResponse.json(await authStatus());
}

/** Opens a terminal running `claude auth login` (local app only: the server listens on 127.0.0.1). */
export async function POST() {
  return NextResponse.json(await openLogin());
}

/** Signs Claude Code out (`claude auth logout`). */
export async function DELETE() {
  const r = await logout();
  return NextResponse.json(r.ok ? r : { error: r.output || "Sign-out failed" }, { status: r.ok ? 200 : 500 });
}
