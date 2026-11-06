import RepoList from "@/components/RepoList";
import { listRepos } from "@/lib/repos";

export const dynamic = "force-dynamic";

export default async function ReposPage() {
  return (
    <div className="space-y-6">
      <h1 className="page-title">GitHub</h1>
      <RepoList repos={await listRepos()} />
    </div>
  );
}
