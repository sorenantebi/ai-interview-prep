import { Suspense } from "react";
import FileBrowser from "@/components/FileBrowser";

export default function FilesPage() {
  return (
    <Suspense>
      <FileBrowser />
    </Suspense>
  );
}
