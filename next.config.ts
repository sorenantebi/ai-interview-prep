import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A package-lock.json in a parent folder would otherwise be picked as the workspace root.
  outputFileTracingRoot: process.cwd(),
  // Lets a second server (e.g. a test run) use its own build folder instead of clashing with yours in .next.
  distDir: process.env.NEXT_DIST_DIR || ".next",
  // The desktop app (npm run dist) runs a self-contained server; these files are read at runtime, so tracing misses them.
  ...(process.env.STANDALONE && {
    output: "standalone",
    outputFileTracingIncludes: { "/**": ["node_modules/monaco-editor/min/vs/**", "src/lib/case_runner.py"] },
    // Your data and Python packages are read through dynamic paths, which tracing would otherwise copy into the app.
    outputFileTracingExcludes: { "/**": ["content/**", ".venv/**", ".env*"] },
  }),
};

export default nextConfig;
