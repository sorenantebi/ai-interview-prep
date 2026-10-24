---
topic: "ML System Design"
difficulty: Medium
problem: "Bot Detection"
---
# Design Bot Detection – Solution

**Topic:** ML System Design · **Difficulty:** Medium · **Question:** Bot Detection - Question

## 1. Problem framing

**Clarified assumptions**
- Prevalence: unchecked, bots can be 50%+ of actions; existing simple heuristics cut this to < 1%. We work on what gets past them.
- False positives hurt: real users get turned away and engage less. Appeals exist but are costly to review, and bot operators use them too.
- Detect as early as possible.
- ~500M DAU × 1-2 sessions/day → billions of actions to evaluate.
- Old bots were obvious (inhuman request rates); new ones are much harder to spot and adapt to our defences.
- Ground truth comes from expensive **investigators**: a few hundred accounts per week.

**Takeaways to say out loud**
- **Adversarial:** attackers adapt, so today's patterns stop working tomorrow.
- **Compute-bound:** the system sits in front of many surfaces at very high volume. (Stopping bots often saves more compute than it costs, but that's no excuse for waste.)
- **Labels are scarce and expensive.**

## 2. Business objective → ML objective

| Objective | Verdict |
|---|---|
| Bad: maximize bot accounts detected | Rewards over-flagging; real users get banned and leave |
| Bad: maximize accuracy | Users feel spam and wrongful bans, not accuracy; on skewed classes the number is meaningless |
| Good: maximize detection rate subject to an FPR cap (e.g. < 1%) | Captures the core tension, but treats a harmless bot the same as one spreading malware |
| **Great: minimize bot impact on legitimate users' experience, with guardrails** | Targets why we care: spam impressions, spam friend requests, etc. Harder to define and keep up to date; overlaps with other systems (e.g. low-quality content isn't always bots) |

**Chosen:** minimize bot impact on real users, subject to a false-positive guardrail.

**ML objective:** binary classification at the **account** level: `P(bot | account)`.

## 3. High-level design

Two complementary tracks plus a graded response:

```
             ┌─► supervised model + nearest-neighbour lookups ─┐   (known bot patterns,
 account ────┤        (high precision)                         ├─► calibration ─► action
 events      └─► unsupervised anomaly detection ──────────────┘   (unknown patterns)

 action = ban (confident) | demote visibility | rate-limit interactions (uncertain)
```

- **Known patterns:** supervised model and non-parametric (kNN/ANN) matching against previously seen bots. Covers the easy vectors with high precision.
- **Unknown patterns:** unsupervised anomaly detection (deep dive §9).
- **Soft actions** (demotion, rate limits) shrink the damage of a false negative without the cost of a false-positive ban.
- **Caution with non-parametric indexes:** what you index drives results. If system-generated labels feed back into the index, you can drift into indexing more and more benign accounts. Keep investigator labels separate from system labels and weight them higher.

## 4. Data and labels

**Ground truth (investigators, hundreds/week)**
- Use for: test sets that reflect real sophistication, edge-case validation, threshold calibration.
- Spend the budget wisely: **active learning**, sending accounts near the decision threshold or showing new patterns.

**User-generated signals (noisy, millions)**
- Account reports ("this looks fake").
- **Appeal outcomes:** successful appeals are high-confidence *negatives*.
- Spam/abuse reports on content often point at bot authors.

**Network-derived labels**
- IPs from past bot campaigns, near-identical behaviour to confirmed bots, bulk registrations from the same source (bot farms).
- Finds whole networks, but errors can propagate through the graph, so be careful.

**Synthetic data**
- Bots may be < 1% of cleaned data. Conditional GANs (e.g. CALEB) can generate realistic bot timelines, content style and network growth to fill gaps.

**Survivorship bias:** better detection removes easy bots, so the bots left in our data keep getting harder. Good for training hard cases, bad for stable distributions.

## 5. Features

Aim for both easy wins (today's bots) and signals that are hard to fake (tomorrow's). Interviewers mostly judge instincts, not trust and safety expertise.

**Activity patterns** (hand-engineered because running sequence models on every action is too expensive)
- Inter-event time distributions (posts, likes, comments); variance of reaction times.
- Error behaviour: typos and corrections (humans make mistakes).
- Session length/frequency; circadian rhythm (humans sleep); bursts beyond human speed.
- Compute over several windows (hour/day/week); summarize with entropy/variance ("how human is this?").

