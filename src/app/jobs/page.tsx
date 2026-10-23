import JobsTable, { type Job } from "@/components/JobsTable";
import { read } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function JobsPage() {
  let jobs: Job[] = [];
  try { jobs = JSON.parse((await read("jobs.json")) ?? "[]"); } catch {}
  return (
    <div className="space-y-6">
      <h1 className="page-title">Jobs</h1>
      <JobsTable initial={jobs} />
    </div>
  );
}
