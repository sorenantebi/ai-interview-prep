import { NextResponse, type NextFetchEvent } from "next/server";
import { withAuth, type NextRequestWithAuth } from "next-auth/middleware";

const gate = withAuth({});

// Login is only enforced when Google credentials are configured in .env.local.
export default function middleware(req: NextRequestWithAuth, event: NextFetchEvent) {
  if (!process.env.GOOGLE_CLIENT_ID) return NextResponse.next();
  return gate(req, event);
}

export const config = { matcher: ["/((?!api/auth|_next|favicon.ico).*)"] };
