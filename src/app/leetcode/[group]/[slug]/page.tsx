import ProblemPage, { type ProblemPageProps } from "@/components/ProblemPage";

export const dynamic = "force-dynamic";

export default function Page(props: ProblemPageProps) {
  return <ProblemPage area="leetcode" {...props} />;
}
