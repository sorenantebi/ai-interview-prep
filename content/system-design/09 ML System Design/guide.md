# ML System Design in a Hurry

_Condensed notes from Hello Interview's free ML System Design in a Hurry guide — see Sources._

ML system design (MLSD) interviews are far less standardized than classic system design. Ask your recruiter which flavor you will get, then prepare for that one. Don't open the interview by hedging ("I've only done recsys"): it undersells you before you have shown anything.

| Interview type | Focus | Typical prompts | Covered here? |
|---|---|---|---|
| **Applied ML system design** (most common) | Turning a business problem into a production ML solution: data, features, model, evaluation, deployment, monitoring. Assume standard ML infra (serving, pipelines) exists | Recommendations for e-commerce, fraud detection, content moderation | **Yes, the main target** |
| **ML infra design** | Scalable, reliable ML platforms: serving, distributed training, feature stores, orchestration, cost, model versioning | Distributed training system, feature store, serving at millions of QPS | Partly (less modeling depth needed there) |
| **AI/ML research** | Theory: architectures, math, recent papers, new algorithms, losses and optimization | Research-scientist loops | No |
| **Research engineering** | Implementing and speeding up papers, frameworks and hardware, experiment design, benchmarking | Research-lab loops | No |

**What interviewers assess** (MLSD is common from mid-level and expected at senior):
- **Problem navigation**: turn a vague goal into a measurable ML problem. State assumptions, decide whether ML is warranted at all, and weigh formulations (classification vs ranking, regression vs forecasting). Senior candidates get vaguer prompts and should find the framing themselves.
- **Data, features, labels**: where labels come from, avoiding leakage and feedback loops, how features are represented (embeddings, one-hot, …), and using more of the available data.
- **Model design** (the core): an effective *and* efficient model, trade-offs between options, how multi-stage pieces fit together. Show you can carry experience over to a domain you haven't worked in.
- **Integration and evaluation**: deployment, monitoring, iteration, getting from a notebook to production. Evaluation strategy is problem-specific; show you know the usual traps.
- **Communication**: always graded implicitly. Be a clear, collaborative colleague.

## Delivery framework

Roughly a 45-minute budget. These are guideposts, not rules: if the interviewer steers somewhere else, follow them. The point is to reach the parts that carry the score (data, model, evaluation) with time to spare.

| # | Step | Time | Output on the board |
|---|---|---|---|
| 1 | Problem framing | 5–7 min | Clarified scope, business objective, ML objective + metric |
| 2 | High-level design | 2–3 min | Block diagram: inputs → components → actions |
| 3 | Data & features | ~10 min | Data sources/labels, signal sources, encodings |
| 4 | Modeling | ~10 min | Baseline → candidate families → chosen architecture + loss |
| 5 | Inference & evaluation | ~7 min | Offline/online metrics, serving constraints and optimizations |
| 6 | Deep dives | remainder | Edge cases, scaling, monitoring/retraining |

### 1. Problem framing (5–7 min)

- [ ] **Clarify before designing.** The most common failure is jumping straight in. Ask about:
  - Users, their pain points, and the current solution (if one exists)
  - Scale: users, QPS, catalog/corpus size
  - Real-time vs batch inference, latency budget, privacy/legal constraints
  - Where the output surfaces (e.g. which page shows the recs)
- [ ] **Find the hard part.** This section isn't heavily graded, but strong (staff-level) candidates quickly name what makes the problem tricky, i.e. what a team would spend years on.
- [ ] **State a business objective.** The model's loss is rarely the true goal. "Detect harmful content" might really mean *reduce harmful impressions* or *reduce legal exposure*, and those lead to different systems.
  - Be specific ("increase purchases from recommendations", not "improve UX"). Direction matters; made-up percentages don't.
  - **Call out where the naive ML objective diverges.** For example, a harmful post with millions of views matters far more than one nobody saw, so weight by exposure.
