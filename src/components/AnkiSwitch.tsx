"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/client";

/** A checkbox for the daily-review choices: Anki review on/off (no deck), or one deck in or out of it. */
export default function AnkiSwitch({ deck, checked, label }: { deck?: string; checked: boolean; label: string }) {
  const router = useRouter();
  const [on, setOn] = useState(checked);
  const [busy, setBusy] = useState(false);
  async function toggle() {
    setOn(!on);
    setBusy(true);
    try {
      await api("/api/cards", deck ? { action: "settings", deck, include: !on } : { action: "settings", daily: !on });
      router.refresh();
    } catch {
      setOn(on);
    } finally {
      setBusy(false);
    }
  }
  return (
    <label className="flex cursor-pointer items-center gap-1.5 text-xs text-muted">
      <input type="checkbox" checked={on} onChange={toggle} disabled={busy} />
      {label}
    </label>
  );
}
