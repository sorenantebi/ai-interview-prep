import { NextResponse, type NextFetchEvent } from "next/server";
import { withAuth, type NextRequestWithAuth } from "next-auth/middleware";
import { foreignRequest } from "@/lib/guard";

const gate = withAuth({});
// Login is only enforced when Google credentials are configured in .env.local.
export default function middleware(req: NextRequestWithAuth, event: NextFetchEvent) {
  const refused = foreignRequest(req.method, req.headers);
  if (refused) return new NextResponse(`Forbidden: ${refused}`, { status: 403 });
  if (!process.env.GOOGLE_CLIENT_ID) return NextResponse.next();
  return gate(req, event);
}

export const config = { matcher: ["/((?!_next|favicon.ico|icon.png).*)"] };
