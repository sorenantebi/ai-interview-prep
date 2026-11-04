import { notFound } from "next/navigation";
import DeckEditor from "@/components/DeckEditor";
import { deck } from "@/lib/cards";

export const dynamic = "force-dynamic";

export default async function DeckPage({ params }: { params: Promise<{ deck: string }> }) {
  const d = await deck(decodeURIComponent((await params).deck)).catch(() => null);
  if (!d) notFound();
  return <DeckEditor file={d.file} name={d.name} cards={d.cards.map(({ front, back }) => ({ front, back }))} />;
}
