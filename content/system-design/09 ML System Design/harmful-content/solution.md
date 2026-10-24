---
topic: "ML System Design"
difficulty: Medium
problem: "Harmful Content Detection"
---
# Design Harmful Content Detection – Solution

**Topic:** ML System Design · **Difficulty:** Medium · **Question:** Harmful Content Detection - Question

## 1. Problem framing

**Clarified assumptions**
- Posts have text + images (video scoped out). We only score **posts**, but comments can be used as signal.
- Detect every policy category: nudity, violence, hate, terrorism, trafficking, …
- Actions: **auto-remove** when very confident, **demote** when likely harmful, **human review** for a small, capacity-limited queue.
- Auto-removal requires **≥ 95% precision**: wrongful takedowns push users away, but so does seeing too much harmful content.
- ~1B posts/day, prevalence < 1%. Start with ~50k labelled examples (balanced 50/50).
- Latency is ours to choose, but the longer harmful content stays up, the more harm.

**Takeaways to say out loud:** multi-modal binary classification, extreme class imbalance, a hard precision bar on the action threshold, and a big scale/compute constraint.

## 2. Business objective → ML objective

| Objective | Verdict |
|---|---|
| Bad: maximize harmful content removed | No precision/recall trade-off; rewards over-flagging and censoring benign posts |
| Bad: maximize model accuracy | Users don't feel "accuracy"; at < 1% prevalence a model predicting "benign" for everything is 99% accurate |
| Good: maximize removals subject to a precision guardrail | Has a built-in trade-off, but still counts posts rather than user harm |
| Great: minimize successful user reports of harmful content | User-centric and label-free; but reports are noisy and can be adversarial (reporting things you disagree with) |
| **Great: minimize views of harmful content, subject to a precision guardrail** | Measures actual exposure, prioritizes viral content; downside is it needs ongoing labelling to measure |

**Chosen:** minimize **harmful impressions**, subject to precision ≥ 95% for auto-removal.

- The objective answers design questions for you: "classify now or later?" → every minute of delay accrues views.
- **Key insight:** a post gets *easier* to classify as people see it (hides, angry reactions, "gross!" comments). Design to exploit this with re-scoring.

**ML objective:** binary classification `P(harmful | post, context)`; loss details come later.

## 3. High-level design

```
new post / behaviour update
        │
        ▼
 [classifier] ──► [calibration layer] ──► [action service]
   (score)        (score → probability,     ├─ p ≥ τ_remove (95% precision) → remove
                   thresholds per action)   ├─ τ_demote ≤ p < τ_remove      → demote
                                            └─ uncertain + high reach       → human review
```

- Score on creation, and **re-score** when new behavioural data arrives.
- The calibration layer is what guarantees the precision guardrail; the classifier alone does not.
- Keep the whiteboard light: it is a communication aid, not a graded artefact.

## 4. Data and labels

**Supervised (gold, small)**
- The 50k labelled set is the most valuable data. Public NSFW datasets can augment it, but they lack platform features and may add bias.
- Ask for a **stream of fresh labels**: harmful content drifts, and **hard cases** (near the boundary) are worth far more than obvious ones.
- "It tested well but degraded over time" usually means **data drift**.

**Semi-supervised (noisy, large)**
- **User reports** are a correlated proxy label, at much higher volume (think ~10M reports vs 50k labels). Useful for larger models.

**Self-supervised (huge)**
- Comments carry signal ("disgusting", "didn't want to see this"). Training a model to predict comments from the post yields better post representations than labels alone, and there are orders of magnitude more posts with comments than labels.
- Precedent: Facebook trained image models to predict Instagram hashtags; the embeddings transferred widely.

**Class imbalance**
- Raw distribution → model collapses to "benign". Use **balanced sampling** in training plus **loss weighting** to tune the precision/recall trade-off, then recalibrate to the real prevalence.

## 5. Features

**Content (first-class)**
- Concatenated text (body, hashtags, …) and the set of attached images. Let a strong model learn topics/hashtags implicitly instead of hand-engineering them.

**Behavioural (audience reactions)**
- Count of comments that signal harm, negative reactions (angry, hide), shares-to-views ratio.
- Normalize for post age: at T=0 every post has zero negative signal, which does **not** mean benign.
- Prefer rates (`negative_reactions_per_view`) and smooth them with a **Bayesian average** (prior + observed) so low-view posts don't get wild ratios:

```
smoothed_rate = (neg_count + prior_rate * k) / (views + k)
```

- Using these features forces two follow-ups (earmark them): how to put time-varying features into training data, and when to re-trigger the model.

**Creator**
- **User embeddings:** dense summary of a user's long-run profile and context (groups, follows). Good at averages, slow to change. Training them is a deep dive (§9).
- **Real-time tallies:** recent reports, dislikes, shares, normalized for account age and activity. Catch sudden behaviour change (e.g. a hacked account).
- Account-risk signals: `account_age`, `number_of_login_countries` (hacked accounts and bots are common sources).
- Slow-but-rich embeddings + fast-but-noisy counters complement each other.

> **Earmarking:** ML interviews are full of rabbit holes. Name the issue, park it, move on; the interviewer will pull you back if it matters.

## 6. Modelling

**Baseline:** logistic regression on numeric + pre-computed embedding features. Fast, explainable, easy to update; misses feature interactions. Shows you don't over-engineer.

**Requirements for the real model:** handle text + images, mix in behavioural/user features, be cheap enough for 1B/day, and update when behaviour arrives (tolerating it being missing early on).

