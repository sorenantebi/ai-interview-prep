import type { Metadata } from "next";
import { Inter, Inter_Tight, JetBrains_Mono } from "next/font/google";
import Nav from "@/components/Nav";
import Cat from "@/components/Cat";
import "./globals.css";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const interTight = Inter_Tight({ variable: "--font-inter-tight", subsets: ["latin"] });
const jetbrains = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Interview Prep",
  description: "LeetCode, system design and mock interviews, stored as local files.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${interTight.variable} ${jetbrains.variable} font-sans antialiased`}>
        <Nav authEnabled={!!process.env.GOOGLE_CLIENT_ID} />
        <main className="mx-auto max-w-[1400px] px-4 py-8 md:px-8">{children}</main>
        <footer className="mx-auto max-w-[1400px] px-4 pb-8 font-mono text-[11px] text-muted md:px-8">
          LeetCode solutions © NeetCode (<a className="underline hover:text-fg" href="https://github.com/neetcode-gh/leetcode" target="_blank" rel="noreferrer">neetcode-gh/leetcode</a>, MIT License) ·
          problems and starter code © LeetCode · system design videos © Hello Interview · not affiliated with any of them
        </footer>
        <Cat />
      </body>
    </html>
  );
}
