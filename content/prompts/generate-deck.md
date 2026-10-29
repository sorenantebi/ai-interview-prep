You write flashcards for someone preparing for software engineering interviews (coding, C++, system design, ML).

Write {{count}} flashcards about: {{topic}}

Good cards:
- One fact, idea or trade-off per card, so it can be answered in under a minute.
- The front is a specific question ("Why is `std::vector::push_back` amortised O(1)?"), not a topic ("Vectors").
- The back answers it in one to four short lines; a small code block only when it is the answer.
- Correct and current. If something depends on the language version or the system, say which.
- Cover the topic from basics to the things interviewers dig into; no two cards ask the same thing.

The deck already has these cards (don't repeat them):
{{existing}}

Answer with one file and nothing else, in exactly this format: a `# ` title line (a short deck name for the topic), then each card as a `## ` line with the front (more front lines may follow), a line `### Answer`, then the back. Don't use `## ` or `# ` headings anywhere else.

=== FILE: deck.md ===
# C++ Move Semantics

## What does `std::move` actually do?
### Answer
Nothing at runtime: it's a cast to an rvalue reference (`static_cast<T&&>`), which lets overload resolution pick the move constructor or move assignment.

## What state is a moved-from `std::string` in?
### Answer
Valid but unspecified: you may assign to it or destroy it, but don't rely on its value.
=== END ===
