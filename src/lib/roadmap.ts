// NeetCode roadmap layout: [x, y] in grid units.
export const LAYOUT: Record<string, [number, number]> = {
  "Arrays & Hashing": [3, 0],
  "Two Pointers": [2, 1], Stack: [4, 1],
  "Binary Search": [1, 2], "Sliding Window": [3, 2], "Linked List": [5, 2],
  Trees: [3, 3],
  Tries: [1, 4], "Heap - Priority Queue": [3, 4], Backtracking: [5, 4],
  Intervals: [0, 5], Greedy: [1.5, 5], "Advanced Graphs": [3, 5], Graphs: [4.5, 5], "1-D Dynamic Programming": [6, 5],
  "2-D Dynamic Programming": [4.5, 6], "Bit Manipulation": [6, 6],
  "Math & Geometry": [5.25, 7],
};
export const EDGES: [string, string][] = [
  ["Arrays & Hashing", "Two Pointers"], ["Arrays & Hashing", "Stack"],
  ["Two Pointers", "Binary Search"], ["Two Pointers", "Sliding Window"], ["Two Pointers", "Linked List"],
  ["Binary Search", "Trees"], ["Linked List", "Trees"],
  ["Trees", "Tries"], ["Trees", "Heap - Priority Queue"], ["Trees", "Backtracking"],
  ["Heap - Priority Queue", "Intervals"], ["Heap - Priority Queue", "Greedy"], ["Heap - Priority Queue", "Advanced Graphs"],
  ["Backtracking", "Graphs"], ["Backtracking", "1-D Dynamic Programming"],
  ["Graphs", "Advanced Graphs"], ["Graphs", "2-D Dynamic Programming"],
  ["1-D Dynamic Programming", "2-D Dynamic Programming"], ["1-D Dynamic Programming", "Bit Manipulation"],
  ["2-D Dynamic Programming", "Math & Geometry"], ["Bit Manipulation", "Math & Geometry"],
];