- [ ] **Translate to an ML objective.** Task type (classification / regression / ranking / clustering), what you predict (e.g. P(purchase | user, item, context)), and a primary metric (precision@k, NDCG, PR-AUC, …).
  - Don't agonize over k or exact operating points. That gives little signal.
  - This objective anchors every later decision, so make it crisp.

**Green flags:** probing questions that reach the core challenge · a concrete business objective · an ML objective that guides the rest.
**Red flags:** settling for a naive ML objective · generic questions · an ML objective too vague to build on.

### 2. High-level design (2–3 min)

- [ ] Sketch a simple block diagram (or describe it verbally): inputs → feature extraction → model(s) → **actions taken** (block, rank, send to review, …).
- [ ] Walk the **full lifecycle**, from data in to action out to feedback logged. Twists often only show up end to end (e.g. labels coming from human review, or actions changing future data).
- [ ] Assume fast feature serving and inference exist. **Skip DB/API choices** in applied interviews, since platform teams own those. Don't polish the diagram; it is only a communication tool.

### 3. Data & features (~10 min)

**Training data**
- [ ] List the data sources: what exists, what must be collected. If unsure whether something exists, ask.
- [ ] **Labels:** explicit (human review, reports) vs implicit/proxy (clicks, watches, purchases). Discuss labeling cost, noise, and volume.
- [ ] Think in three buckets: **supervised, semi-supervised, unsupervised**. Great answers use the much larger unlabeled pools (pretraining, pseudo-labels, self-supervision).
- [ ] Flag bias and quality issues, cold start, and the risk of baking existing biases into training data. Don't assume clean data; prep usually takes most of a real project.

**Features** (see Core concepts → Feature engineering for the structure)
- [ ] Organize by **signal source**, not as a flat list. Give 2–3 representative signals per source, each with a reason it should predict the label.
- [ ] Say how each one is **represented**: embeddings vs one-hot for categoricals, encoders for text/images, normalization and missing-value handling for numerics.
- [ ] Note **freshness/serving tier** (static, batch, streaming, request-time) and use a feature store for online/offline parity.
- [ ] Prioritize by expected predictive power vs build and serving cost. Not every good idea is worth its pipeline.

**Green flags:** using non-supervised data creatively · features with clear hypotheses · representation is addressed.
**Red flags:** a long list of features with no rationale · unclear how features reach the model.

### 4. Modeling (~10 min)

- [ ] **Baseline first.** A heuristic or simple model (popularity, collaborative filtering, logistic regression). It gives a yardstick and turns the discussion into "is each added piece of complexity worth it?"
  - Baselines also **fill gaps** in multi-stage systems: a quick candidate generator lets you spend your time on the ranker.
- [ ] **Survey model families with trade-offs**: cost, latency, complexity, interpretability, accuracy, data needs. Usually compare a classical option (GBDT/LR) with a deep one. Deep isn't always the right call, but always consider it.
  - Aim for **proven techniques from the last few years** (what big-company ML blogs describe). One brand-new paper sounds risky; nothing from the last 5–7 years sounds dated.
  - Don't forget non-parametric options like ANN retrieval, alone or alongside a learned model.
- [ ] **Commit to one** and go deeper. There isn't time for all of them.
- [ ] **Architecture at the right altitude**: main components, inputs, layer types, activations, output head, **loss function**, regularization (dropout/L2). Avoid both "use deep learning" (too vague) and "4×1024 layers" (that is an empirical choice). Example: a two-tower model (user/item embeddings) → MLP with ReLU → sigmoid for P(purchase).
- [ ] Expect probing follow-ups; this is where interviewers test whether you have actually built such a model. It's fine to say "I've mostly done classification, but here's how I'd reason about ranking", then *generalize* convincingly.

**Green flags:** a cheap baseline vs a justified complex model · several options compared · enough architecture detail to defend.
**Red flags:** jumping to a big, expensive model · vague architecture that suggests no hands-on experience.

### 5. Inference & evaluation (~7 min)

