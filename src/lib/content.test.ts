import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

process.env.CONTENT_DIR = fs.mkdtempSync(path.join(os.tmpdir(), "content-test-"));
const { safePath, write, read, problems, setProgress, progress } = await import("./content.ts");
const { files } = await import("./claude.ts");

test("safePath blocks escapes from content/", () => {
  assert.throws(() => safePath("../etc/passwd"));
  assert.throws(() => safePath("leetcode/../../x"));
  assert.throws(() => safePath("/etc/passwd"));
  assert.ok(safePath("leetcode/a/question.md").endsWith(path.join("leetcode", "a", "question.md")));
});

test("problems parse frontmatter, title and sort by difficulty", async () => {
  await write("leetcode/01 T/b/question.md", "---\ndifficulty: Hard\n---\n# Bee\n");
  await write("leetcode/01 T/a/question.md", "---\ndifficulty: Easy\nleetcode: https://x\n---\n# Ay\n");
  const ps = await problems("leetcode/01 T");
  assert.deepEqual(ps.map((p) => [p.title, p.difficulty]), [["Ay", "Easy"], ["Bee", "Hard"]]);
  assert.equal(ps[0].leetcode, "https://x");
  assert.equal(await read("missing.md"), null);
});

test("progress round-trips", async () => {
  await setProgress("leetcode/01 T/a", "solved");
  assert.equal((await progress())["leetcode/01 T/a"].status, "solved");
  await setProgress("leetcode/01 T/a", null);
  assert.equal((await progress())["leetcode/01 T/a"], undefined);
});

test("files() splits model output into named files", () => {
  const out = files("noise\n=== FILE: question.md ===\n# Q\n\n=== FILE: solution.md ===\n```python\nx = [[1]]\n```\n=== END ===\ntrailing");
  assert.deepEqual(Object.keys(out), ["question.md", "solution.md"]);
  assert.equal(out["question.md"], "# Q\n");
  assert.equal(out["solution.md"], "```python\nx = [[1]]\n```\n");
});

test("spaced repetition ladder", async () => {
  const { review, setProgress } = await import("./content.ts");
  const now = new Date(2026, 0, 10);
  const day = (n: number) => new Date(2026, 0, 10 + n).toLocaleDateString("en-CA");
  await setProgress("leetcode/01 T/a", "solved");
  await assert.rejects(review("leetcode/01 T/missing", "enable", now));
  assert.deepEqual((await review("leetcode/01 T/a", "enable", now))["leetcode/01 T/a"].review, { step: 0, due: day(1) });
  assert.equal((await review("leetcode/01 T/a", "good", now))["leetcode/01 T/a"].review?.due, day(3));
  assert.equal((await review("leetcode/01 T/a", "easy", now))["leetcode/01 T/a"].review?.due, day(14));
  assert.equal((await review("leetcode/01 T/a", "hard", now))["leetcode/01 T/a"].review?.due, day(14));
  assert.equal((await review("leetcode/01 T/a", "again", now))["leetcode/01 T/a"].review?.due, day(1));
  await setProgress("leetcode/01 T/a", "attempted"); // failed re-run must not undo the solve or the schedule
  const e = (await progress())["leetcode/01 T/a"];
  assert.equal(e.status, "solved");
  assert.ok(e.review);
  assert.equal((await review("leetcode/01 T/a", "disable", now))["leetcode/01 T/a"].review, undefined);
});

test("complexity reads Time and Space", async () => {
  const { complexity } = await import("./content.ts");
  assert.deepEqual(complexity("## Complexity\n\n- **Time:** `O(V + E)` — why\n- **Space:** `O(V)` — why\n"), { time: "O(V + E)", space: "O(V)" });
  assert.deepEqual(complexity("nothing"), { time: undefined, space: undefined });
});

test("review date can be set by hand", async () => {
  const { review, setProgress } = await import("./content.ts");
  await setProgress("leetcode/01 T/b", "solved");
  assert.deepEqual((await review("leetcode/01 T/b", "set", new Date(), "2027-02-03"))["leetcode/01 T/b"].review, { step: 0, due: "2027-02-03" });
  await assert.rejects(review("leetcode/01 T/b", "set", new Date(), "tomorrow"));
  await assert.rejects(review("leetcode/01 T/b", "set", new Date(), "2027-13-45"));
});


