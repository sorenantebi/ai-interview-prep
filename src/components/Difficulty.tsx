const color: Record<string, string> = { Easy: "bg-easy", Medium: "bg-medium", Hard: "bg-hard" };

export default function Difficulty({ level }: { level?: string }) {
  if (!level) return null;
  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-muted">
      <span className={`h-2 w-2 ${color[level] ?? "bg-muted"}`} aria-hidden />
      {level}
    </span>
  );
}
