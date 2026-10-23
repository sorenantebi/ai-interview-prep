// One-off: builds content/ from the Obsidian vault. Usage: node scripts/seed-from-vault.mjs [vaultDir]
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const vault = process.argv[2] ?? path.join(os.homedir(), "Documents/Obsidian Vault/ML Prep");
const out = path.join(process.cwd(), "content");

const NEETCODE_150 = {
  "01 Arrays & Hashing": ["Contains Duplicate", "Valid Anagram", "Two Sum", "Group Anagrams", "Top K Frequent Elements", "Encode and Decode Strings", "Product of Array Except Self", "Valid Sudoku", "Longest Consecutive Sequence"],
  "02 Two Pointers": ["Valid Palindrome", "Two Sum II Input Array Is Sorted", "3Sum", "Container With Most Water", "Trapping Rain Water"],
  "03 Sliding Window": ["Best Time to Buy And Sell Stock", "Longest Substring Without Repeating Characters", "Longest Repeating Character Replacement", "Permutation In String", "Minimum Window Substring", "Sliding Window Maximum"],
  "04 Stack": ["Valid Parentheses", "Min Stack", "Evaluate Reverse Polish Notation", "Daily Temperatures", "Car Fleet", "Largest Rectangle In Histogram"],
  "05 Binary Search": ["Binary Search", "Search a 2D Matrix", "Koko Eating Bananas", "Find Minimum In Rotated Sorted Array", "Search In Rotated Sorted Array", "Time Based Key Value Store", "Median of Two Sorted Arrays"],
  "06 Linked List": ["Reverse Linked List", "Merge Two Sorted Lists", "Linked List Cycle", "Reorder List", "Remove Nth Node From End of List", "Copy List With Random Pointer", "Add Two Numbers", "Find The Duplicate Number", "LRU Cache", "Merge K Sorted Lists", "Reverse Nodes In K Group"],
  "07 Trees": ["Invert Binary Tree", "Maximum Depth of Binary Tree", "Diameter of Binary Tree", "Balanced Binary Tree", "Same Tree", "Subtree of Another Tree", "Lowest Common Ancestor of a Binary Search Tree", "Binary Tree Level Order Traversal", "Binary Tree Right Side View", "Count Good Nodes In Binary Tree", "Validate Binary Search Tree", "Kth Smallest Element In a Bst", "Construct Binary Tree From Preorder And Inorder Traversal", "Binary Tree Maximum Path Sum", "Serialize And Deserialize Binary Tree"],
  "08 Heap - Priority Queue": ["Kth Largest Element In a Stream", "Last Stone Weight", "K Closest Points to Origin", "Kth Largest Element In An Array", "Task Scheduler", "Design Twitter", "Find Median From Data Stream"],
  "09 Backtracking": ["Subsets", "Combination Sum", "Combination Sum II", "Permutations", "Subsets II", "Word Search", "Palindrome Partitioning", "Generate Parentheses", "Letter Combinations of a Phone Number", "N Queens"],
  "10 Tries": ["Implement Trie Prefix Tree", "Design Add And Search Words Data Structure", "Word Search II"],
  "11 Graphs": ["Number of Islands", "Max Area of Island", "Clone Graph", "Walls And Gates", "Rotting Oranges", "Pacific Atlantic Water Flow", "Surrounded Regions", "Course Schedule", "Course Schedule II", "Graph Valid Tree", "Number of Connected Components In An Undirected Graph", "Redundant Connection", "Word Ladder"],
  "12 Advanced Graphs": ["Reconstruct Itinerary", "Min Cost to Connect All Points", "Network Delay Time", "Swim In Rising Water", "Alien Dictionary", "Cheapest Flights Within K Stops"],
  "13 1-D Dynamic Programming": ["Climbing Stairs", "Min Cost Climbing Stairs", "House Robber", "House Robber II", "Longest Palindromic Substring", "Palindromic Substrings", "Decode Ways", "Coin Change", "Maximum Product Subarray", "Word Break", "Longest Increasing Subsequence", "Partition Equal Subset Sum"],
  "14 2-D Dynamic Programming": ["Unique Paths", "Longest Common Subsequence", "Best Time to Buy And Sell Stock With Cooldown", "Coin Change II", "Target Sum", "Interleaving String", "Longest Increasing Path In a Matrix", "Distinct Subsequences", "Edit Distance", "Burst Balloons", "Regular Expression Matching"],
  "15 Greedy": ["Maximum Subarray", "Jump Game", "Jump Game II", "Gas Station", "Hand of Straights", "Merge Triplets to Form Target Triplet", "Partition Labels", "Valid Parenthesis String"],
  "16 Intervals": ["Insert Interval", "Merge Intervals", "Non Overlapping Intervals", "Meeting Rooms", "Meeting Rooms II", "Minimum Interval to Include Each Query"],
  "17 Math & Geometry": ["Rotate Image", "Spiral Matrix", "Set Matrix Zeroes", "Happy Number", "Plus One", "Pow(x, n)", "Multiply Strings", "Detect Squares"],
  "18 Bit Manipulation": ["Single Number", "Number of 1 Bits", "Counting Bits", "Reverse Bits", "Missing Number", "Sum of Two Integers", "Reverse Integer"],
};