- [ ] **Offline metrics** on held-out data (precision/recall, PR-AUC, NDCG, MAP, recall@k) with a split that matches production, usually **time-based**.
- [ ] **Online:** shadow mode → A/B test (or interleaving for rankers) measuring **business metrics** (CTR, conversion, retention, reviewer load). Include operational metrics: latency, cost.
- [ ] **Tie every metric back to the business objective.** Better ML metrics with flat business metrics means no win.
- [ ] **Inference constraints:** QPS, latency, cost. Mention optimizations only when justified: distillation, quantization, pruning, caching, precomputing embeddings, multi-stage funnels (cheap retrieval → heavy ranker).
- [ ] If inference is offline and small, say so and move on. If it is high-QPS and latency-critical, expect to be pushed here. This is where people who only know notebooks stand out, in a bad way.

**Green flags:** offline + online metrics linked to the objective · real serving constraints · justified optimizations.
**Red flags:** metrics disconnected from business · ignoring latency/cost · optimizations with no stated need.

### 6. Deep dives (remaining time)

Follow the interviewer if they steer. Otherwise pick where you're strongest and where the problem is hardest.
- **Edge cases:** cold start (content-based features, exploration like ε-greedy), sparsity, seasonality, debiasing models trained on unrepresentative data.
- **Scaling:** distributed training, serving architecture, caching, ANN indexes.
- **Monitoring & maintenance:** what to track (business KPIs, prediction/feature distributions, diversity, drift), alerts, retraining cadence and triggers.

> The goal isn't a perfect system in 45 minutes. It's showing a clear thought process and sensible trade-offs under constraints.

## Core concepts

### Feature engineering

**The shift:** large models (transformers, DLRM-style rankers, multimodal encoders) now take raw text, images and event sequences directly and learn the interactions themselves. Hand-built numeric features remain mostly in light rankers, tree models, and fraud/trust-and-safety. But **choosing which signals the model sees, keeping them fresh, and computing them the same way at train and serve time** is still your job. Most production cases of "the model isn't learning X" come from a missing, stale, or skewed source.

**Structure by signal source.** This prevents the endless feature list: it gives a skeleton you can expand or stop at any point.

| Source | What it is | Examples | Notes |
|---|---|---|---|
| **Content / item** | The thing being scored | Post text + image, video title/thumbnail/transcript, transaction details | Encode raw content with a model. Dominant for "what is this?" problems (moderation); weaker for engagement |
| **Actor / user / creator** | Who is involved | Viewer, author, account holder | Long-term embedding (fine to assume a shared company one exists) **plus** a few explicit attributes: account age, country, verification, recent flags |
| **Behavioral** | What happened recently | Last N watches, view velocity, posting cadence, negative-reaction rate | Heavy rankers take raw `(item, action, time)` sequences; light rankers and trees use aggregates. Most prone to drift, leakage and skew |
| **Network / graph** | Relationships | Follows, co-watches, shared IPs/devices, money flows | Usually a GNN embedding fed in as a feature. Key in fraud, bots, PYMK; minor for product classification |
| **Context / request** | The request itself | Time, device, current page, recent queries | Cheap, real-time, surprisingly predictive, and often forgotten. Mentioning it is easy credit |

- **Freshness ladder:** static (at creation) → daily batch → streaming → request-time. Each rung down costs more infrastructure. When you propose a fast signal, ask aloud whether it **justifies a streaming pipeline**.

**Encoding by input shape**

| Input | Modern encoding |
|---|---|
| Raw text / images | Tokenize → transformer; patches → ViT. Train jointly, or pretrained + fine-tuned/frozen when data is limited. No hand-made n-grams or histograms |
| Text + image | Contrastive alignment into a shared space (CLIP-style) |
| Sparse categoricals (IDs, enums) | Learned embedding table looked up by ID |
| Very high-cardinality IDs | **Hashing trick**: hash into a fixed number of buckets (e.g. 10M rather than 1B), then embed. Heavy users dominate their bucket; long-tail users share rows and end up near an "average" vector |
| Event sequences | **Light ranker:** mean / recency-weighted pooling of embeddings (cheap, loses order). **Heavy ranker:** sequence as tokens through self-attention |
| Power-law numerics | Log-transform, or bucketize (10–100 bins) and embed (good for non-monotonic effects). Standardize for linear models, using **training-set** stats at serve time too |
| Graph | Train a GNN, import the node embedding |

