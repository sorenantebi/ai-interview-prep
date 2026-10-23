"use client";
import { Handle, Position, ReactFlow, type Edge, type Node, type NodeProps } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useRouter } from "next/navigation";
import { EDGES, LAYOUT } from "@/lib/roadmap";

type Stat = { group: string; name: string; total: number; solved: number };
type TopicData = Stat & { selected: boolean };

function Topic({ data }: NodeProps<Node<TopicData>>) {
  const pct = data.total ? (data.solved / data.total) * 100 : 0;
  const sel = data.selected;
  return (
    <div className={`w-44 cursor-pointer border px-3 py-2 ${sel ? "border-fg bg-fg text-panel" : "border-border bg-panel text-fg hover:border-fg"}`}>
      <Handle type="target" position={Position.Top} className="!opacity-0" />
      <div className="truncate text-center font-display text-[15px] font-medium">{data.name}</div>
      <div className={`mt-1.5 h-1.5 overflow-hidden ${sel ? "bg-panel/25" : "bg-fg/10"}`}>
        <div className="h-full bg-accent" style={{ width: `${pct}%` }} />
      </div>
      <div className={`mt-1 text-center font-mono text-[11px] tabular-nums ${sel ? "opacity-70" : "text-muted"}`}>{data.solved} / {data.total}</div>
      <Handle type="source" position={Position.Bottom} className="!opacity-0" />
    </div>
  );
}

const nodeTypes = { topic: Topic };

export default function Roadmap({ stats, selected }: { stats: Stat[]; selected?: string }) {
  const router = useRouter();
  const nodes: Node<TopicData>[] = stats
    .filter((s) => LAYOUT[s.name])
    .map((s) => ({ id: s.name, type: "topic", position: { x: LAYOUT[s.name][0] * 200, y: LAYOUT[s.name][1] * 100 }, data: { ...s, selected: s.group === selected } }));
  const ids = new Set(nodes.map((n) => n.id));
  const edges: Edge[] = EDGES.filter(([a, b]) => ids.has(a) && ids.has(b)).map(([a, b]) => ({ id: `${a}>${b}`, source: a, target: b, style: { stroke: "var(--fg)", strokeOpacity: 0.35 } }));

  return (
    <div className="card h-[640px] overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.04 }}
        nodesDraggable={false}
        nodesConnectable={false}
        proOptions={{ hideAttribution: true }}
        onNodeClick={(_, n) => router.push(`/leetcode?topic=${encodeURIComponent((n.data as TopicData).group)}`, { scroll: false })}
        style={{ background: "transparent" }}
      />
    </div>
  );
}
