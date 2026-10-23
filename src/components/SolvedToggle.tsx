"use client";
import { useState } from "react";
import { api } from "@/lib/client";

export default function SolvedToggle({ path, status: initial, label = "Mark solved" }: { path: string; status?: string; label?: string }) {
  const [status, setStatus] = useState(initial);
  async function toggle() {
    const next = status === "solved" ? null : "solved";
    await api("/api/progress", { path, status: next });
    setStatus(next ?? undefined);
  }
  return (
    <button onClick={toggle} className={`btn ${status === "solved" ? "border-easy text-easy" : ""}`}>
      {status === "solved" ? "✓ Done" : label}
    </button>
  );
}
