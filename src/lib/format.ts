/** "2026-10-23" or an ISO timestamp -> "23 Oct 2026" in the viewer's locale. */
export const fmtDate = (d: string) => new Date(d.length === 10 ? d + "T00:00" : d).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
