import { planUsage } from "@/lib/claude";

export const dynamic = "force-dynamic";

export default async function UsagePage() {
  const { limits, raw } = await planUsage().catch((e) => ({ limits: [], raw: (e as Error).message }));
  return (
    <div className="max-w-3xl space-y-6">
      <h1 className="page-title">Claude Code left</h1>
      {limits.length === 0 ? (
        <div className="card space-y-2 p-4 text-sm">
          <p>Couldn&apos;t read your plan limits from Claude Code. Its output was:</p>
          <pre className="whitespace-pre-wrap font-mono text-xs text-muted">{raw || "(nothing)"}</pre>
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {limits.map((l) => {
            const left = Math.max(0, 100 - l.used);
            return (
              <div key={l.label} className="card space-y-3 p-5">
                <div className="font-mono text-xs uppercase tracking-wide text-muted">{l.label}</div>
                <div className={`font-display text-6xl font-medium tracking-tight tabular-nums ${left <= 10 ? "text-hard" : ""}`}>
                  {left}% <span className="text-2xl text-muted">left</span>
                </div>
                <div className="h-2 bg-fg/10" role="meter" aria-valuemin={0} aria-valuemax={100} aria-valuenow={left} aria-label={`${l.label}: ${left}% left`}>
                  <div className={`h-full ${left <= 10 ? "bg-hard" : "bg-fg"}`} style={{ width: `${left}%` }} />
                </div>
                <div className="font-mono text-xs text-muted">{l.resets ? `resets ${l.resets}` : `${l.used}% used`}</div>
              </div>
            );
          })}
        </div>
      )}
      <p className="font-mono text-xs text-muted">From Claude Code&apos;s <code>/usage</code>, read when this page loads. Reload to refresh.</p>
    </div>
  );
}