test("case runner compares your output with the reference, LeetCode style", async () => {
  const { runCases } = await import("./run.ts");
  const { parseExamples, starterFrom } = await import("./starter.ts");
  const ref = "class Solution:\n    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:\n        res = []\n        def dfs(i, cur, t):\n            if t == 0: res.append(cur[:]); return\n            if i == len(candidates) or t < 0: return\n            dfs(i, cur + [candidates[i]], t - candidates[i]); dfs(i + 1, cur, t)\n        dfs(0, [], target)\n        return res\n";
  const starter = starterFrom(ref);
  assert.match(starter, /def combinationSum\(self, candidates: List\[int\], target: int\) -> List\[List\[int\]\]:\n\s+pass/);
  assert.doesNotMatch(starter, /dfs/);
  const question = "Return them in any order.\n\nInput: candidates = [2,3,6,7], target = 7\nOutput: [[2,2,3],[7]]\nInput: the same, but empty\n";
  const { names, cases } = parseExamples(question, starter);
  assert.deepEqual(names, ["candidates", "target"]);
  assert.deepEqual(cases, [["[2,3,6,7]", "7"]]); // prose example dropped

  const mine = "class Solution:\n    def combinationSum(self, candidates, target):\n        print('debug')\n        return [[7], [3, 2, 2]]\n";
  let r = await runCases({ attempt: mine, reference: ref, starter, cases: [...cases, ["[2]", "1"]], question });
  assert.equal(r.results![0].ok, true); // order ignored for "any order" problems
  assert.equal(r.results![0].note, "matches when order inside each group is ignored");
  assert.equal(r.results![0].stdout, "debug\n");
  assert.equal(r.results![0].expected, "[[2,2,3],[7]]");
  assert.equal(r.results![1].ok, false);
  assert.equal(r.results![1].expected, "[]");

  r = await runCases({ attempt: "class Solution:\n    def combinationSum(self, c, t):\n        return 1 / 0\n", reference: ref, starter, cases, question });
  assert.match(r.results![0].error!, /ZeroDivisionError.*\(line 3\)/);

  const lru = "class LRUCache:\n    def __init__(self, capacity: int):\n        self.c, self.d = capacity, {}\n    def get(self, key: int) -> int:\n        if key not in self.d: return -1\n        self.d[key] = self.d.pop(key); return self.d[key]\n    def put(self, key: int, value: int) -> None:\n        self.d.pop(key, None); self.d[key] = value\n        if len(self.d) > self.c: self.d.pop(next(iter(self.d)))\n";
  r = await runCases({ attempt: lru, reference: lru, starter: starterFrom(lru), cases: [['["LRUCache","put","put","get","put","get"]', "[[2],[1,1],[2,2],[1],[3,3],[2]]"]], question: "" });
  assert.equal(r.results![0].output, "[null,null,null,1,null,-1]");

  const rev = "class Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        prev = None\n        while head: head.next, prev, head = prev, head, head.next\n        return prev\n";
  r = await runCases({ attempt: rev, reference: rev, starter: starterFrom(rev), cases: [["[1,2,3]"], ["[]"]], question: "" });
  assert.deepEqual(r.results!.map((x) => [x.output, x.ok]), [["[3,2,1]", true], ["[]", true]]);
});

test("seeded shuffle is stable and a permutation", async () => {
  const { shuffle, sequence } = await import("./order.ts");
  const xs = Array.from({ length: 50 }, (_, i) => `p${i}`);
  assert.deepEqual(shuffle(xs, 42), shuffle(xs, 42));
  assert.notDeepEqual(shuffle(xs, 42), shuffle(xs, 43));
  assert.deepEqual([...shuffle(xs, 7)].sort(), [...xs].sort());
  const seq = sequence(xs, { random: true, seed: 1, unsolved: true }, new Set(["p1", "p2"]), "p2");
  assert.ok(seq.includes("p2") && !seq.includes("p1") && seq.length === 49);
  assert.deepEqual(sequence(xs, { random: false, seed: 0, unsolved: false }, new Set()), xs);
});


test("plan usage parser reads each limit's used percentage and reset time", async () => {
  const { parseUsage } = await import("./claude.ts");
  const report = "You are currently using your subscription\n\nCurrent session: 60% used · resets Oct 23 at 11:19pm (Europe/Berlin)\nCurrent week (all models): 13% used · resets Oct 28 at 3:59am (Europe/Berlin)\nCurrent week (Opus): 100% used\n\nLast 24h · 329 requests";
  assert.deepEqual(parseUsage(report), [
    { label: "Current session", used: 60, resets: "Oct 23 at 11:19pm (Europe/Berlin)" },
    { label: "Current week (all models)", used: 13, resets: "Oct 28 at 3:59am (Europe/Berlin)" },
    { label: "Current week (Opus)", used: 100, resets: null },
  ]);
});

