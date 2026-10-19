<a href="https://asp53826.github.io/labs/faultline/">
<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/fault-chamber/fault-chamber-mobile-dark-still.png">
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/fault-chamber/fault-chamber-mobile-light-still.png">
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/fault-chamber/fault-chamber-mobile-dark.png">
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/fault-chamber/fault-chamber-mobile-light.png">
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/fault-chamber/fault-chamber-dark-still.png">
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: light)" srcset="assets/fault-chamber/fault-chamber-light-still.png">
  <source media="(prefers-color-scheme: dark)" srcset="assets/fault-chamber/fault-chamber-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/fault-chamber/fault-chamber-light.png">
  <img alt="FAULT CHAMBER: a five-node Raft cluster is partitioned, elects a leader, repairs conflicting history, and emits a verification receipt" src="assets/fault-chamber/fault-chamber-dark-still.png" width="100%">
</picture>
</a>

<p align="center">
  <a href="https://asp53826.github.io/lab/"><strong>▶ ENTER THE LAB</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/labs/faultline/"><strong>BREAK A RAFT CLUSTER</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://github.com/asp53826/raft-mvcc"><strong>INSPECT THE SOURCE</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/resume/Aaryan-Patel-Systems-Resume.pdf"><strong>RÉSUMÉ</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="mailto:aaryansp26@gmail.com"><strong>EMAIL</strong></a>
</p>

> I build systems that can show where—and why—they fail.

## The 30-second version

