---
video: https://www.youtube.com/watch?v=krsuaUp__pM
topic: "Search & Analytics"
difficulty: Medium
problem: "Web Crawler"
---
# Design a Web Crawler

**Topic:** Search & Analytics · **Difficulty:** Medium · **Answer:** Web Crawler - Solution

## Prompt

Design a web crawler that starts from a set of seed URLs, downloads pages, extracts the links inside them, and keeps going. The downloaded content will be used to train an LLM / build a search index, so the crawler is the data-collection layer, not the consumer.

## Requirements to pin down (ask the interviewer)

- What content do we need: HTML only, or also images, PDFs, JavaScript-rendered pages?
- Is this a one-off crawl or does it run continuously (re-crawling for freshness)?
- Must we respect `robots.txt` and per-site rate limits?
- How are crawled pages consumed downstream (just stored, or also indexed)?
- Is the whole web in scope, or a restricted set of domains?

## Scale hints

- ~10B pages to be crawled, finishing within about 5 days
- Average page is roughly 2 MB; only the text is needed downstream
- The crawl must be fault tolerant: machines will die mid-crawl and progress must not be lost
- Efficiency matters: no repeated fetches of the same URL or the same content
- We must be polite: never hammer a single website

## Think about before opening the answer

1. What is the crawl loop, and which components does it need?
2. How do you avoid fetching the same URL (or the same content under a different URL) twice?
3. How do you stay polite (robots.txt, per-domain rate) to a host while 1,000 machines are crawling in parallel?
4. What happens when a fetcher crashes halfway through a page? What happens on a transient 503?
5. Where does the bottleneck sit (bandwidth, DNS, parsing), and how many machines do you need to hit 5 days?
6. How would you detect crawler traps, such as infinite calendars or session-id URLs?
7. How would you extend it to re-crawl pages and to handle JavaScript-heavy sites?

## Self-check

- [ ] I can estimate pages per second, bandwidth and storage
- [ ] I can design a frontier that supports both priority and per-host politeness
- [ ] I can explain URL-level and content-level deduplication with memory estimates
- [ ] I can describe retry, DLQ and checkpoint behaviour