- **Rates with small denominators** → Bayesian/additive smoothing: `(events + α·C) / (trials + C)`, with α a prior rate and C a pseudo-count. For example, with prior 3% and C=100, an item with 3 reports on 6 views scores ≈5.7% rather than 50%; high-volume items keep roughly their observed rate.
- **Recency:** exponential decay `exp(-Δt/τ)` (short τ for clicks, long τ for taste) and/or **several windows** (1h / 1d / 7d) to tell a spike from a baseline. Avoid hard cutoffs.

**Pitfalls interviewers probe**
- **Leakage:** a feature unavailable at prediction time (post-hoc moderator label, lifetime clicks on the same impression, aggregates computed over train+test). Offline metrics look great, then the launch fails. Ask of every feature: *known at request time, before the prediction?*
- **Cold start:** imputing the mean hides that the value is unknown. Prefer a **missing indicator** (with missing examples in training, possibly synthesized) or a separate cold-start feature set or model that graduates entities later. In recsys, also make sure new items/creators get enough exposure to gather signal.
- **Feedback loops:** the model's own decisions shape its future features and labels, so it ends up measuring "what we surfaced". Don't drop the feature. Add **randomized exploration** or log propensities and use **inverse propensity weighting**. Name the loop out loud.
- **Adversarial robustness:** content features are easy to evade; temporal and graph patterns are hard to fake. Judge feature groups by **robustness over time**, not just today's accuracy.
- **Drift:** distributions move without any attacker (seasons, new categories, logging changes). Monitor feature distributions and automatically drop or ignore corrupted features. Retraining helps but doesn't fix everything.

**10-minute feature plan:** ~3 min sources + examples → ~2 min encodings → ~2 min the one or two normalization tricks that matter → ~2 min the most relevant pitfall → ~1 min buffer. **Earmark depth** instead of spending time on it: "There's more to say on behavioral signals; happy to come back to it."

### Embeddings

- **What:** a dense learned vector (e.g. 64–512 floats) for a user, item, query or image, where **nearby means similar**. It replaces one-hot encoding, which has no shared structure (each ID is learned alone), is huge, and can't handle new entities without retraining.
- **"Similar" means whatever the training objective says.** Co-watch training puts videos together because the same people watch them (not because they look alike); co-purchase puts toothbrush near toothpaste. Training starts from random vectors and repeatedly pulls positives together and pushes negatives apart until clusters form.

| Method | How | When / trade-off |
|---|---|---|
| **Matrix factorization** | Factor the sparse user×item matrix R ≈ U·Vᵀ (rank k), minimizing error on observed cells via ALS/SGD with regularization. The low rank forces shared patterns | Cheap, well understood, a **solid retrieval baseline** (MF + ANN). Usually beaten by neural methods |
| **Two-tower / contrastive** | Separate query (user) and candidate (item) encoders, possibly different architectures, mapping into **one shared space**; score = dot product. Train on positive pairs from logs with in-batch negatives; loss **InfoNCE** (softmax over batch) or triplet (margin) | The production default for retrieval (recsys, semantic search, RAG). Candidate embeddings are precomputed into an ANN index, so only the query tower runs online. Siamese (shared encoder) when both sides are the same type |
| **Graph embeddings** | *Transductive* (node2vec/DeepWalk: random walks + word2vec) learns one vector per known node. *Inductive* (GraphSAGE/GNNs) learns a function of node features + neighborhood | Say: "inductive, so new nodes get embeddings without retraining". Transductive needs retraining or a content fallback for new nodes |
| **Pretrained + fine-tune** | Start from BERT / CLIP / sentence-transformers and fine-tune contrastively on in-domain pairs | The modern default; don't train from scratch. Hosted embedding APIs suit prototypes; at scale, self-host for cost and fine-tuning |