- **What I build:** systems in C++ and Python, including consensus, storage engines, query planners, LLM inference and GPU compilers. Each one ships with a test suite, a named baseline, and the regime where it breaks.
- **Strongest evidence:** [raft-mvcc](https://github.com/asp53826/raft-mvcc) passes **598 assertions** under seeded faults · [vllm-lite](https://github.com/asp53826/vllm-lite) reaches **2.9× throughput** at 94% KV-cache use · [track-fusion](https://github.com/asp53826/track-fusion) cuts localization error **47%** in its published regime.
- **Now:** UGA computer science, graduating December 2026 · industrial data engineering at **MP Equipment** · open to full-time **systems and ML infrastructure** roles.

<a href="https://asp53826.github.io/labs/faultline/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/terminal-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/terminal-light.svg"><img alt="Animated terminal: whoami, then make test in raft-mvcc passes 598 assertions, a FAULTLINE leader isolation produces two leaders that heal into one, and current status. A second pane shows a live lab monitor." src="assets/fun/terminal-dark.svg" width="100%"></picture></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/now-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/now-light.svg"><img alt="Now shipping: the latest human commit across the public portfolio" src="assets/now-dark.svg" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-a-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-a-light.svg"><img alt="" src="assets/fun/divider-a-dark.svg" width="100%"></picture>

## Enter the working lab

<a href="https://asp53826.github.io/lab/"><img alt="The live site asp53826.github.io/lab, filmed in a real browser by CI: an aurora field steered by the cursor behind the line 'I build systems, then I try to break them.'" src="assets/live/lab.webp" width="100%"></a>

<sub>↑ Not a mockup. A GitHub Action opens <a href="https://asp53826.github.io/lab/">the live site</a> in a real browser, steers it, and re-films this window whenever the site changes.</sub>

## Inside the mechanism

<table>
<tr>
<td width="50%"><a href="https://asp53826.github.io/labs/faultline/"><img alt="FAULTLINE: isolating a Raft leader produces two leaders in different terms; the invariant monitor flags the commit-index split, then healing repairs it" src="assets/demos/faultline.gif" width="100%"></a></td>
<td width="50%"><a href="https://asp53826.github.io/labs/signalroom/"><img alt="SIGNALROOM: measured replay of an IMM tracker on a maneuvering target and crossing tracks, with truth, measurements and estimates" src="assets/demos/signalroom.gif" width="100%"></a></td>
</tr>
<tr>
<td><strong>FAULTLINE</strong>: the real C++17 Raft + MVCC engine in WebAssembly. Isolate the leader, watch two leaders appear in different terms, then heal and verify repair.</td>
<td><strong>SIGNALROOM</strong>: measured replays of the published tracking results, with truth, measurements and estimates kept separate, including the regime where the estimator loses.</td>
</tr>
</table>

## The arcade

<a href="https://asp53826.github.io/lab/play/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/highscores-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/highscores-light.svg"><img alt="Arcade high-score screen built from measured results: 598 assertions, 138x warm read, 2.9x throughput, 47% less error, 68 tests. A pixel ship turns split-brain, stale-read and lost-write bugs into regression tests." src="assets/fun/highscores-dark.svg" width="100%"></picture></a>

<table>
<tr>
<td width="50%"><a href="https://asp53826.github.io/lab/play/"><img alt="Short Gamma gameplay: hedging a short-volatility options book as delta swings, Greeks from the aad-greeks reverse-mode engine" src="assets/live/short-gamma.gif" width="100%"></a></td>
<td width="50%"><a href="https://asp53826.github.io/lab/royale/"><img alt="Order Book Royale gameplay: eight traders on one live order book on the lob-market-making matching engine" src="assets/live/royale.gif" width="100%"></a></td>
</tr>
<tr>
<td><strong><a href="https://asp53826.github.io/lab/play/">SHORT GAMMA ▶</a></strong>: you inherit a short-volatility book with ten days to the close. Every Greek on screen comes off the <a href="https://github.com/asp53826/aad-greeks">aad-greeks</a> reverse-mode tape, and one number is wrong on purpose.</td>
<td><strong><a href="https://asp53826.github.io/lab/royale/">ORDER BOOK ROYALE ▶</a></strong>: eight seats, one live order book, four minutes, last trader standing. It runs on the <a href="https://github.com/asp53826/lob-market-making">lob-market-making</a> matching engine.</td>
</tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/fault-chamber/evidence-stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/fault-chamber/evidence-stack-light.svg">
  <img alt="Evidence stack: claim, attack, oracle, boundary, and source-bound receipt" src="assets/fault-chamber/evidence-stack-dark.svg" width="100%">
</picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-b-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-b-light.svg"><img alt="" src="assets/fun/divider-b-dark.svg" width="100%"></picture>

## Execute the evidence

<a href="https://asp53826.github.io/witness/">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/witness-chamber-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/witness-chamber-light.svg">
  <img alt="Open WITNESS, a live reproducibility chamber for eight receipt-bound engineering counterexamples" src="assets/witness-chamber-dark.svg" width="100%">
</picture>
</a>

**[WITNESS](https://asp53826.github.io/witness/)** verifies eight canonical
receipts, runs each pinned C++/WebAssembly, TypeScript, or Python implementation
inside the browser, compares the observed trace with its oracle, and emits a
local run receipt. The local receipt is explicitly unattested; release
provenance remains bound to COUNTEREXAMPLE.

**[Read the 23-page technical monograph](https://asp53826.github.io/witness/publications/WITNESS-Technical-Monograph.pdf)** ·
**[Inspect the GitHub edition](https://github.com/asp53826/witness/blob/main/docs/WITNESS-Technical-Monograph.md)** ·
**[Download the Word edition](https://github.com/asp53826/witness/raw/main/docs/WITNESS-Technical-Monograph.docx)**

The publication formalizes WITNESS as an executable-evidence system through a
threat model, eight capsule studies, eleven original diagrams, artifact-review
readiness, explicit limitations, and a pinned identity register. It is
independent technical documentation, not an awarded degree or peer-reviewed
thesis.

## Vidur: speculative decoding

**[Explore the results](https://asp53826.github.io/vidur/)** ·
**[Inspect the source](https://github.com/asp53826/vidur)** ·
**[Read the modeling notes](https://github.com/asp53826/vidur/blob/spec-decode/docs/speculative_decoding.md)**

An independent extension of Microsoft Vidur for proposal generation, target-model
verification, accepted-token progress, and lookahead KV memory. The interactive
page explores a **39-row simulator sweep** where the verify-attention assumption
can reverse whether speculation appears beneficial. These are predictions;
real GPU validation is pending. The repository includes a matched-workload vLLM
validation harness and **68 passing unit and fake-server tests**; one additional
end-to-end test requires a trained predictor cache.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-c-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-c-light.svg"><img alt="" src="assets/fun/divider-c-dark.svg" width="100%"></picture>

## Choose your route

<table>
<tr>
<td width="25%"><a href="https://asp53826.github.io/systems/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/routes/systems-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/routes/systems-light.svg"><img alt="Open Systems route" src="assets/routes/systems-dark.svg" width="100%"></picture></a></td>
<td width="25%"><a href="https://asp53826.github.io/ml-infrastructure/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/routes/ml-infrastructure-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/routes/ml-infrastructure-light.svg"><img alt="Open ML Infrastructure route" src="assets/routes/ml-infrastructure-dark.svg" width="100%"></picture></a></td>
<td width="25%"><a href="https://asp53826.github.io/defense/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/routes/defense-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/routes/defense-light.svg"><img alt="Open Autonomy route" src="assets/routes/defense-dark.svg" width="100%"></picture></a></td>
<td width="25%"><a href="https://asp53826.github.io/quant/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/routes/quant-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/routes/quant-light.svg"><img alt="Open Quant route" src="assets/routes/quant-dark.svg" width="100%"></picture></a></td>
</tr>
</table>

Each route is a short, role-specific path through live systems, source, tests,
measured evidence, and the regime where the result stops holding.

**[PROOFGRAPH](https://asp53826.github.io/proofgraph/)** is the interactive
router across those routes: choose a hiring lens, then traverse one claim
through its attack, oracle, measurement, boundary, exact source revision, and
signed receipt.

## Eight proof cartridges

<table>
<tr>
<td width="50%"><a href="https://asp53826.github.io/counterexample/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/counterexample-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/counterexample-light.svg"><img alt="COUNTEREXAMPLE public failure register" src="assets/projects/counterexample-dark.svg" width="100%"></picture></a></td>
<td width="50%"><a href="https://asp53826.github.io/labs/faultline/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/raft-mvcc-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/raft-mvcc-light.svg"><img alt="Raft and MVCC consensus under attack" src="assets/projects/raft-mvcc-dark.svg" width="100%"></picture></a></td>
</tr>
<tr>
<td width="50%"><a href="https://asp53826.github.io/labs/kernelarena/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/tensorforge-webgpu-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/tensorforge-webgpu-light.svg"><img alt="TensorForge browser tensor compiler" src="assets/projects/tensorforge-webgpu-dark.svg" width="100%"></picture></a></td>
<td width="50%"><a href="https://asp53826.github.io/labs/signalroom/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/track-fusion-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/track-fusion-light.svg"><img alt="SignalRoom autonomy mission control" src="assets/projects/track-fusion-dark.svg" width="100%"></picture></a></td>
</tr>
<tr>
<td width="50%"><a href="https://asp53826.github.io/edgar-mcp/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/edgar-mcp-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/edgar-mcp-light.svg"><img alt="EDGAR MCP bounded financial data" src="assets/projects/edgar-mcp-dark.svg" width="100%"></picture></a></td>
<td width="50%"><a href="https://github.com/asp53826/vllm-lite"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/vllm-lite-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/vllm-lite-light.svg"><img alt="vLLM-lite paged inference scheduler" src="assets/projects/vllm-lite-dark.svg" width="100%"></picture></a></td>
</tr>
<tr>
<td width="50%"><a href="https://github.com/asp53826/faultgraph"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/faultgraph-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/faultgraph-light.svg"><img alt="FaultGraph causal incident workbench" src="assets/projects/faultgraph-dark.svg" width="100%"></picture></a></td>
<td width="50%"><a href="https://github.com/asp53826/portfolio-ops"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/portfolio-ops-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/projects/portfolio-ops-light.svg"><img alt="Portfolio Ops autonomous engineering control plane" src="assets/projects/portfolio-ops-dark.svg" width="100%"></picture></a></td>
</tr>
</table>

### Current flagship: COUNTEREXAMPLE

Twelve losing regimes from eight public engines live in one constrained failure
register. Each capsule binds the mechanism, attack, oracle, limitation, exact
source revision, downloadable receipt, and GitHub-signed stable release.

**[Operate the register](https://asp53826.github.io/counterexample/)** ·
**[Inspect the source](https://github.com/asp53826/counterexample)** ·
**[Verify the release](https://github.com/asp53826/counterexample/releases/tag/v1.0.0)** ·
**[Submit a bounded counterexample](https://github.com/asp53826/counterexample/issues/new/choose)**

### Current release: FaultGraph

**[FaultGraph](https://github.com/asp53826/faultgraph)** is a causal incident
analysis workbench for operating on evidence rather than decorating a postmortem.
It combines a FastAPI service, typed event contracts, checksum-addressed SQLite
experiments, server-sent events, and a React/TypeScript forensic console.

| surface | released evidence |
|---|---|
| **Model** | transparent dynamic linear influence model with documented assumptions and bounded `do(source=0)` counterfactuals |
| **Workbench** | dependency graph, event timeline, ranked evidence, competing hypotheses, replay ledger, and keyboard command palette |
| **Verification** | **11 backend + 4 frontend tests**, strict type/lint gates, container build, CodeQL, and zero open security alerts at release |
| **Supply chain** | signed **[v0.1.0](https://github.com/asp53826/faultgraph/releases/tag/v0.1.0)** wheel, workbench archive, checksums, and GitHub attestations |

The model is deliberately bounded: it ranks evidence and executes explicit
interventions; it does not claim unrestricted causal discovery from arbitrary
observational logs.

**[Inspect the workbench](https://github.com/asp53826/faultgraph)** ·
**[Read the architecture](https://github.com/asp53826/faultgraph/blob/main/docs/ARCHITECTURE.md)** ·
**[Audit the research protocol](https://github.com/asp53826/faultgraph/blob/main/docs/RESEARCH_PROTOCOL.md)** ·
**[Verify CI](https://github.com/asp53826/faultgraph/actions/runs/31710995157)**

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-a-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-a-light.svg"><img alt="" src="assets/fun/divider-a-dark.svg" width="100%"></picture>

## Three reproducible passports

| system | mechanism | measured proof | reproduce |
|---|---|---|---|
| **[raft-mvcc](https://github.com/asp53826/raft-mvcc)** | Raft + serializable MVCC + linearizability checking | **598 assertions** across seeded faults; **11-tick** five-node failover | `make test` |
| **[edgar-mcp](https://github.com/asp53826/edgar-mcp)** | bounded SEC tools + cache validation + global pacing | **32 tests**; **138×** warm 10-K read; SEC ceiling enforced | `make test` |
| **[track-fusion](https://github.com/asp53826/track-fusion)** | IMM + JPDA + track scoring + OSPA | **47%** lower localization error in the published winning regime; failure sweep included | `python -m pytest -q` |

<details>
<summary><strong>Clone and run all three</strong></summary>

```bash
git clone https://github.com/asp53826/raft-mvcc && cd raft-mvcc && make test
git clone https://github.com/asp53826/edgar-mcp && cd edgar-mcp && make test
git clone https://github.com/asp53826/track-fusion && cd track-fusion && python -m pip install -e '.[dev]' && python -m pytest -q
```

</details>

## The engineering contract

> Build the mechanism. Attack the assumption. Measure against a named
> baseline. Publish the boundary. Bind the evidence to source.

The portfolio is organized as an engineering laboratory, not a gallery of
screenshots. The interactive pages expose controls; the repositories expose
implementation and tests; the evidence manifest records commands, units, and
limitations.

| instrument | what it exposes |
|---|---|
| **[FAULTLINE](https://asp53826.github.io/labs/faultline/)** | a real C++17 Raft + MVCC engine in WebAssembly, including minority leaders, conflict repair, and passing or failing histories |
| **[KERNELARENA](https://asp53826.github.io/labs/kernelarena/)** | typed tensor IR, fusion, liveness-aware memory reuse, generated WGSL, and a browser-local oracle |
| **[SIGNALROOM](https://asp53826.github.io/labs/signalroom/)** | truth, measurements, residuals, uncertainty, and the manoeuvre regime where an estimator loses |
| **[MARKETWIRE](https://asp53826.github.io/labs/marketwire/)** | toxicity, quote age, inventory control, deterministic shocks, and a committed 20,000-step benchmark |
| **[WITNESS](https://asp53826.github.io/witness/)** | receipt hashing, pinned browser execution, deterministic oracles, tamper detection, and local run receipts |
| **[Benchmark Observatory](https://asp53826.github.io/benchmarks/)** | exact commits, commands, environments, units, baselines, and limitations |
| **[Demo Cinema](https://asp53826.github.io/cinema/)** | four captioned engineering films under one minute with direct routes into the running system |

<details>
<summary><strong>Open the complete source catalog</strong></summary>

### Evidence + reliability

**[faultgraph](https://github.com/asp53826/faultgraph)** ·
**[counterexample](https://github.com/asp53826/counterexample)** ·
**[portfolio-ops](https://github.com/asp53826/portfolio-ops)** ·
**[witness](https://github.com/asp53826/witness)** ·
**[proofgraph](https://github.com/asp53826/proofgraph)**

### Correctness + storage

**[raft-mvcc](https://github.com/asp53826/raft-mvcc)** ·
**[dst-harness](https://github.com/asp53826/dst-harness)** ·
**[hotstuff-bft](https://github.com/asp53826/hotstuff-bft)** ·
**[wal-recovery](https://github.com/asp53826/wal-recovery)** ·
**[lsm-tree](https://github.com/asp53826/lsm-tree)** ·
**[columnar-engine](https://github.com/asp53826/columnar-engine)** ·
**[query-planner](https://github.com/asp53826/query-planner)** ·
**[cdcl-sat](https://github.com/asp53826/cdcl-sat)**

### ML infrastructure

**[tensorforge-webgpu](https://github.com/asp53826/tensorforge-webgpu)** ·
**[vllm-lite](https://github.com/asp53826/vllm-lite)** ·
**[annlite](https://github.com/asp53826/annlite)** ·
**[dist-train](https://github.com/asp53826/dist-train)** ·
**[feature-store](https://github.com/asp53826/feature-store)** ·
**[rag-eval](https://github.com/asp53826/rag-eval)** ·
**[grammar-decode](https://github.com/asp53826/grammar-decode)** ·
**[ptq-budget](https://github.com/asp53826/ptq-budget)** ·
**[agent-harness](https://github.com/asp53826/agent-harness)** ·
**[codebase-qa](https://github.com/asp53826/codebase-qa)**

### Signal + autonomy

**[sdr-receiver](https://github.com/asp53826/sdr-receiver)** ·
**[sar-focus](https://github.com/asp53826/sar-focus)** ·
**[track-fusion](https://github.com/asp53826/track-fusion)** ·
**[vio-nav](https://github.com/asp53826/vio-nav)**

### Financial data + markets

**[edgar-mcp](https://github.com/asp53826/edgar-mcp)** ·
**[xbrl-normalize](https://github.com/asp53826/xbrl-normalize)** ·
**[lob-market-making](https://github.com/asp53826/lob-market-making)** ·
**[aad-greeks](https://github.com/asp53826/aad-greeks)** ·
**[backtest-honest](https://github.com/asp53826/backtest-honest)**

</details>

<details>
<summary><strong>Inspect source-backed telemetry and delivery</strong></summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/telemetry-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/telemetry-light.svg">
  <img alt="Portfolio telemetry generated from public repository source" src="assets/telemetry-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolchain-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/toolchain-light.svg">
  <img alt="Source-backed development and verification toolchain" src="assets/toolchain-dark.svg" width="100%">
</picture>

The daily workflow reads public source and counts test functions without a
third-party stats card or page-load API call. Parametrized and looped suites
execute more checks than the function count—for example, `raft-mvcc` alone
executes 598 assertions.

</details>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-b-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-b-light.svg"><img alt="" src="assets/fun/divider-b-dark.svg" width="100%"></picture>

## Autonomous operations

**[Portfolio Ops](https://github.com/asp53826/portfolio-ops)** maintains the
public systems through eight auditable roles: repository verification,
benchmark evidence, dependency care, documentation checks, demo monitoring,
verified releases, achievement-state monitoring, and profile curation.
Automation uses the GitHub Actions bot identity, retains raw evidence, and does
not manufacture human contributions or interact with third-party repositories.

Patch dependency updates may auto-merge only after repository checks pass.
Source changes, major upgrades, external contributions, benchmark claims, and
account or legal decisions remain outside the autonomous boundary.

<!-- portfolio-status:start -->
| Project | Primary language | Latest release | Latest completed workflow |
|---|---|---|---|
| [faultgraph](https://github.com/asp53826/faultgraph) | Python | [v0.1.0](https://github.com/asp53826/faultgraph/releases/tag/v0.1.0) | [Autonomous Engineering Lab: success](https://github.com/asp53826/faultgraph/actions/runs/39271662733) |
| [raft-mvcc](https://github.com/asp53826/raft-mvcc) | C++ | [v1.0.0](https://github.com/asp53826/raft-mvcc/releases/tag/v1.0.0) | [Autonomous Engineering Lab: success](https://github.com/asp53826/raft-mvcc/actions/runs/38563197098) |
| [edgar-mcp](https://github.com/asp53826/edgar-mcp) | Python | [v0.1.0](https://github.com/asp53826/edgar-mcp/releases/tag/v0.1.0) | [Autonomous Engineering Lab: success](https://github.com/asp53826/edgar-mcp/actions/runs/39257502955) |
| [track-fusion](https://github.com/asp53826/track-fusion) | Python | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/track-fusion/actions/runs/38413934806) |
| [tensorforge-webgpu](https://github.com/asp53826/tensorforge-webgpu) | TypeScript | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/tensorforge-webgpu/actions/runs/38748950302) |
| [columnar-engine](https://github.com/asp53826/columnar-engine) | C++ | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/columnar-engine/actions/runs/38563197276) |
| [lsm-tree](https://github.com/asp53826/lsm-tree) | C++ | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/lsm-tree/actions/runs/38428927465) |
| [counterexample](https://github.com/asp53826/counterexample) | CSS | [v1.0.0](https://github.com/asp53826/counterexample/releases/tag/v1.0.0) | [OpenSSF Scorecard: success](https://github.com/asp53826/counterexample/actions/runs/38411648702) |
| [portfolio-ops](https://github.com/asp53826/portfolio-ops) | Python | No published release | [Achievement Scout: success](https://github.com/asp53826/portfolio-ops/actions/runs/39273509369) |

This block is regenerated only when GitHub's repository, release, or workflow data changes.
<!-- portfolio-status:end -->

<details>
<summary><kbd>↑</kbd> <kbd>↑</kbd> <kbd>↓</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> <kbd>←</kbd> <kbd>→</kbd> <kbd>B</kbd> <kbd>A</kbd></summary>
<br>

<a href="https://asp53826.github.io/labs/faultline/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/secret-level-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/secret-level-light.svg"><img alt="Secret level: isolating N1 leaves two leaders in two terms; healing makes N1 step down, rolls back its conflicting entries, and unlocks an achievement." src="assets/fun/secret-level-dark.svg" width="100%"></picture></a>

<sub>That was a cartoon. <a href="https://asp53826.github.io/labs/faultline/">FAULTLINE</a> runs the real C++17 Raft engine in your browser, so you can isolate the leader yourself and watch the safety check decide.</sub>

</details>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/divider-c-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/divider-c-light.svg"><img alt="" src="assets/fun/divider-c-dark.svg" width="100%"></picture>

## Open channel

**[aaryansp26@gmail.com](mailto:aaryansp26@gmail.com)** ·
**[Systems résumé](https://asp53826.github.io/resume/Aaryan-Patel-Systems-Resume.pdf)** ·
**[Systems Observatory](https://asp53826.github.io/)** ·
**[LinkedIn](https://www.linkedin.com/in/aaryanpatelsystems/)**

**[Engineering OS](https://asp53826.github.io/recruiter/)** ·
**[Proof tours](https://asp53826.github.io/tours/)** ·
**[PROOFGRAPH](https://asp53826.github.io/proofgraph/)** ·
**[Evidence manifest](https://asp53826.github.io/data/evidence.json)**

UGA computer science, December 2026. Industrial data engineering at
**MP Equipment**. Every system above is MIT licensed: clone one, run the
benchmark, and inspect the regime where it breaks.

<a href="https://asp53826.github.io/lab/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/fun/patrol-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/fun/patrol-light.svg"><img alt="Thanks for playing: a small robot walks the commit log and zaps split-brain, stale-read, lost-write and off-by-one bugs, turning each one into a test." src="assets/fun/patrol-dark.svg" width="100%"></picture></a>

<sub>All profile visuals are first-party SVGs generated in this repository; the play layer comes from
<code>scripts/arcade.py</code>. Every animation is plain CSS and stops under <code>prefers-reduced-motion</code>.
Psst: there is a secret level above the contact links.</sub>