test("repo URLs are validated and named", async () => {
  const { normalizeUrl } = await import("./repos.ts");
  assert.deepEqual(normalizeUrl("neetcode-gh/leetcode"), { url: "https://github.com/neetcode-gh/leetcode.git", name: "leetcode" });
  assert.equal(normalizeUrl("https://gitlab.com/group/sub/my-repo.git").name, "my-repo");
  assert.equal(normalizeUrl("git@github.com:me/dotfiles.git").name, "dotfiles");
  for (const bad of ["file:///etc", "--upload-pack=touch /tmp/x", "http://insecure.com/a/b", "https://x.com/a b", "../x"]) assert.throws(() => normalizeUrl(bad));
});

test("repo markdown links resolve inside the repo", async () => {
  const { resolveRepoUrl } = await import("./repo-links.ts");
  const repo = { name: "AI-Qs", dir: "" };
  assert.equal(resolveRepoUrl("14-company/qwen-alibaba.md", "href", repo), "/repos/AI-Qs/14-company/qwen-alibaba.md");
  assert.equal(resolveRepoUrl("./docs/a b.md#setup", "href", repo), "/repos/AI-Qs/docs/a%20b.md#setup");
  assert.equal(resolveRepoUrl("../README.md", "href", { name: "AI-Qs", dir: "docs" }), "/repos/AI-Qs/README.md");
  assert.equal(resolveRepoUrl("../../etc/passwd", "href", { name: "AI-Qs", dir: "docs" }), "#");
  assert.equal(resolveRepoUrl("img/logo.png", "src", repo), "/api/repos/raw?path=repos%2FAI-Qs%2Fimg%2Flogo.png");
  for (const u of ["https://x.com/a", "#top", "/abs", "mailto:a@example.com"]) assert.equal(resolveRepoUrl(u, "href", repo), u);
});

test("streaks count consecutive active days", async () => {
  const { streaks } = await import("./content.ts");
  const days = { "2026-10-20": 2, "2026-10-21": 1, "2026-10-22": 3, "2026-10-15": 1, "2026-10-16": 1 };
  assert.deepEqual(streaks(days, "2026-10-23"), { current: 3, longest: 3 }); // today empty: streak still alive from yesterday
  assert.deepEqual(streaks({ ...days, "2026-10-23": 1 }, "2026-10-23"), { current: 4, longest: 4 });
  assert.deepEqual(streaks(days, "2026-10-25"), { current: 0, longest: 3 });
  assert.deepEqual(streaks({}, "2026-10-23"), { current: 0, longest: 0 });
});

test("study plans keep only real problems and in-range days", async () => {
  const { validatePlan } = await import("./plan.ts");
  const titles = new Map([["leetcode/02 Two Pointers/valid-palindrome", "Valid Palindrome"]]);
  const plan = validatePlan({
    title: "Plan",
    days: [
      { date: "2026-10-25", focus: "TP", tasks: [{ type: "leetcode", path: "leetcode/02 Two Pointers/valid-palindrome" }, { type: "leetcode", path: "leetcode/made-up" }, { type: "note", text: " review " }, { type: "review", path: "leetcode/02 Two Pointers/valid-palindrome" }] },
      { date: "2026-10-24", tasks: [{ type: "note", text: "warm up" }] },
      { date: "2027-01-01", tasks: [{ type: "note", text: "too late" }] },
      { date: "bad", tasks: [] },
    ],
  }, titles, "2026-10-24", "2026-11-20");
  assert.deepEqual(plan.days.map((d) => d.date), ["2026-10-24", "2026-10-25"]);
  assert.deepEqual(plan.days[1].tasks, [{ type: "leetcode", path: "leetcode/02 Two Pointers/valid-palindrome", title: "Valid Palindrome" }, { type: "note", text: "review" }, { type: "review", path: "leetcode/02 Two Pointers/valid-palindrome", title: "Valid Palindrome" }]);
  const { taskDone } = await import("./plan.ts");
  const solved = new Set(["leetcode/02 Two Pointers/valid-palindrome"]);
  assert.equal(taskDone(plan.days[1].tasks[0], solved), true);   // new problem: done once solved
  assert.equal(taskDone(plan.days[1].tasks[2], solved), false);  // review: needs a tick
  assert.equal(taskDone({ ...plan.days[1].tasks[0], done: false }, solved), false); // an untick wins over "solved"
  assert.throws(() => validatePlan({ days: [] }, titles, "2026-10-24", "2026-11-20"));
});

