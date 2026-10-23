import type { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";

/** Comma-separated ALLOWED_EMAILS restricts who can sign in; empty allows any Google account. */
const allowed = (process.env.ALLOWED_EMAILS ?? "").split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);

export const authOptions: NextAuthOptions = {
  providers: [GoogleProvider({ clientId: process.env.GOOGLE_CLIENT_ID ?? "", clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "" })],
  callbacks: {
    signIn: ({ user }) => !allowed.length || allowed.includes((user.email ?? "").toLowerCase()),
  },
};
