"use client";
import { useRouter } from "next/navigation";

export default function DeletePlan() {
  const router = useRouter();
  return (
    <button className="btn px-2 py-1 text-xs hover:border-hard" onClick={async () => { if (confirm("Delete your study plan?")) { await fetch("/api/plan", { method: "DELETE" }); router.refresh(); } }}>
      Delete plan
    </button>
  );
}