// Verified Hello Interview videos (Yelp and Online Auction are mock interviews, the rest are walkthroughs).
const VIDEOS = {
  "Bitly": "iUU4O1sWtJA", "Dropbox": "_UZ1ngy-kOI", "YouTube": "IUrQ5_g3XKs", "FB News Feed": "Qj4-GruzyDU",
  "Tinder": "18Fg5Akhkqw", "FB Live Comments": "LjLx0fCd1k8", "WhatsApp": "cr6p0n0N-VA", "Online Auction": "o8nSXW-B7Rw",
  "Uber": "lsKU38RKQSo", "Yelp": "yz1jtze4qr8", "Ticketmaster": "fhdPyoO6aXI", "Ad Click Aggregator": "Zcv_899yqhI",
  "FB Post Search": "l38XL9914fs", "Web Crawler": "krsuaUp__pM", "YouTube Top K": "y-tA2NW4LNY", "LeetCode": "1xHADtekTNg",
  "Rate Limiter": "MIJFyUPG4Z4",
};

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
export const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
// [[target|alias]] -> alias, [[target]] -> target; drop vault-only "Solve it in" lines
// Code (fenced or inline) is left alone so arrays like [[1]] survive.
const clean = (md) =>
  md.replace(/^\*\*Solve it in:\*\*.*\n\n?/m, "")
    .replace(/^## Starter Code & Test Cases$[\s\S]*/m, "") // always the last section; holds vault-only practice code
    .split(/(```[\s\S]*?```|`[^`\n]*`)/)
    .map((part, i) => i % 2 ? part : part
      .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, "$2")
      .replace(/\[\[([^\]]+)\]\]/g, "$1"))
    .join("").trimEnd() + "\n";

function copyProblem(srcDir, name, destDir) {
  fs.mkdirSync(destDir, { recursive: true });
  for (const [from, to] of [["Question", "question.md"], ["Solution", "solution.md"]]) {
    const f = path.join(srcDir, `${name} - ${from}.md`);
    if (fs.existsSync(f)) fs.writeFileSync(path.join(destDir, to), clean(fs.readFileSync(f, "utf8")));
  }
}

const missing = [];
let count = 0;
for (const [topic, names] of Object.entries(NEETCODE_150)) {
  const topicDir = path.join(vault, "Coding/Leetcode", topic);
  const available = new Map(fs.readdirSync(topicDir).map((d) => [norm(d), d]));
  for (const name of names) {
    const dir = available.get(norm(name));
    if (!dir) { missing.push(`${topic}/${name}`); continue; }
    copyProblem(path.join(topicDir, dir), dir, path.join(out, "leetcode", topic, slug(dir)));
    count++;
  }
}

const sdRoot = path.join(vault, "System Design/General System Design");
let sd = 0;
for (const cat of fs.readdirSync(sdRoot).filter((d) => /^\d\d /.test(d))) {
  for (const p of fs.readdirSync(path.join(sdRoot, cat)).filter((d) => !d.endsWith(".md"))) {
    const dest = path.join(out, "system-design", cat, slug(p));
    copyProblem(path.join(sdRoot, cat, p), p, dest);
    if (VIDEOS[p]) {
      const q = path.join(dest, "question.md");
      fs.writeFileSync(q, fs.readFileSync(q, "utf8").replace(/^---\n/, `---\nvideo: https://www.youtube.com/watch?v=${VIDEOS[p]}\n`));
    }
    sd++;
  }
}

for (const d of ["interviews", "notes", "repos"]) {
  fs.mkdirSync(path.join(out, d), { recursive: true });
  fs.writeFileSync(path.join(out, d, ".gitkeep"), "");
}
console.log(`leetcode: ${count}/150, system design: ${sd}`);
if (missing.length) console.log("missing:\n" + missing.join("\n"));