**Content signals** (weakest, easiest to fake)
- Semantic diversity, near-duplicate content (embedding similarity), language quality.
- Keep an **ANN index of known bot content**; feed "distance to / count of nearby bot posts" as a feature. Adapts to new campaigns without retraining.
- Attackers see which content gets removed and shift to what doesn't. Timing signals are harder to game.

**Network topology**
- Follower/following ratio, speed of connection growth, clustering coefficient, plus graph embeddings.

**Account metadata**
- Account age, verification, profile completeness; login frequency, device diversity, location consistency; username patterns, profile photo, bio.

**Interaction with our defences**
- Prior flags across models, behaviour change after being flagged, appeal frequency/success. Evasion itself becomes a signal.

> **Often missed:** many features don't exist at signup. The model must handle missing values, and new vs established accounts may need different feature sets.

## 6. Modelling

Integrity systems grow over time in response to attacks: start simple, find gaps, add layers (**defence in depth**).

**Baseline:** logistic regression on simple signals (post frequency, friend-request ratio, login geography). Trains in minutes, scores in microseconds, and later serves as a **canary** for regressions.

| Option | Notes |
|---|---|
| Bad: one big content-focused multi-modal model | Very expensive per post, and ignores the strongest signals (session rhythm, IP hopping, follow bursts). Bot detection is about **behaviour**, not content |
| **Good: graph + sequence model** | Graph view catches coordinated botnets; sequence view catches single-account automation. No need to parse every image/text |

