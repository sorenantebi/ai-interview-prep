import { notFound } from "next/navigation";
import RepoWorkspace from "@/components/RepoWorkspace";
import { progress, read } from "@/lib/content";
import { AREA, folderFiles, workingRepo } from "@/lib/repo";

export const dynamic = "force-dynamic";

export default async function Page({ params }: { params: Promise<{ group: string; slug: string }> }) {
  const { group, slug } = await params;
  const path = `${AREA}/${decodeURIComponent(group)}/${decodeURIComponent(slug)}`;
  const question = await read(`${path}/question.md`);
  if (question === null) notFound();
  const [{ repo, files }, solution, prog] = await Promise.all([workingRepo(path), folderFiles(`${path}/solution`), progress()]);
  const { "solution.md": explanation = "", ...fixed } = solution;
  return <RepoWorkspace path={path} question={question} repo={repo} files={files} explanation={explanation} fixed={fixed} status={prog[path]?.status} />;
}