- **Negative sampling is the hard part.** Random negatives are easy but weak. **Hard negatives** (scored high but irrelevant) drive quality. Mine them periodically with a frozen model snapshot, since the index changes as the model trains, and rely on in-batch negatives between refreshes.
- **Three uses:** (1) **features** for downstream models (embeddings are often shared across teams, so assuming one exists is fine); (2) **clustering** (segmentation, topics, near-duplicate detection; k-means is usually enough); (3) **retrieval** (offline index + online query + ANN), which covers recsys candidate generation, semantic search (often **hybrid** with keyword/BM25), and RAG (retrieval quality depends on the embeddings).
- **Dimensionality:** 64–128 for very high-QPS retrieval · 256–512 as the default · 1024+ when quality outweighs cost. **Matryoshka** embeddings: prefixes are valid embeddings, so a short prefix can do coarse retrieval and the full vector can re-rank.
- **Evaluation:** prefer **extrinsic** measures (recall@k on held-out pairs, downstream accuracy, A/B) plus quick intrinsic sanity checks (nearest-neighbor spot checks, similarity spread; MTEB for text). Don't propose abstract research on embedding quality.
- **Serving:** batch-embed candidates into an ANN index (HNSW/IVF/quantization) · **refresh** on a schedule plus event-driven hot updates when items change or the model is retrained (candidates often skip this; seniors ask about it) · for minute-level freshness, update embedding tables **online** in a parameter server while the dense layers stay mostly frozen (Monolith-style) · **cold start:** begin with a content-based embedding and blend in the behavioral one as interactions accumulate.
- **Canonical sentence:** "User and item each get a 64-d embedding from a user tower (profile + recent history) and an item tower (content features), trained with in-batch-negative InfoNCE so the dot product predicts engagement. Items are precomputed into an ANN index."

### Evaluation

**Framework (work top-down):** Business objective → Product metrics → ML metrics → Methodology (offline as a fast proxy, online as truth) → Challenges and mitigations. Showing each layer shows you can *optimize* a real system, not just score a model.

| System | Business / product signals | ML metrics | Methodology | Signature challenges |
|---|---|---|---|---|
| **Classification** (moderation, spam, fraud) | What action follows and what it costs: retention, reviewer cost, time to label, appeal rate, cost of FP vs FN | Precision at an operating threshold (often around human level), recall at that precision, **PR-AUC**, ROC-AUC, F1, FPR per segment, per-class metrics | Offline: stratified test set, choose threshold from the PR curve. Online: **shadow mode** (predict, take no action) → A/B. Check offline↔online correlation | **Imbalance** (use PR-AUC; ROC-AUC can look fine on a useless model) · expensive labels (stratify by score, active learning) · **prevalence estimation** (random samples are unbiased but noisy at <1% positives) · feedback loops (withhold actions sometimes, keep a golden set) |
| **Recommender** | Value of a good rec vs cost of a bad one; session conversion, ARPU/GMV, N-day retention, catalog coverage, dwell time (watch for doom-scrolling) | MRR, **NDCG**, Hit/Recall@K, coverage, calibration | Offline: **time-respecting** splits (beware temporal leakage), replay the retrieval + ranking pipeline. Online: shadow-rank → A/B with a short-term (CTR) **and** long-term (retention) metric, run long enough. **Interleaving**: paired comparison in one mixed list, needs roughly an order of magnitude less traffic | Short-term wins hurting long-term (a favorite probe) · long horizons (proxies + holdout cohorts, counterfactual estimates with high variance) · feedback loops (ε-greedy/Thompson exploration, uniform golden set). **Log all candidates + features** so experiments can be replayed |
| **Search / IR** | Satisfied users return; conversion; time to answer. Clicks alone are a weak proxy (check bounces) | P@k / R@k, MRR, **NDCG@k** (k = results visible in the UI), MAP, success@k; plus p99 latency | Offline: graded (query, doc, relevance) set spanning head/torso/tail, fresh vs evergreen, locales. Online: shadow → A/B or interleaving | **Position/presentation bias** in click labels (IPW, interleaving) · ambiguous queries (intent classification, diversify results) · long-tail queries with few judgments (active learning, query clustering, LLM judges) · freshness (decay, freshness classifiers) |
| **Generative** | Value unlocked vs harm prevented: task success, handle time, CSAT/NPS, brand-safety incidents, latency | A **portfolio**: BLEU/ROUGE (cheap, brittle), BERTScore, hallucination rate, toxicity, diversity (distinct-n), human pairwise/Likert, custom (% refusals) | Offline: stratified prompt set (intents, languages, edge cases, policy limits), multiple references or pairwise ranking. Online: hidden shadow → A/B + safety dashboards; a **golden canary** prompt set for drift | Subjective quality (rubrics per aspect, preference models) · hallucination (attribution, fact checks, RAG grounding, calibration; target rare prompts) · safety (**prioritize false negatives**, red-teaming) · human-eval cost (cheap automated filters + sampled human review, track their correlation) · drift (**time-based** holdouts) |

