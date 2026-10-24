---
topic: "ML System Design"
difficulty: Hard
problem: "Video Recommendations"
---
# Design Video Recommendations ("Up Next") – Solution

**Topic:** ML System Design · **Difficulty:** Hard · **Question:** Video Recommendations - Question

## 1. Problem framing

**Clarified scope**
- Surface: the "up next" list shown next to the video currently playing
- Catalog ~1B videos, ~1B DAU, ~5 slots per request, ~250 ms to render
- Context is the user's session and, above all, the video being watched right now

**Business objective (pick deliberately, it shapes every later choice)**

| Objective | Verdict |
|---|---|
| Bad: maximize CTR | Easy to measure, but rewards clickbait thumbnails/titles; users click, don't stay, and leave |
| Good: maximize total watch time | Fits an ad-funded platform and punishes clickbait; but can push long or addictive low-quality videos |
| Good: **quality-adjusted watch time** | Watch time weighted by quality signals (ratings, completion, shares): "time well spent". Still ignores creators/diversity |
| Great: long-term satisfaction and engagement | Balances users (satisfaction), platform (watch time → ad revenue) and creators (new creators get distribution, good ones get rewarded) |

- Working choice: **quality-adjusted watch time**, while mentioning the long-term version to show senior thinking.
- The objective also frames later deep dives (clickbait with poor retention, creator promotion, platform health).

## 2. ML objective

- **Ranking problem:** given (user, session, current video), order candidate videos by expected contribution to the objective.
- The ranker predicts several future behaviours: click, watch time, like, share, completion, return visit.
- A **value model** combines those predictions into one score; its weights are the knob that ties the ML system to the business objective.
- Scale forces a funnel: you cannot run a heavy model over 1B videos per request.

## 3. High-level design

```
 context (user, session, current video)
            │
            ▼
 ┌─────────────────────────────┐
 │ Candidate generators (~100s) │  ANN lookups, subscriptions, trending ...
 └─────────────────────────────┘  → O(10k) videos
            ▼
 ┌──────────────┐   cheap features, optimize RECALL
 │ Light ranker │  → O(100)
 └──────────────┘
            ▼
 ┌──────────────┐   full features, optimize PRECISION
 │ Heavy ranker │  → scored list (multi-task heads)
 └──────────────┘
            ▼
 ┌──────────────┐   value model, diversity, business rules
 │  Re-ranker   │  → final 5 slots
 └──────────────┘
```

- **Candidate generation:** many generators in parallel, some global ("top platform videos"), some personal ("from your subscriptions", "similar to this video"). Low-context generators are cacheable/precomputable, which is key for scaling.
- **Rule of thumb:** if a feature is informative for ranking, make sure some generator surfaces candidates along that axis.
- **Light ranker:** mostly a compute optimization; must not throw away good videos.
- **Heavy ranker:** where the quality comes from; learns user, video and interaction representations.
- **Re-ranking:** works on the whole slate: applies the value model, enforces diversity, handles new-creator boosts or viral content.
- Every stage can add bias or lose good items, so each stage needs its own monitoring (a common interviewer probe).

## 4. Data and labels

Group the data and give a few examples per group rather than listing everything.

**Explicit feedback** (high quality, sparse)
- Likes/dislikes, subscriptions, "not interested"
- Avoid relying on user-declared interests: stated and revealed preferences often diverge.

**Implicit feedback** (the bulk of the training data)
- Watch time, absolute and relative to video length
- Clicks, shares, whether the user comes back to the platform
- **Session abandonment** after a video is a strong (noisy) negative, stronger than simply skipping to another video.

**Context**
- Current video (creator, title, semantics), recent searches, previous videos in the session
- Time of day / day of week, device and form factor

## 5. Features

Each ranker sees two "legs": the **context** (current video, user profile/history) and each **candidate**. Organize features by update frequency to maximize caching.

**Video features** (apply to both the current video and candidates)
- *Content* (compute at upload/edit, cache long): title/description/tags, thumbnail vision features, audio features, quality metrics, topic embeddings
- *Engagement* (refresh often): views, likes, avg watch time, velocity, creator track record, monetization/advertiser-friendliness
- Normalize engagement for video age (compare to an expected growth curve); watch for "popular because popular" loops.
- Content alone is a weak predictor of enjoyment; behaviour signals usually dominate.

**User features**
- *Profile* (slow-moving): topic and language preferences, subscription embeddings, demographics if available
- *Behavioural* (fast-moving): recent watches/searches in the session, favourite creators/categories, time and device patterns

**Encoding:** for the light ranker, summarize watch history as averaged embeddings over a few windows (e.g. last 3, last 10); the heavy ranker consumes the full sequence. Say this proactively, interviewers like to probe it.

## 6. Modelling

### 6.1 Baselines
- Random blend of candidate-generator outputs, or simple collaborative filtering.
- Expected to lose, but they anchor ablations and the compute-vs-quality trade-off.

### 6.2 Candidate generation: two-tower retrieval
- Many generators are thin wrappers over a **vector DB**: query with an embedding (current video, user, last watched video) and take the top-K nearest neighbours.
- Train a **two-tower** model (user tower, video tower) on triplets `(user, positive, negative)` with a triplet loss:
  `L = max(0, margin + d(u, pos) − d(u, neg))`
