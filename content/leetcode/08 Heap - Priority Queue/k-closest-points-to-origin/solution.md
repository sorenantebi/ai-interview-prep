---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/k-closest-points-to-origin/
neetcode: https://neetcode.io/problems/k-closest-points-to-origin
---
# K Closest Points to Origin - Solution

**Question:** K Closest Points to Origin - Question · **Difficulty:** Medium

## Intuition

We need the `k` smallest distances, not a full ordering. Keep a **max-heap of size `k`** keyed by squared distance: any point farther than the current worst of the best `k` is discarded. Squared distance preserves ordering, so `sqrt` is unnecessary.

## Approach

1. For each point compute `d = x*x + y*y`.
2. Push `(-d, x, y)` onto a heap (negated to make it a max-heap).
3. If the heap grows beyond `k`, pop — this removes the farthest point currently kept.
4. Return the coordinates left in the heap.

## Code

```python
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        minHeap = []
        for x, y in points:
            dist = (x ** 2) + (y ** 2)
            minHeap.append((dist, x, y))
        
        heapq.heapify(minHeap)
        res = []
        for _ in range(k):
            _, x, y = heapq.heappop(minHeap)
            res.append((x, y))
        return res
```

## Complexity

- **Time:** `O(n log k)` — each of the `n` points costs at most one push and one pop on a heap of size `k + 1`.
- **Space:** `O(k)` — the heap (output also `O(k)`).

## Other Approaches

- **Sort by distance:** `sorted(points, key=dist)[:k]` — Time `O(n log n)`, Space `O(n)`.
- **Quickselect on distance:** partition until the first `k` are the closest — Time `O(n)` average / `O(n^2)` worst, Space `O(1)` extra.

## Key Takeaway

For "k smallest", keep a max-heap of size `k` (and vice versa); compare squared distances to avoid floating point.

## C++

```cpp
/*
    Given array of points & an int k, return k closest points to (0, 0)
    Ex. points = [[1,3],[-2,2]], k = 1 -> [[-2,2]]

    Quickselect, partition until pivot = k, left side all < k

    Time: O(k log n)
    Space: O(n)
*/

// class Solution {
// public:
//     vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
//         priority_queue<pair<double, vector<int>>> pq;
//         for (int i = 0; i < points.size(); i++) {
//             double distance = sqrt(pow(points[i][0], 2) + pow(points[i][1], 2));
//             pq.push({distance, points[i]});
//             if (pq.size() > k) {
//                 pq.pop();
//             }
//         }
        
//         vector<vector<int>> result;
//         while(!pq.empty()) {
//             result.push_back(pq.top().second);
//             pq.pop();
//         }
        
//         return result;
//     }
// };
/*
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        int low = 0;
        int high = points.size() - 1;
        int pivotIndex = points.size();
        
        while (pivotIndex != k) {
            pivotIndex = partition(points, low, high);
            if (pivotIndex < k) {
                low = pivotIndex;
            } else {
                high = pivotIndex - 1;
            }
        }
        
        return vector<vector<int>>(points.begin(), points.begin() + k);
    }
private:
    int partition(vector<vector<int>>& points, int low, int high) {
        vector<int> pivot = points[low + (high - low) / 2];
        int pivotDistance = getDistance(pivot);
        
        while (low < high) {
            if (getDistance(points[low]) >= pivotDistance) {
                swap(points[low], points[high]);
                high--;
            } else {
                low++;
            }
        }
        
        if (getDistance(points[low]) < pivotDistance) {
            low++;
        }
        return low;
    }
    
    int getDistance(vector<int>& point) {
        return pow(point[0], 2) + pow(point[1], 2);
    }
};
*/

/*
// O(n logn) solution using sorting
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        vector<vector<int>> res(k);
        sort(points.begin(), points.end(), [](vector<int>& p1, vector<int>& p2){
            int dist_p1 = pow(p1[0],2) + pow(p1[1],2);
            int dist_p2 = pow(p2[0],2) + pow(p2[1],2);
            return dist_p1 < dist_p2;
        });
        copy(points.begin(), points.begin() + k, res.begin());
        return res;
    }
};
*/

// O(k logn) solution
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        vector<vector<int>> triples;
        for (auto& p : points)
            triples.push_back({p[0] * p[0] + p[1] * p[1], p[0], p[1]});
        // Min heap of vectors (triples). This constructor takes O(n) time (n = len(v))
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq(triples.begin(), triples.end());
        vector<vector<int>> res;
        while (k--){
            vector<int> el = pq.top();
            pq.pop();
            res.push_back({el[1], el[2]});
        }
        return res;
    }
};
```
