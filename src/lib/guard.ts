const LOCAL = new Set(["localhost", "127.0.0.1", "[::1]"]);

/**
 * The API can run code and write files, so only this app's own pages may use it. Other websites you visit can send
 * requests to localhost (a "text/plain" POST skips the browser's CORS check), and DNS rebinding can point a foreign
 * domain at 127.0.0.1, so: the Host must be local, and any request that changes something must come from this origin.
 * Returns the reason to refuse, or null to allow.
 */
export function foreignRequest(method: string, headers: { get(name: string): string | null }): string | null {
  const host = headers.get("host") ?? "";
  if (!LOCAL.has(host.replace(/:\d+$/, ""))) return "not a local address";
  if (method === "GET" || method === "HEAD") return null;
  const origin = headers.get("origin");
  const site = headers.get("sec-fetch-site");
  let sameOrigin = false;
  try { sameOrigin = !!origin && new URL(origin).host === host; } catch {}
  // Browsers always send Origin (and Sec-Fetch-Site) on cross-site writes; a request with neither is not from a web page.
  if ((origin && !sameOrigin) || (site && site !== "same-origin" && site !== "none")) return "cross-site request";
  return null;
}
