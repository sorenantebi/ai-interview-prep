"use client";
import { useEffect, useRef, useState } from "react";

/**
 * Renders a PDF's pages as images in the page itself, two per row, so you scroll the dashboard rather than a
 * separate PDF viewer. Uses Mozilla's pdf.js.
 */
export default function PdfPages({ src, title }: { src: string; title: string }) {
  const box = useRef<HTMLDivElement>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const pdfjs = await import("pdfjs-dist");
      pdfjs.GlobalWorkerOptions.workerSrc = new URL("pdfjs-dist/build/pdf.worker.min.mjs", import.meta.url).toString();
      const doc = await pdfjs.getDocument({ url: src }).promise;
      const el = box.current;
      if (!el || cancelled) return;
      el.replaceChildren();
      const width = el.clientWidth / (el.clientWidth >= 768 ? 2 : 1); // one column on phones
      for (let n = 1; n <= doc.numPages && !cancelled; n++) {
        const page = await doc.getPage(n);
        const base = page.getViewport({ scale: 1 });
        const viewport = page.getViewport({ scale: (width / base.width) * Math.min(window.devicePixelRatio || 1, 2) });
        const canvas = document.createElement("canvas");
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        canvas.className = "card w-full h-auto bg-white";
        canvas.setAttribute("aria-label", `${title}, page ${n} of ${doc.numPages}`);
        canvas.setAttribute("role", "img");
        el.append(canvas); // add as each page renders, so the first pages show quickly
        await page.render({ canvas, viewport }).promise;
      }
    })().catch((e) => !cancelled && setError((e as Error).message));
    return () => { cancelled = true; };
  }, [src, title]);
  return (
    <div>
      {error && <p className="text-sm text-hard">Couldn&apos;t show the PDF: {error}. <a className="underline" href={src} target="_blank" rel="noreferrer">Open it</a></p>}
      <div ref={box} className="grid gap-3 md:grid-cols-2" />
      <a href={src} target="_blank" rel="noreferrer" className="mt-2 inline-block font-mono text-xs text-muted hover:text-fg">open the PDF ↗</a>
    </div>
  );
}
