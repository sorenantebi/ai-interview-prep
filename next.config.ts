import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A package-lock.json in a parent folder would otherwise be picked as the workspace root.
  outputFileTracingRoot: process.cwd(),
};

export default nextConfig;
