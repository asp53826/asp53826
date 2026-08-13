<picture>
  <source media="(prefers-color-scheme: dark)" srcset="banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="banner-light.svg">
  <img alt="Aaryan Patel — systems and ML infrastructure engineer whose public claims pass through attack, oracle, boundary, and receipt" src="banner-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="https://asp53826.github.io/counterexample/"><strong>ENTER COUNTEREXAMPLE</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/proofgraph/"><strong>OPEN PROOFGRAPH</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/recruiter/"><strong>OPEN ENGINEERING OS</strong></a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/tours/">TAKE A PROOF TOUR</a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/resume/Aaryan-Patel-Systems-Resume.pdf">RÉSUMÉ</a>&nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://asp53826.github.io/data/evidence.json">EVIDENCE MANIFEST</a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/proof-bus-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/proof-bus-light.svg">
  <img alt="Verification bus: claim, attack, oracle, boundary, and receipt" src="assets/proof-bus-dark.svg" width="100%">
</picture>

## Choose your route

| [<img alt="Open Systems route" src="assets/routes/systems-dark.svg" width="100%">](https://asp53826.github.io/systems/) | [<img alt="Open ML Infrastructure route" src="assets/routes/ml-infrastructure-dark.svg" width="100%">](https://asp53826.github.io/ml-infrastructure/) | [<img alt="Open Autonomy route" src="assets/routes/defense-dark.svg" width="100%">](https://asp53826.github.io/defense/) | [<img alt="Open Quant route" src="assets/routes/quant-dark.svg" width="100%">](https://asp53826.github.io/quant/) |
|---|---|---|---|

Each route is a short, role-specific path through live systems, source, tests,
measured evidence, and the regime where the result stops holding.

**[PROOFGRAPH](https://asp53826.github.io/proofgraph/)** is the interactive
router across those routes: choose a hiring lens, then traverse one claim
through its attack, oracle, measurement, boundary, exact source revision, and
signed receipt.

## Six proof cartridges

| [<img alt="COUNTEREXAMPLE public failure register" src="assets/projects/counterexample-dark.svg" width="100%">](https://asp53826.github.io/counterexample/) | [<img alt="Raft and MVCC consensus under attack" src="assets/projects/raft-mvcc-dark.svg" width="100%">](https://asp53826.github.io/labs/faultline/) |
|---|---|
| [<img alt="TensorForge browser tensor compiler" src="assets/projects/tensorforge-webgpu-dark.svg" width="100%">](https://asp53826.github.io/labs/kernelarena/) | [<img alt="SignalRoom autonomy mission control" src="assets/projects/track-fusion-dark.svg" width="100%">](https://asp53826.github.io/labs/signalroom/) |
| [<img alt="EDGAR MCP bounded financial data" src="assets/projects/edgar-mcp-dark.svg" width="100%">](https://asp53826.github.io/edgar-mcp/) | [<img alt="vLLM-lite paged inference scheduler" src="assets/projects/vllm-lite-dark.svg" width="100%">](https://github.com/asp53826/vllm-lite) |

### Current flagship: COUNTEREXAMPLE

Twelve losing regimes from eight public engines live in one constrained failure
register. Each capsule binds the mechanism, attack, oracle, limitation, exact
source revision, downloadable receipt, and GitHub-signed stable release.

**[Operate the register](https://asp53826.github.io/counterexample/)** ·
**[Inspect the source](https://github.com/asp53826/counterexample)** ·
**[Verify the release](https://github.com/asp53826/counterexample/releases/tag/v1.0.0)** ·
**[Submit a bounded counterexample](https://github.com/asp53826/counterexample/issues/new/choose)**

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
| **[Benchmark Observatory](https://asp53826.github.io/benchmarks/)** | exact commits, commands, environments, units, baselines, and limitations |
| **[Demo Cinema](https://asp53826.github.io/cinema/)** | four captioned engineering films under one minute with direct routes into the running system |

<details>
<summary><strong>Open the complete source catalog</strong></summary>

### Correctness + storage

**[counterexample](https://github.com/asp53826/counterexample)** ·
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
| [raft-mvcc](https://github.com/asp53826/raft-mvcc) | C++ | [v1.0.0](https://github.com/asp53826/raft-mvcc/releases/tag/v1.0.0) | [Autonomous Engineering Lab: success](https://github.com/asp53826/raft-mvcc/actions/runs/31705422333) |
| [edgar-mcp](https://github.com/asp53826/edgar-mcp) | Python | [v0.1.0](https://github.com/asp53826/edgar-mcp/releases/tag/v0.1.0) | [Autonomous Engineering Lab: success](https://github.com/asp53826/edgar-mcp/actions/runs/31705797339) |
| [track-fusion](https://github.com/asp53826/track-fusion) | Python | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/track-fusion/actions/runs/31705678908) |
| [tensorforge-webgpu](https://github.com/asp53826/tensorforge-webgpu) | TypeScript | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/tensorforge-webgpu/actions/runs/31705451182) |
| [columnar-engine](https://github.com/asp53826/columnar-engine) | C++ | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/columnar-engine/actions/runs/31705462306) |
| [lsm-tree](https://github.com/asp53826/lsm-tree) | C++ | No published release | [Autonomous Engineering Lab: success](https://github.com/asp53826/lsm-tree/actions/runs/31705519571) |
| [counterexample](https://github.com/asp53826/counterexample) | CSS | [v1.0.0](https://github.com/asp53826/counterexample/releases/tag/v1.0.0) | [OpenSSF Scorecard: success](https://github.com/asp53826/counterexample/actions/runs/31469800250) |
| [portfolio-ops](https://github.com/asp53826/portfolio-ops) | Python | No published release | [Control Plane CI: success](https://github.com/asp53826/portfolio-ops/actions/runs/31706473274) |

This block is regenerated only when GitHub's repository, release, or workflow data changes.
<!-- portfolio-status:end -->

## Open channel

**[aaryansp26@gmail.com](mailto:aaryansp26@gmail.com)** ·
**[Systems résumé](https://asp53826.github.io/resume/Aaryan-Patel-Systems-Resume.pdf)** ·
**[Systems Observatory](https://asp53826.github.io/)** ·
**[LinkedIn](https://www.linkedin.com/in/aaryanpatelsystems/)**

UGA computer science, December 2026. Industrial data engineering at
**MP Equipment**. Every system above is MIT licensed: clone one, run the
benchmark, and inspect the regime where it breaks.

<sub>All profile visuals are first-party SVGs generated in this repository.
Motion is limited to signal flow and respects <code>prefers-reduced-motion</code>.</sub>
