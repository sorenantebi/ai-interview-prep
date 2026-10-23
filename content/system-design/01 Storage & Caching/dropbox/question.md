---
video: https://www.youtube.com/watch?v=_UZ1ngy-kOI
topic: "Storage & Caching"
difficulty: Medium
problem: "Dropbox"
---
# Design Dropbox (File Storage and Sync)

**Topic:** Storage & Caching · **Difficulty:** Medium · **Answer:** Dropbox - Solution

## Prompt

Design a cloud file storage and sync service like Dropbox. Users upload files from one device, see them appear on their other devices, download them again, and share folders with other users. Files can be very large (tens of GB), and users expect a small edit to a big file to sync quickly.

## Requirements to pin down (ask the interviewer)

- Which operations are in scope: upload, download, share with other users, automatic sync across devices (and out of scope: editing, previews, version history)?
- Maximum file size (up to ~50 GB)? Availability or consistency first? Are there offline edits, and what happens on conflicting edits?
- Do we need real-time collaborative editing (Google Docs style), or only file-level sync?
- Do we need to restore deleted files or previous versions?

## Scale hints

- ~500M registered users, ~100M daily active users
- Average user stores ~1 GB, max file size ~50 GB
- Many files are small and changed often; most stored bytes are cold
- Sync latency target: a change appears on another device in a few seconds
- Durability matters more than anything: losing a user's file is unacceptable

## Think about before opening the answer

1. What are the core entities (File, FileMetadata, User, shares), and why should file metadata and file bytes live in different systems?
2. How do you upload a 50 GB file over a flaky connection without starting over?
3. How can you sync a small edit to a large file without re-uploading all of it?
4. How does device B find out that device A changed something?
5. What happens when two devices edit the same file offline?
6. How do you keep storage cost under control across 500M users?
7. How do you make uploads and downloads fast, and how do you keep files secure (signed URLs, encryption)?

## Self-check

- [ ] I can estimate storage, metadata size and sync traffic
- [ ] I can explain chunking (bad / good / great upload approaches), content hashing and deduplication
- [ ] I can describe how clients learn about changes (push vs pull, cursors)
- [ ] I can describe a conflict policy and its trade-offs