**Architecture**
- **Graph branch:** **GraphSAGE** on a 2-hop neighbourhood. *Inductive* (new accounts get embeddings without retraining), cost grows with sampled neighbours. Relation-specific weights so a "follow" edge differs from a "reply" edge (auto-followers don't look like community members). **Neighbour sampling** caps celebrity fan-out.
- **Sequence branch:** last ~200 events, timestamps bucketed into 5-minute slots, embedded event types (post, like, login, device switch, …) → small **bidirectional GRU**. A transformer works too, but it's overkill: we're modelling suspicious rhythms, not language.
- **Fusion:** one cross-attention layer between the two branch outputs ("does anyone in my cluster act with this cadence?"), then a small MLP (64 → 32 → 1) → raw risk score.

```
k-hop subgraph ─► GraphSAGE ─┐
                             ├─► cross-attention ─► MLP(64→32→1) ─► score ─► calibration
event sequence ─► BiGRU ─────┘
```

**Pretraining (self-supervised, then a light fine-tune)**
Big model + few labels + one binary target = overfitting. So pretrain each branch on unlabelled data:
- **Graph:** mask node attributes (age, country), drop edges, mix in fake neighbour pairs; the encoder reconstructs or discriminates. It learns what tight communities vs star-shaped follow farms look like.
- **Sequence:** 30-60 days of events; mask ~20% of tokens and reconstruct, predict the next event, and **contrastive** same-user session halves vs other users. It learns human rhythms (sleep, breaks, device switches) and notices "too fast / too regular".
- **Alignment:** label-free pass where the fusion layer is rewarded when the graph and sequence embeddings of the same account agree.
- **Fine-tune:** freeze most layers, train on a few thousand trusted labels, then calibrate.

**Loss:** weighted BCE where each sample's weight reflects how many real users the account could affect, **capped** so one viral spammer doesn't dominate gradients.

## 7. Inference

**Scaling (billions of actions/day)**
- Quantization-aware training.
- **Caching:** graph embeddings for a short TTL (invalidate on big neighbourhood changes); reuse activity-sequence encodings.
- **Two-stage cascade:** cheap logistic-regression filter (posting frequency, account age, device patterns) clears obvious humans; the heavy graph-sequence model only sees the rest. Train the filter as a **student of the heavy model** so it targets "would the heavy model act?". Cuts compute substantially (source cites ~80-90%), and the stage-1 threshold is a dial for capacity.

**Triggers** (run the light model on)
- Registration (metadata + first actions)
- Activity thresholds crossed (mass follows, rapid posting)
- Network changes (joins a known bot cluster, coordinated behaviour)
- User reports (priority re-score)

Re-scoring is cheap: update behavioural inputs, reuse the cached graph embedding if the neighbourhood is stable.

**Data pitfalls**
- **Positive suppression:** bots get removed before showing full behaviour, so the model may learn "rich behavioural history ⇒ human".
- **Survivorship bias:** remaining bots are increasingly sophisticated; keep adapting.
- **Fix: holdouts.** A small unenforced slice collects unbiased data and hides from attackers whether their probes triggered us. Guard against attackers exploiting the holdout.

## 8. Evaluation

**Offline**
- **Precision @ Recall 90** (tied to the action threshold) and **PR-AUC** (stable overall signal).
- **Impact-weighted** metrics: weight by followers/activity (potential exposure).
- Diagnostics: **early detection rate** (caught in first 24h), **network coverage** (share of bot clusters found).
- **Time-split validation sets** so you test on future behaviour: drift is the main threat.
- **Fairness:** slice by geography/demographics so legitimate users from specific communities aren't hit harder.
- **Adversarial robustness:** maintain a red-team set of sophisticated/evasive bot patterns.

**Online (A/B)**
- Control vs candidate, only one acts. They flag different accounts → need fresh labels.
- **Importance sampling** by score: oversample the boundary where models disagree, downsample near-0/near-1 and reweight, prioritize high-impact accounts.
- Proxies: bot/spam/fake-account reports, appeal success rate, friend-request acceptance and message response rates.
- Primary metric: **bot interactions per legitimate user** (requests, messages, views) with **< 1% FPR** on restrictions.

## 9. Deep dives

### 9.1 Calibration

Raw scores aren't probabilities (0.6 ≠ 60% bots). Calibrate to hit guardrails and to keep enforcement stable when a new model with a different score distribution ships.

| Method | Notes |
|---|---|
| Good: histogram binning | Fixed buckets, each mapped to its observed positive rate. Simple, easy to explain |
| Good: isotonic regression | Monotonic piecewise-constant fit. Flexible but needs more labels than we have |
| **Great: Platt scaling** | Fit a 2-parameter sigmoid on a holdout. Works with scarce labels and few points of interest on the curve |

### 9.2 Anomaly detection (unknown unknowns)

| Method | Strengths | Weaknesses |
|---|---|---|
| Good: isolation forest | Random splits isolate outliers in few steps (short path = anomaly). Cheap, scales to many features, no distribution assumptions, tolerates missing values | Misses contextual anomalies; coordinated bots that look alike aren't "few and different" |
| Good: autoencoder | High reconstruction error = unusual. Captures temporal/sequential patterns and subtle shared campaign signatures | More expensive; depends on choice of reconstruction loss; may learn to reconstruct anomalies too |
| **Great: ensemble** | Isolation forest screens metadata/basic activity fast; autoencoder on survivors for sequence patterns; learned weighting of scores | More moving parts |

- Isolation forests suit the needle-in-a-haystack case; new positives they surface (after investigator review) **bootstrap the supervised model**.
- Only act on accounts that are anomalous **and** causing harm that matters for the objective. Weird ≠ bot.

## 10. What interviewers look for

- **Mid-level:** a workable end-to-end design with sensible choices, good instincts on data/features, spots obvious problems.
- **Senior:** reaches a working design quickly, then goes deep (sequence model, anomaly detection), picks the right model family, reasons carefully about objective and evaluation, says where their experience runs out.
- **Staff:** owns objective-to-model trade-offs, capacity and optimization, realistic attacker vulnerabilities and mitigations, leads their own deep dives, and keeps everything tied to user impact rather than raw accuracy.

## 11. Common pitfalls

- Reaching for a giant content LLM when behaviour and graph signals matter most
- Treating it as a static problem: no time-split eval, no drift plan, no holdouts
- Ignoring missing features for brand-new accounts
- Mixing system-generated labels with investigator labels at equal weight (runaway feedback)
- Binary ban/no-ban only, with no soft actions for uncertain cases
- Leaning on content features that attackers can trivially change

Source: summarized from [Hello Interview: Bot Detection](https://www.hellointerview.com/learn/ml-system-design/problem-breakdowns/bot-detection) and its video walkthrough.
