import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A package-lock.json in a parent folder would otherwise be picked as the workspace root.
  outputFileTracingRoot: process.cwd(),
  // Lets a second server (e.g. a test run) use its own build folder instead of clashing with yours in .next.
  distDir: process.env.NEXT_DIST_DIR || ".next",
};

export default nextConfig;