| Option | Notes |
|---|---|
| Bad: independent unimodal models + max of scores | Simple, reuses pre-trained models; can't see cross-modal meaning (benign image + caption = harmful), awkward to add tabular features, two models per post |
| Good: late fusion | Separate text/image encoders → concat with behavioural + user features → MLP. Easy to build; modalities only interact at the top |
| **Great: multi-modal transformer** (e.g. FLAVA-style) | Attention across all modalities, copes with missing modalities, strong few-shot. Costly → handle in inference |

**Architecture**
1. **Multi-modal encoder:** ViT for image patches, text encoder for post text, cross-attention between them, embedding layers for behavioural/user features.
2. **Lightweight update network:** a small net that takes the cached content embedding + fresh behavioural features, so re-scoring doesn't rerun the encoders.
3. **Heads:** shared layers → several task heads → calibration layer.

**Loss**
- Base: binary cross-entropy.
- **View weighting** aligns with the business objective, but raw views are power-law distributed and would let a few viral posts dominate. Use a capped log weight:

```
L_primary = BCE(y, ŷ) * min(log(1 + views), c)
L_reports = MSE(report_rate, predicted_report_rate)
L         = α * L_primary + β * L_reports      # keep α dominant
```

- **Feedback loop:** if production removes posts early, they never collect views, so view weights get biased. Impute predicted views, using a holdout to learn them.
- **Multi-task:** the report head uses the noisy-but-large report data, regularizes the representation and gives diagnostics. Only the primary head drives actions; more heads can be added later.
- **Categories:** if you want per-type outputs (nudity, violence, …) use **multi-label** sigmoid heads, not a softmax, because one post can violate several policies.

## 7. Inference

**Scaling to 1B posts/day**
- **Quantization-aware training** to shrink memory/compute with little accuracy loss.
- **Cache encoder outputs**: identical images and text recur (reposts, memes), so skip redundant forward passes.
- **Two-stage cascade:** a small **distilled student** (fewer features, trained to mimic the heavy teacher) screens everything and clears obvious benign posts; only the rest hit the heavy model. The stage-1 threshold is a dial for compute vs recall.

```
post ─► light model ──(score < t1)──► done (benign)
                     └─(score ≥ t1)─► heavy multi-modal model ─► calibration ─► action
```

**Triggering**
- On creation: light model, escalate to heavy if needed.
- Re-trigger on events: user reports, view-count milestones, negative comments. Cached encoders mean only the update network reruns.

**Training-data pitfalls from re-scoring**
- **Positive suppression:** if harmful posts get removed before they accumulate behaviour, the training set has few positives with behavioural signal, and the model learns "lots of negative reactions ⇒ benign". Holdouts help.
- **Calibration** must account for the same post being scored many times.

## 8. Evaluation

**Offline**
- **PR-AUC:** stable, overall quality.
- **Recall @ 95% precision:** matches the auto-removal threshold, but noisier (one point on the curve).
- **Impression-weighted** variants of both, to reflect the business objective.
- **Fairness:** slice metrics by user groups and look for gaps (a full bias discussion goes deeper).

**Online (A/B)**
- Run control and candidate side by side, with only one taking action per bucket. They flag different content, so new labels are needed.
- Random sampling at < 1% prevalence needs huge samples. Use **importance sampling** on model scores: label few very-high and very-low-score items, more of the uncertain middle, and **reweight** to stay unbiased (cheap variance reduction).
- Proxy metrics: user reports, appeals and appeal overturns.
- Primary metric: harmful impressions, with the precision guardrail.

## 9. Deep dive: user embeddings

(At Facebook, shared embeddings like "world2vec" exist as drop-in features, which hints at how useful this is.)

| Approach | How | Problems |
|---|---|---|
| Bad: learned ID embedding | Embedding table keyed by user ID, trained with the classifier | Cold start for new users; sparse users get noisy vectors; huge parameter count → memorizes past offenders instead of generalizing |
| Good: transductive graph embedding (e.g. GCN) | Train on the social graph (friends, followed pages, groups) for a fixed set of users | New users have none until retrain; fallback to average (of all users / friends) degrades over time, needs frequent retraining |
| **Good+: inductive graph embedding (GraphSAGE)** | Learn a function from a user's neighbourhood subgraph → embedding; works for unseen users | More complex, bigger model, real inference cost; cache aggressively. Embeddings get reused by other teams |

## 10. What interviewers look for

- **Mid-level:** sensible framing, the most informative features, model trade-offs, a credible end-to-end solution with some production awareness.
- **Senior:** stronger feature engineering (encoding, normalization, Bayesian smoothing), broader modelling toolkit, spots production issues unprompted (feedback loops, drift, positive suppression).
- **Staff:** moves fast through the basics, leads deep dives, knows multi-modal research trade-offs, and attacks the **label bottleneck** creatively (reports, comments, smarter label collection).

## 11. Common pitfalls

- Optimizing accuracy, or "content removed", without a precision guardrail
- Ignoring class imbalance (or forgetting to recalibrate after rebalancing)
- Weighting the loss by raw views (power law blows up training)
- Scoring only at creation and ignoring behavioural signal that arrives later
- Treating harm categories as a softmax instead of multi-label
- Running the heavy model on every post with no cascade or caching

Source: summarized from [Hello Interview: Harmful Content](https://www.hellointerview.com/learn/ml-system-design/problem-breakdowns/harmful-content) and its video walkthrough.