**Metric cheat sheet**
- **Precision** = TP/(TP+FP), "when it flags, is it right?" · **Recall** = TP/(TP+FN), "how much do we catch?" · **F1** = harmonic mean of the two.
- **ROC-AUC** = separability across thresholds, misleading under heavy imbalance · **PR-AUC** = the precision/recall trade-off across thresholds, the right choice for rare positives.
- **NDCG** = graded relevance discounted by log(rank), normalized by the ideal order · **MAP** = mean of precision at each relevant hit · **MRR** = mean of 1/rank of the first relevant hit.
- **Perplexity** = how surprised the LM is by the true text (lower is better) · **FID** = distance between generated and real image distributions (lower is better) · **CLIP score** = image-prompt alignment.

### Generalization

- **Goal:** good performance on *unseen, future* data. Over- and underfitting aren't a binary; a model can overfit some slices and underfit others, and leakage or drift are harder to diagnose than a loss curve. Don't just say "avoid overfitting": say what you'd **measure**.

| | Overfitting | Underfitting |
|---|---|---|
| Symptom | Training loss keeps falling while validation loss plateaus or rises; prod ≪ offline | Training and validation loss both high, plateau early |
| Cause | High variance: memorizes noise; too much capacity for the data | High bias: model too simple or wrong model family |
| Fixes | Smaller model, more data, transfer learning, augmentation, regularization, early stopping | More capacity, better features, different model |

- **Validation split is a design choice.** Random splits can leak shared signal (e.g. market-wide moves when holding out individual stocks). For anything temporal, **split by time**.
- **Capacity vs data:** high-capacity models need lots of data. Proposing a big model trained from scratch on a small dataset is a strong red flag. Say instead: "Limited data, so start with logistic regression: fast, hard to overfit, a good baseline."
- **Small-data tools:**
  - **Transfer learning:** reuse a pretrained backbone (BERT, ResNet), freeze the lower/general layers, train a new head or LoRA adapter.
  - **Augmentation:** targeted transforms (crops, noise, paraphrases) for known invariances, not a general fix for scarce data. If proposing LLM-generated data, be ready to answer "why not use the LLM to label directly?"
  - **Self-supervised** pretraining on unlabeled data (masking, reconstruction) → fine-tune; **semi-supervised** training on a few labels plus many unlabeled examples (pseudo-labels, consistency regularization).
- **Data drift** (the world changes after deploy, unlike overfitting):
  - *Covariate shift*: P(x) changes, P(y|x) stays (summer vs winter browsing).
  - *Prior/label shift*: P(y) changes (fraud rate 1% → 3%), so thresholds become miscalibrated.
  - *Concept drift*: P(y|x) changes (new competitor, regulation, changed tastes). The hardest case.
  - **Detect:** prediction-distribution shifts · feature stats (mean/percentiles, category frequencies) with alerts · live performance on fresh labels (label delay is the catch) · scores on a fixed holdout across retrains.
  - **Handle:** **scheduled retraining first** (e.g. weekly; easy to propose) → **online learning** for fast-moving domains like fraud (risk: catastrophic forgetting) → **online embedding updates** with a frozen network (short-video recsys) → ensembles over time periods (costly) → **human-in-the-loop** review of uncertain cases, which also yields fresh labels.
