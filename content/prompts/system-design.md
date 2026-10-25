You are adding a system design interview problem to a study app.

Request: {{request}}
Category: {{category}}
(If the request names a known problem, e.g. "Design Uber", cover that one. If it is an idea, design an original prompt around it.)

Match the style of a Hello Interview breakdown: concrete numbers, clear trade-offs, no fluff.
If the category is ML system design, keep question.md as below but give solution.md these sections instead:
1. Problem framing · 2. Business objective → ML objective · 3. High-level design · 4. Data and labels · 5. Features ·
6. Modelling (baseline → stronger model, loss) · 7. Evaluation (offline and online) · 8. Deployment and monitoring ·
9. Deep dives · 10. What interviewers look for · 11. Common pitfalls.
Write exactly two files (no text outside the file sections):

=== FILE: question.md ===
---
topic: "{{category}}"
difficulty: Easy | Medium | Hard
problem: "<Short name>"
video: <a Hello Interview YouTube URL only if you are certain it exists, otherwise omit the line>
---
# Design <X>

**Topic:** {{category}} · **Difficulty:** <difficulty>

## Prompt

## Requirements to pin down (ask the interviewer)

## Scale hints

## Think about before opening the answer

1. ...

## Self-check

- [ ] ...

=== FILE: solution.md ===
---
(same frontmatter)
---
# Design <X> – Solution

## 1. Requirements
(Functional / Non-functional / Out of scope)

## 2. Back-of-envelope

## 3. Core entities and API

## 4. High-level design
(include a component diagram as an ASCII box-and-arrow sketch in a ```text block)

## 5. Deep dives

## 6. What interviewers look for

## 7. Common pitfalls
=== END ===
