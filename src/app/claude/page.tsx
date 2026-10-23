import { defaultModelName, MODELS, planUsage, savedModel } from "@/lib/claude";
import ModelPicker from "@/components/ModelPicker";
import ClaudeConnection from "@/components/ClaudeConnection";

export const dynamic = "force-dynamic";

export default async function ClaudePage() {
  const [{ limits, raw }, model, defaultName] = await Promise.all([planUsage().catch((e) => ({ limits: [], raw: (e as Error).message })), savedModel(), defaultModelName()]);
  return (
    <div className="max-w-3xl space-y-6">
      <h1 className="page-title">Claude</h1>
      <ClaudeConnection />
      <ModelPicker models={MODELS} initial={model} defaultName={defaultName} />
      {limits.length === 0 ? (
        <div className="card space-y-2 p-4 text-sm">
          <p>Couldn&apos;t read your plan limits from Claude Code. Its output was:</p>
          <pre className="whitespace-pre-wrap font-mono text-xs text-muted">{raw || "(nothing)"}</pre>
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {limits.map((l) => {
            const high = l.used >= 90;
            return (
              <div key={l.label} className="card space-y-3 p-5">
                <div className="font-mono text-xs uppercase tracking-wide text-muted">{l.label}</div>
                <div className={`font-display text-6xl font-medium tracking-tight tabular-nums ${high ? "text-hard" : ""}`}>
                  {l.used}% <span className="text-2xl text-muted">used</span>
                </div>
                <div className="h-2 bg-fg/10" role="meter" aria-valuemin={0} aria-valuemax={100} aria-valuenow={l.used} aria-label={`${l.label}: ${l.used}% used`}>
                  <div className={`h-full ${high ? "bg-hard" : "bg-fg"}`} style={{ width: `${Math.min(100, l.used)}%` }} />
                </div>
                <div className="font-mono text-xs text-muted">{l.resets ? `resets ${l.resets}` : `${100 - l.used}% left`}</div>
              </div>
            );
          })}
        </div>
      )}
      <p className="font-mono text-xs text-muted">From Claude Code&apos;s <code>/usage</code>, read when this page loads. Reload to refresh.</p>
    </div>
  );
}
