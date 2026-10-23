"use client";
import { useRouter } from "next/navigation";
import { startTransition, useEffect } from "react";

/**
 * Pages restored with Back (or from the router cache) show what they had before, so a task you just completed by
 * submitting looks unticked. Fetch fresh data whenever the page is shown or the tab becomes visible again.
 */
export default function RefreshOnShow() {
  const router = useRouter();
  useEffect(() => {
    const refresh = () => startTransition(() => router.refresh());
    const onVisible = () => document.visibilityState === "visible" && refresh();
    refresh();
    window.addEventListener("pageshow", refresh);
    document.addEventListener("visibilitychange", onVisible);
    return () => { window.removeEventListener("pageshow", refresh); document.removeEventListener("visibilitychange", onVisible); };
  }, [router]);
  return null;
}
