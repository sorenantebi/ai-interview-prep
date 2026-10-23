/** POSTs JSON and throws the server's error message on failure. */
export async function api(url: string, body: unknown, method = "POST") {
  const res = await fetch(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.error) throw new Error(data.error ?? data.output ?? `Request failed (${res.status})`);
  return data;
}

export const putFile = (path: string, content: string) => api("/api/files", { path, content }, "PUT");
