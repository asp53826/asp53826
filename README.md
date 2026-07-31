<picture>
  <source media="(prefers-color-scheme: dark)" srcset="banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="banner-light.svg">
  <img alt="Aaryan Patel — systems engineer building measured infrastructure across storage, machine learning, sensing, and financial data" src="banner-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="#financial-data">FINANCIAL DATA</a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#storage--execution">STORAGE + EXECUTION</a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#ml-infrastructure">ML INFRASTRUCTURE</a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#signal--autonomy">SIGNAL + AUTONOMY</a>
</p>

## Systems, not scripts

I'm a computer science undergrad at UGA building the layer underneath the
model: storage engines, distributed runtimes, retrieval systems, signal
processors, and financial-data infrastructure.

Every repository follows the same contract:

> **Build the mechanism. Attack the assumptions. Measure against a real
> baseline. Publish where it loses.**

That means the output is not a screenshot or a notebook that ran once. It is a
reproducible benchmark, a correctness oracle, or a fault campaign that another
engineer can clone and challenge.

## Current signal

| system | what is implemented | measured proof |
|---|---|---:|
| **[edgar-mcp](https://github.com/asp53826/edgar-mcp)** | MCP server over SEC EDGAR with identity resolution, filing overflow history, bounded text windows, XBRL discovery, per-host caching, and a global request pacer | **32 tests**; warm 10-K read **138×** faster; peak request window held at the SEC's **10 req/s** ceiling |
| **[xbrl-normalize](https://github.com/asp53826/xbrl-normalize)** | 19 canonical financial line items with period-aware tag selection, restatement handling, derivations, provenance, and accounting-identity checks | **102-company** cross-industry benchmark; assets and liabilities at **100% coverage**; **96.1%** exact identity balance |
| **[lob-market-making](https://github.com/asp53826/lob-market-making)** | limit order book with price-time priority and post-only orders, informed-trader flow, three quoting strategies, exact PnL decomposition, and adverse-selection measurement | **36 tests**; paired 12-seed comparison; the naive strategy wins on PnL and loses on every risk-adjusted metric at **7×** the inventory deviation |
| **[aad-greeks](https://github.com/asp53826/aad-greeks)** | tape-based reverse-mode automatic differentiation over Monte Carlo paths, with pricers written once and differentiated rather than hand-derived | **19 tests**; Greeks match analytic formulas to **5.6e-16**; cost stays **1.7-2.4×** the price across a 50× change in input count |
| **[raft-mvcc](https://github.com/asp53826/raft-mvcc)** | Raft elections, conflict repair and majority commit combined with serializable MVCC, safe-point GC, and P-compositional linearizability checking | **598 assertions** across seeded partitions; **11-tick** five-node failover in the in-process simulator |
| **[columnar-engine](https://github.com/asp53826/columnar-engine)** | C++17 vector-at-a-time engine with null bitmaps, selection vectors, joins, aggregation, TPC-H Q1, and scalar differential oracles | **6,288 assertions**; Q1 at **53.1M rows/s**; batched filters **1.94×** scalar |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/proof-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/proof-light.svg">
  <img alt="Measured speedups plotted against the named baseline each was tested against, on a log axis" src="assets/proof-dark.svg" width="100%">
</picture>

<sub>Only results that reduce to a ratio over a <em>named</em> baseline appear
above. Throughput, utilisation and drift are not comparable quantities, so
putting them on one axis without a baseline would be decoration dressed as
evidence — the conformance rates, crash campaigns and coverage numbers stay in
the tables where the units survive.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/system-map-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/system-map-light.svg">
  <img alt="Animated topology connecting ingestion, storage, compute, serving, verification, financial data, machine learning, autonomy, and correctness" src="assets/system-map-dark.svg" width="100%">
</picture>

## Build channels

### Financial data

| project | evidence |
|---|---|
| **[edgar-mcp](https://github.com/asp53826/edgar-mcp)** | EDGAR filing/facts tools; cache validation; iXBRL cleanup; context-safe windows; rate-limit enforcement |
| **[xbrl-normalize](https://github.com/asp53826/xbrl-normalize)** | comparable statements across 102 filers; provenance on every value; missing is never silently zero |
| **[lob-market-making](https://github.com/asp53826/lob-market-making)** | post-only matching, informed flow, exact spread-capture/inventory split; two bugs that flattered the results are documented in `DESIGN.md` |
| **[aad-greeks](https://github.com/asp53826/aad-greeks)** ([live](https://asp53826.github.io/aad-greeks/)) | adjoint Greeks at constant cost in the input count; publishes the payoff where pathwise AAD returns a delta of exactly zero and is silently wrong |

### Storage + execution

| project | evidence |
|---|---|
| **[lob-market-making](https://github.com/asp53826/lob-market-making)** | limit order book with price-time priority and post-only orders, informed-trader flow, three quoting strategies, exact PnL decomposition, and adverse-selection measurement | **36 tests**; paired 12-seed comparison; the naive strategy wins on PnL and loses on every risk-adjusted metric at **7×** the inventory deviation |
| **[aad-greeks](https://github.com/asp53826/aad-greeks)** | tape-based reverse-mode automatic differentiation over Monte Carlo paths, with pricers written once and differentiated rather than hand-derived | **19 tests**; Greeks match analytic formulas to **5.6e-16**; cost stays **1.7-2.4×** the price across a 50× change in input count |
| **[raft-mvcc](https://github.com/asp53826/raft-mvcc)** | consensus + serializable snapshots + machine-checkable histories |
| **[columnar-engine](https://github.com/asp53826/columnar-engine)** | vectorized execution checked against scalar oracles |
| **[lsm-tree](https://github.com/asp53826/lsm-tree)** | WAL, memtables, SSTables, Bloom filters, range scans, crash-safe compaction; **4,064 assertions** |
| **[wal-recovery](https://github.com/asp53826/wal-recovery)** | CRC32 records, damaged-tail repair, atomic replay; 100 crash trials with **zero acknowledged writes lost** |

### ML infrastructure

| project | evidence |
|---|---|
| **[vllm-lite](https://github.com/asp53826/vllm-lite)** | paged KV cache, continuous batching, prefix caching, speculative decoding; **94% vs 21%** KV utilization |
| **[annlite](https://github.com/asp53826/annlite)** | HNSW + SIMD + Python bindings; FAISS parity at 0.99 recall and **1.83×** faster at 0.999 |
| **[dist-train](https://github.com/asp53826/dist-train)** | ring all-reduce from `send`/`recv`; **58.7 vs 234.9 MB/worker** at eight workers |
| **[rag-eval](https://github.com/asp53826/rag-eval)** | hybrid retrieval, reranking, hallucination metrics, and CI gates; SciFact **0.6643 vs 0.665** published BM25 |
| **[feature-store](https://github.com/asp53826/feature-store)** | point-in-time joins and streaming materialization; leakage measured at **+0.059 AUC** |
| **[grammar-decode](https://github.com/asp53826/grammar-decode)** | JSON Schema → character automaton → cached token mask; **100% vs 0%** conformance baseline |
| **[agent-harness](https://github.com/asp53826/agent-harness)** | five-layer sandbox and graded benchmark; 57 tests, including **25 escape attempts** |
| **[codebase-qa](https://github.com/asp53826/codebase-qa)** | auth, rate limits, durable jobs, cost tracking, and tracing—the prototype-to-service gap |

### Signal + autonomy

| project | evidence |
|---|---|
| **[sdr-receiver](https://github.com/asp53826/sdr-receiver)** | QPSK, RRC, acquisition, soft decisions, LDPC; **0 errors in 21,600 bits** at 4–8 dB after the waterfall |
| **[sar-focus](https://github.com/asp53826/sar-focus)** | pulse compression, backprojection, PGA autofocus; resolution within **0.5%** of theory |
| **[track-fusion](https://github.com/asp53826/track-fusion)** | IMM + JPDA + Wald scoring + OSPA; reports the manoeuvre regime where IMM wins and straight-line regime where it costs |
| **[vio-nav](https://github.com/asp53826/vio-nav)** | MSCKF, SO(3) preintegration, null-space feature marginalisation; **51.9×** lower drift than inertial dead reckoning |

## Portfolio telemetry

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/telemetry-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/telemetry-light.svg">
  <img alt="Measured portfolio telemetry generated from the public repository source" src="assets/telemetry-dark.svg" width="100%">
</picture>

<sub>Regenerated daily by <a href=".github/workflows/profile.yml">GitHub
Actions</a>. The panel reads the repositories and counts test functions from
source; no third-party stats card, hand-edited total, or page-load API call is
involved. Parametrized suites and looped invariants expand into many more checks
than the function count—for example, <code>raft-mvcc</code> alone executes 598
assertions.</sub>

## Working stack

```text
SYSTEMS    C++17 · Python · Raft · MVCC · WAL · LSM/SSTables · SIMD · POSIX
ML INFRA   PyTorch · distributed collectives · HNSW · BM25 · reranking · evals
FINANCE    SEC EDGAR · XBRL · accounting identities · provenance · MCP
MARKETS    limit order books · price-time priority · adverse selection · Avellaneda-Stoikov
QUANT      adjoint AD · pathwise Greeks · Black-Scholes · Monte Carlo · payoff smoothing
SIGNAL     QPSK · RRC · LDPC · SAR · Kalman/IMM · JPDA · OSPA
ESTIMATE   IMU preintegration · SO(3) · MSCKF · ATE/RPE · triangulation
SERVICES   FastAPI · SQLite/Postgres · durable queues · scrypt · tracing
INDUSTRY   Power BI · Node-RED · CtrlX Core · ERP automation
```

Day job: automation and analytics at **MP Equipment**—dashboards, ERP
automation, and AR/AI for industrial food processing.

## Open channel

**[aaryansp26@gmail.com](mailto:aaryansp26@gmail.com)**

Every system above is MIT licensed. Clone one, run the benchmark, and inspect
the regime where it breaks.

<sub>Hero, topology, and telemetry are generated in this repository. Both
themes are first-party SVGs and respect <code>prefers-reduced-motion</code>.</sub>