test("solving a problem completes its plan tasks (reviews only once due)", async () => {
  const { completeTasks, readPlan, savePlan } = await import("./plan.ts");
  const { localDate } = await import("./content.ts");
  const p = "leetcode/01 T/a", today = localDate(new Date()), later = "2999-01-01";
  await savePlan({ title: "t", created: "", days: [
    { date: today, tasks: [{ type: "leetcode", path: p, title: "A", done: false }, { type: "review", path: p, title: "A" }, { type: "note", text: "x" }] },
    { date: later, tasks: [{ type: "review", path: p, title: "A" }, { type: "leetcode", path: "leetcode/01 T/b", title: "B" }] },
  ] });
  await completeTasks(p);
  const plan = (await readPlan())!;
  assert.deepEqual(plan.days[0].tasks.map((t) => t.done), [true, true, undefined]); // even after an earlier untick
  assert.deepEqual(plan.days[1].tasks.map((t) => t.done), [undefined, undefined]);  // future review and other problems untouched
});

test("login opens the right terminal on each OS", async () => {
  const { loginTerminal } = await import("./claude.ts");
  const none = () => false;
  assert.equal(loginTerminal("darwin", none, "claude")!.cmd, "osascript");
  assert.match(loginTerminal("darwin", none, "claude")!.args[1], /do script "claude auth login"/);
  assert.deepEqual(loginTerminal("win32", none, "claude"), { cmd: "cmd.exe", args: ["/c", "start", "Claude login", "cmd.exe", "/k", "claude auth login"] });
  assert.deepEqual(loginTerminal("linux", (c) => c === "konsole" || c === "xterm", "claude"), { cmd: "konsole", args: ["-e", "claude", "auth", "login"] });
  assert.equal(loginTerminal("linux", none, "claude"), null); // no terminal: the page shows the command instead
});

test("model choice is saved and validated", async () => {
  const { saveModel, savedModel } = await import("./claude.ts");
  assert.equal(await savedModel(), "");
  await saveModel("claude-sonnet-5-5");
  assert.equal(await savedModel(), "claude-sonnet-5-5");
  await assert.rejects(saveModel("sonnet")); // only exact IDs from the list
  const { write } = await import("./content.ts");
  await write("settings.json", JSON.stringify({ model: "haiku" })); // a pick saved before IDs were used
  assert.equal(await savedModel(), "claude-haiku-5-5");
  await assert.rejects(saveModel("gpt-4"));
  await saveModel("");
  assert.equal(await savedModel(), "");
});

test("API only accepts local, same-origin requests", async () => {
  const { foreignRequest } = await import("./guard.ts");
  const check = (method: string, h: Record<string, string>) => foreignRequest(method, new Headers(h));
  assert.equal(check("POST", { host: "127.0.0.1:3000", origin: "http://127.0.0.1:3000", "sec-fetch-site": "same-origin" }), null);
  assert.equal(check("GET", { host: "localhost:3000" }), null);
  assert.equal(check("POST", { host: "127.0.0.1:3000", origin: "https://evil.example" }), "cross-site request");
  assert.equal(check("POST", { host: "127.0.0.1:3000", "sec-fetch-site": "cross-site" }), "cross-site request");
  assert.equal(check("GET", { host: "evil.example:3000" }), "not a local address"); // DNS rebinding
});


test("moving a problem to another topic carries its progress, plan tasks and topic label", async () => {
  const { moveProblem, write, read, progress, setProgress } = await import("./content.ts");
  const from = "leetcode/01 T/mv";
  await write(`${from}/question.md`, '---\ntopic: "T"\n---\n# Mv\n\n**Topic:** T · **Difficulty:** Easy\n');
  await write(`${from}/attempt.py`, "x = 1\n");
  await setProgress(from, "solved");
  await write("plan.json", JSON.stringify({ days: [{ date: "2026-01-01", tasks: [{ type: "leetcode", path: from }] }] }));
  const to = await moveProblem(from, "05 Graphs");
  assert.equal(to, "leetcode/05 Graphs/mv");
  assert.equal(await read(`${to}/attempt.py`), "x = 1\n");
  assert.equal(await read(`${from}/question.md`), null);
  assert.match((await read(`${to}/question.md`))!, /topic: "Graphs"[\s\S]*\*\*Topic:\*\* Graphs ·/);
  assert.equal((await progress())[to].status, "solved");
  assert.equal((await progress())[from], undefined);
  assert.match((await read("plan.json"))!, /leetcode\/05 Graphs\/mv/);
  await assert.rejects(moveProblem(to, "../escape"));
});

