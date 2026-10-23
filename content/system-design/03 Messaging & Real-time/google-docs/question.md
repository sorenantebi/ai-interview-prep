---
topic: "Messaging & Real-time"
difficulty: Hard
problem: "Google Docs"
---
# Design Google Docs (Collaborative Document Editing)

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Answer:** Google Docs - Solution

## Prompt

Design a web-based collaborative text editor. Many users can open the same document and type simultaneously. Everyone sees the others' changes within a fraction of a second, cursors are visible, and all participants converge to exactly the same final text, even if they type at the same position at the same time.

## Requirements to pin down (ask the interviewer)

- Plain text or rich text (bold, lists, images, tables)?
- How many simultaneous editors per document? How many documents overall?
- Offline editing and later merge? Version history and undo?
- Sharing and permissions (view/comment/edit)?

## Scale hints

- ~1B documents, ~100M daily active users
- Typical document has 1-5 editors; some have **100+ concurrent editors**
- Keystroke-to-screen latency for collaborators: < 100-200 ms
- Document size up to a few MB of text; millions of edits per second across the fleet

## Think about before opening the answer

1. If two users edit the same sentence at once, how do you make both replicas end up identical? Why does "last write wins" on the whole document fail?
2. What do you send over the network: the whole document, a diff, or an operation? What is an operation?
3. What are the two classic algorithm families for this (and how do they differ in where the complexity lives)?
4. How do you route all editors of one document to the same server, and what happens when that server dies?
5. How do you store a document so that loading is fast but history is preserved?
6. How do you handle an editor that is offline for ten minutes?

## Self-check

- [ ] I can walk through a concrete concurrent-insert example and show convergence
- [ ] I can compare OT and CRDT with their trade-offs
- [ ] I can explain the per-document single-writer design and its failover
- [ ] I can describe the operation log plus snapshot storage model
