import { Suspense } from "react";
import AiStudio from "@/components/AiStudio";

export default function AiPage() {
  return (
    <Suspense>
      <AiStudio />
    </Suspense>
  );
}
