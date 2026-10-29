import CardReview from "@/components/CardReview";
import { cardKey, decks, dueToday, preview, schedule } from "@/lib/cards";
import { localDate } from "@/lib/content";

export const dynamic = "force-dynamic";

/** Today's cards: one deck (?deck=) or all of them; reviews due first, then new cards. */
export default async function ReviewPage({ searchParams }: { searchParams: Promise<{ deck?: string }> }) {
  const only = (await searchParams).deck;
  const [all, sched] = await Promise.all([decks(), schedule()]);
  const today = localDate(new Date());
  const picked = all.filter((d) => !only || d.file === only);
  const today_ = picked.map((d) => ({ d, ...dueToday(d, sched, today) }));
  const item = (deck: string) => (c: { id: string; front: string; back: string }) => ({ deck, ...c, labels: preview(sched[cardKey(deck, c.id)], today) });
  const queue = [...today_.flatMap(({ d, due }) => due.map(item(d.file))), ...today_.flatMap(({ d, fresh }) => fresh.map(item(d.file)))];
  return <CardReview queue={queue} title={only ? (picked[0]?.name ?? only) : "All decks"} back={only ? `/cards/${encodeURIComponent(only)}` : "/cards"} />;
}