- **Hard negatives** (videos the model thinks the user likes but they didn't) make the embeddings much sharper.
- Store the resulting embeddings in the vector DB for ANN lookups. Be ready to explain this concretely; hand-waving about "embeddings" is a red flag.

### 6.3 Light ranker
- Goals: high recall, low latency, high throughput.
- **GBDT** (XGBoost/LightGBM) on CPU: sub-ms per item, cheap to scale, strong on tabular rec features.
- Alternative: a skinny MLP distilled from the heavy ranker, reusing learned categorical embeddings (needs more GPU).

### 6.4 Heavy ranker options

| Option | Notes |
|---|---|
| Bad: plain MLP on concatenated features | Easy to ship; misses high-order feature interactions and sequence context, struggles with sparse inputs |
| Good: **DLRM** | Handles sparse (embeddings) and dense features in separate paths, then models their interactions; no notion of order, so can be stale/repetitive |
| Great: **transformer sequence ranker** | Attends over the user's action sequence and between history and candidate; captures long-term and temporal patterns; costlier, harder to debug, may need sparse attention / MoE to scale |

- Matrix factorization / classic CF is a fine baseline but no longer state of the art.

### 6.5 Heavy ranker architecture (multi-task)
- **Inputs:** embeddings for IDs (video, creator), normalized numeric features, history sequence with positional encoding, tokens marking action type (watch/like/share).
- **Interaction:** self-attention within history, cross-attention between history and candidate, FFN blocks, residuals + layer norm.
- **Heads:** watch time (regression), click, like, share, return visit (classification), completion rate (regression).
- **Why multi-task:** regularizes, adds auxiliary signal, helps cold start through correlated tasks, and every head becomes an input to the value model. Extra heads (e.g. subscribe-after-watch) can encode creator-growth goals.

### 6.6 Loss
- **Main term:** engagement log-loss weighted by watch time (absolute and relative).
- **Auxiliary terms:** weighted click, completion and satisfaction losses.
- **Position-bias correction:** reweight examples by the slot they were shown in.
- Total = weighted sum. Key point: logged data comes from the *current* recommender, so without debiasing the new model just learns to imitate the old one.

## 7. Serving

- The funnel itself is the main scaling lever: cheap broad retrieval, expensive narrow ranking.
- **Precompute and cache:** video embeddings, user embeddings, outputs of low-context generators.
- **Freshness:** online embedding/model updates (e.g. ByteDance Monolith-style) for fast-moving signals.
- **Model efficiency:** quantization to shrink memory; GPU/TPU for heavy-ranker throughput.

```
request ─► fetch cached features + embeddings ─► parallel generators (ANN, rules)
        ─► GBDT light ranker (CPU) ─► transformer heavy ranker (GPU)
        ─► re-rank with value model ─► 5 videos   (all within ~250 ms)
```

## 8. Evaluation

**Offline** (useful but imperfect: user behaviour keeps shifting)
- Per-head metrics for each prediction task (e.g. AUC/log-loss for classifiers, error for regressors)
- Ranking metrics on the final list: **NDCG, MAP, precision/recall**
- Slate **diversity** across videos and creators
- **Recall of candidate generators**, measured on unbiased items (outside the top window or outside that generator's scope)

**Online** (A/B test is the gold standard)
- Business: session watch time, return rate, long-term engagement, creator metrics
- UX: acceptance rate of recommendations, surveys, negative-feedback rate
- System: latency, throughput, utilization, error rate
- Beware **novelty effects**: a fresh set of videos lifts engagement temporarily; run long enough (or watch the trend) before calling a winner.

## 9. Deep dives

### 9.1 Feedback loops
- Problems: popularity bias (rich get richer), filter bubbles, creators optimizing for the algorithm instead of quality.
- Mitigations: counterfactual logging + **inverse propensity weighting**, exposure-penalized losses, slate-level diversity constraints, periodic training on uniformly sampled impressions.
- Monitor diversity and how success is distributed across creators.

### 9.2 Cold start
- **New users:** onboarding (pick channels/interests) plus coarse demographic clustering; recommend what worked for similar users, then personalize as data arrives.
- **New videos:** multimodal content features (thumbnail, title, transcript, frames); controlled exposure to a small, varied audience to collect early signal, then hand off to the behavioural models.

### 9.3 Explore / exploit
- Pure exploitation gets boring; too much exploration annoys users.
- Tools: contextual bandits, Thompson sampling, UCB, epsilon-greedy.
- Give each slot a risk budget: safe at the top, more exploration lower down; explore more for new users and in categories where a user's taste is still uncertain.
- Expect follow-ups on measuring exploration cost vs long-term gain, per-segment fairness, and the cost of tracking uncertainty for millions of items.

## 10. What interviewers look for

- **Mid-level:** the candidate generation → ranking split, common engagement signals as features, NDCG/MAP, awareness of scale.
- **Senior:** careful feature engineering (normalization, freshness), multi-stage trade-offs, caching / embedding compression / ANN, balancing engagement vs diversity vs creators, A/B testing and monitoring.
- **Staff+:** sets up the architecture quickly then drives into systemic issues: feedback loops, cold start, position bias and noisy labels, effects on the creator ecosystem; knows the bottleneck is often data and evaluation, not the model.

## 11. Common pitfalls

- Optimizing raw CTR and shipping a clickbait machine
- Trying to score the whole catalog with one model instead of a funnel
- Trusting user-declared interests over observed behaviour
- Ignoring that training data is produced by the old system (position/presentation bias)
- Hand-waving embeddings without explaining how they are trained
- Declaring A/B wins during the novelty bump

Source: summarized from [Hello Interview: Video Recommendations](https://www.hellointerview.com/learn/ml-system-design/problem-breakdowns/video-recommendations).
