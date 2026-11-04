---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/accounts-merge/
neetcode: https://neetcode.io/problems/accounts-merge
---
# Accounts Merge - Solution

## Intuition

Treat each account as a node. Two accounts are connected if they share an email, and connectivity is transitive, so each connected component is one person. Union-Find groups accounts into components efficiently: while scanning emails, remember which account first claimed each email, and union with that account whenever the email appears again.

## Approach

1. Create a Union-Find over account indices `0..n-1`.
2. Walk through every account and each of its emails. If the email was seen before in account `j`, union the current account with `j`. Otherwise record the current account as the email's owner.
3. Group every email under the root of its owner account.
4. For each group, output the name of the root account followed by the sorted emails.

## Code

```python
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.rank = [1] * n
    
    def find(self, x):
        while x != self.par[x]:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x
    
    def union(self, x1, x2):
        p1, p2 = self.find(x1), self.find(x2)
        if p1 == p2:
            return False
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
            self.rank[p1] += self.rank[p2]
        else:
            self.par[p1] = p2
            self.rank[p2] += self.rank[p1]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        emailToAcc = {} # email -> index of acc

        for i, a in enumerate(accounts):
            for e in a[1:]:
                if e in emailToAcc:
                    uf.union(i, emailToAcc[e])
                else:
                    emailToAcc[e] = i

        emailGroup = defaultdict(list) # index of acc -> list of emails
        for e, i in emailToAcc.items():
            leader = uf.find(i)
            emailGroup[leader].append(e)

        res = []
        for i, emails in emailGroup.items():
            name = accounts[i][0]
            res.append([name] + sorted(emailGroup[i])) # array concat
        return res
```

## Complexity

- **Time:** `O(E · α(N) + E log E)` — `E` is the total number of emails and `N` the number of accounts. Union-Find operations are near-constant amortized, and sorting each group's emails costs `O(E log E)` overall (times the email length for string comparisons).
- **Space:** `O(E + N)` — the owner map, the groups, and the parent array.

## Other Approaches

- **DFS/BFS on an email graph:** connect emails within the same account, then collect each connected component and sort it — Time `O(E log E)` / Space `O(E)`
- **Union-Find on emails:** union all emails of an account together, then group by root and attach the name — Time `O(E · α(E) + E log E)` / Space `O(E)`