test("plan progress reads how far the streamed plan JSON has got", async () => {
  const { planProgress } = await import("./plan.ts");
  const partial = '```json\n{"title":"x","days":[{"date":"2026-10-24","focus":"Arrays","tasks":[]},{"date": "2026-10-25","focus":"Two Poin';
  assert.deepEqual(planProgress(partial, 56), { days: 2, total: 56, date: "2026-10-25", focus: "Arrays" });
  assert.deepEqual(planProgress("", 7), { days: 0, total: 7, date: undefined, focus: undefined });
});

test("adding to a plan day: unsolved as new work, solved as a review; remove drops it", async () => {
  const { addTask, removeTask, savePlan } = await import("./plan.ts");
  await write("leetcode/09 P/x/question.md", "# Ay\n");
  await write("leetcode/09 P/y/question.md", "# Bee\n");
  await write("system-design/01 C/s/question.md", "# Sys\n");
  await setProgress("leetcode/09 P/y", "solved");
  await savePlan({ title: "t", created: "", days: [{ date: "2026-10-26", tasks: [{ type: "note", text: "x" }] }] });
  await addTask("2026-10-26", "leetcode/09 P/x");
  const plan = await addTask("2026-10-26", "leetcode/09 P/y");
  assert.deepEqual(plan.days[0].tasks.slice(1), [{ type: "leetcode", path: "leetcode/09 P/x", title: "Ay" }, { type: "review", path: "leetcode/09 P/y", title: "Bee" }]);
  await assert.rejects(addTask("2026-10-26", "leetcode/09 P/nope"));
  await assert.rejects(addTask("2026-12-01", "leetcode/09 P/x"));
  assert.deepEqual((await addTask("2026-10-26", "mock:coding")).days[0].tasks.at(-1), { type: "mock", kind: "coding" });
  assert.deepEqual((await addTask("2026-10-26", "mock:coding", "leetcode/09 P/x")).days[0].tasks.at(-1), { type: "mock", kind: "coding", path: "leetcode/09 P/x", title: "Ay" });
  await assert.rejects(addTask("2026-10-26", "mock:system-design", "leetcode/09 P/x")); // wrong kind for that problem
  assert.equal((await removeTask("2026-10-26", 0)).days[0].tasks.length, 4);
  await setProgress("leetcode/09 P/y", null);
});

test("mock interview length follows the kind and difficulty", async () => {
  const { interviewMinutes, difficultyOf } = await import("./interview.ts");
  assert.equal(interviewMinutes("coding", difficultyOf("---\ndifficulty: Easy\n---\n# X")), 15);
  assert.equal(interviewMinutes("coding", "Medium"), 30);
  assert.equal(interviewMinutes("coding", "Hard"), 45);
  assert.equal(interviewMinutes("system-design", difficultyOf('---\ndifficulty: "Hard"\n---')), 60);
  assert.equal(interviewMinutes("coding", undefined), 45); // interviewer picks
  assert.equal(interviewMinutes("system-design", "weird"), 45);
});

test("plans from Claude keep mock interviews and drop unknown tasks", async () => {
  const { validatePlan } = await import("./plan.ts");
  const titles = new Map([["leetcode/01 A/two-sum", "Two Sum"]]);
  const plan = validatePlan({ days: [{ date: "2026-11-02", tasks: [{ type: "mock", kind: "system-design" }, { type: "mock" }, { type: "mock", kind: "coding", path: "leetcode/01 A/two-sum" }, { type: "mock", kind: "system-design", path: "leetcode/01 A/two-sum" }, { type: "bogus" }] }] }, titles, "2026-11-01", "2026-11-30");
  assert.deepEqual(plan.days[0].tasks, [{ type: "mock", kind: "system-design" }, { type: "mock", kind: "coding" }, { type: "mock", kind: "coding", path: "leetcode/01 A/two-sum", title: "Two Sum" }, { type: "mock", kind: "system-design" }]);
});

test("coverAll adds every missing problem, spread over the days in order", async () => {
  const { coverAll } = await import("./plan.ts");
  const plan = { title: "t", created: "", days: [1, 2, 3, 4].map((n) => ({ date: `2026-11-0${n}`, tasks: [] as never[] })) } as import("./plan.ts").Plan;
  plan.days[0].tasks.push({ type: "leetcode", path: "a", title: "A" } as never);
  const req = ["a", "b", "c", "d", "e"].map((p) => ({ type: "leetcode" as const, path: p, title: p.toUpperCase() }));
  coverAll(plan, [...req, { type: "review", path: "a", title: "A" }]);
  const where = plan.days.map((d) => d.tasks.map((t) => ("path" in t ? `${t.type[0]}:${t.path}` : "")).join(","));
  assert.deepEqual(where, ["l:a,l:b,l:c", "l:d", "l:e", "r:a"]); // b..e and the review of a, in order, evenly spread
});
