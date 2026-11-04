---
video: https://www.youtube.com/watch?v=6st4IxEF-90
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/accounts-merge/
neetcode: https://neetcode.io/problems/accounts-merge
---
# Accounts Merge

**Topic:** Graphs · **Difficulty:** Medium

## Problem

You are given a list `accounts`. Each `accounts[i]` is a list of strings: the first element `accounts[i][0]` is a name, and the remaining elements are the emails belonging to that account.

Two accounts definitely belong to the same person if they share at least one email. Two accounts with the same name may still belong to different people, since different people can have the same name. A person can have any number of accounts, but all of their accounts have the same name.

Merge all accounts that belong to the same person. Return the merged accounts in this format: the first element is the name, and the remaining elements are the person's emails in sorted order. The merged accounts may be returned in any order.

## Examples

**Example 1**
```text
Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
```
The first and second "John" accounts share `johnsmith@mail.com`, so they are the same person. The third "John" and "Mary" share no emails with any other account, so they stay separate. The result may be returned in any order, e.g. `[["Mary","mary@mail.com"],["John","johnnybravo@mail.com"],["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"]]` is also accepted.

**Example 2**
```text
Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
```
No emails are shared, so no accounts are merged; only the emails within each account are sorted.

## Constraints

- `1 <= accounts.length <= 1000`
- `2 <= accounts[i].length <= 10`
- `1 <= accounts[i][j].length <= 30`
- `accounts[i][0]` consists of English letters.
- `accounts[i][j]` (for `j > 0`) is a valid email.