- **Regularization** (trade a little training fit for robustness; it also helps under drift):
  - **L2 / weight decay:** the default, mention first; tune λ on validation.
  - **L1:** drives weights to zero, giving sparsity and feature selection; useful for linear models and pruning under performance constraints.
  - **Dropout:** randomly zero units with probability p (inverted dropout scales by 1/(1-p) during training, so inference needs no change). Standard for deep nets.
  - **LayerNorm:** per-example normalization that stabilizes training (mild regularizer); it has replaced BatchNorm in transformers (BatchNorm struggles with small batches and sequences).
  - **Early stopping:** stop when validation loss hasn't improved for N epochs and keep the best checkpoint. Essentially free; always use it.

## Common pitfalls / quick checklist

**Pitfalls**
- Designing before clarifying scope, scale, latency and the current system.
- An ML objective that ignores the business objective (e.g. unweighted accuracy when exposure is what matters).
- Spending 10+ minutes listing features with no structure and no rationale.
- Leaky features or random splits on temporal data, so offline metrics look great and production disappoints.
- Jumping to a huge model with no baseline, or training it from scratch on little data.
- Hand-waving architecture ("a deep model") or over-specifying it (exact layer widths).
- ROC-AUC on heavily imbalanced data; offline metrics never checked against online results.
- Ignoring latency, cost and serving, or proposing optimizations nobody needs.
- Forgetting feedback loops, cold start, drift and retraining.
- Spending time on DB/API details in an applied interview.
- Opening with disclaimers about your experience.

**Quick checklist**
- [ ] Clarified users, scale, latency, real-time vs batch, existing system
- [ ] Business objective stated, with how it differs from the naive ML objective
- [ ] ML task + prediction target + primary offline metric
- [ ] End-to-end block diagram including the action taken and the feedback logged
- [ ] Data sources + label strategy (explicit vs proxy, cost, noise) + unlabeled data use
- [ ] Features by source (content, actor, behavioral, graph, context) with encodings and freshness tier
- [ ] Leakage, cold start, feedback-loop risks named and mitigated
- [ ] Baseline → 2–3 model options with trade-offs → one chosen, with architecture + loss + regularization
- [ ] Offline metrics + time-based split; online shadow → A/B (or interleaving); short- and long-term metrics
- [ ] Serving: latency/QPS/cost, multi-stage funnel, ANN, caching, distillation/quantization if needed
- [ ] Monitoring: feature/prediction drift, KPI dashboards, retraining cadence, exploration traffic
- [ ] Earmarked deeper topics so the interviewer can choose

## Sources

- [ML System Design in a Hurry: Introduction](https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/introduction)
- [Delivery Framework](https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/delivery)
- [Core Concepts: Feature Engineering](https://www.hellointerview.com/learn/ml-system-design/core-concepts/feature-engineering)
- [Core Concepts: Embeddings](https://www.hellointerview.com/learn/ml-system-design/core-concepts/embeddings)
- [Core Concepts: Evaluation](https://www.hellointerview.com/learn/ml-system-design/core-concepts/evaluation)
- [Core Concepts: Generalization](https://www.hellointerview.com/learn/ml-system-design/core-concepts/generalization)
- Videos: [Harmful Content Detection](https://www.youtube.com/watch?v=9KUC_nHydZg), [Bot Detection](https://www.youtube.com/watch?v=wI4L11EoW3I), [Recommendation System Infra Basics](https://www.youtube.com/watch?v=GncgOIiMII8), [Vector Databases](https://www.youtube.com/watch?v=Fq73E8DQprc)
