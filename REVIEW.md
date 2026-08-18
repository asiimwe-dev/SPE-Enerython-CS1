# Project Audit — CS #1: Data Center Architecture & Load Profiling

**SPE AMTS Energython 2026**
**Personal review document — not for repository**

---

## Table of Contents

1. [Project Origin & Journey](#1-project-origin--journey)
2. [All Assumptions](#2-all-assumptions)
3. [What is built](#3-what-is-built)
4. [Gap Analysis vs. Competition Brief](#4-gap-analysis-vs-competition-brief)
5. [Potential Judge Questions & Answers](#5-potential-judge-questions--answers)
6. [Questions for Team Members](#6-questions-for-team-members)

---

## 1. Project Origin & Journey

### Where We Started

The repository began as **4 markdown files** copied from the competition briefs:

- `SPE-Energython-overview.md` — master competition document
- `Data-Center-Architecture-and-Load-Profiling.md` — CS #1's primary spec (417 lines)
- `Data-Center-Optimization.md` — industry reference on 10–20 MW DC design
- `TECHNO-ECONOMIC MODEL FOR ENERGYTHON 2026.md` — CS #1 deliverable specification

No code. No config. No tests. Just competition requirements and domain context.

### What Happened

We built a full Python analytical engine from scratch in a single session, going through three conceptual phases:

**Phase A — Single-phase 15 MW baseline**

- Initial implementation matched the competition brief's exact numbers: 15 MW gross, PUE 1.25, 12 MW IT, 360 racks
- 3 scenarios (Cloud-Heavy, AI-Heavy, Mixed), 8760-hour profiles
- Single PUE target, no scaling logic

**Phase B — 3-phase deployment strategy**

- Recognized that starting at full 15 MW is unrealistic for a new facility
- Designed 3-phase deployment: 10 MW → 15 MW → 20 MW
- PUE improves with scale (1.30 → 1.25 → 1.20) due to chiller utilization
- Zone-based deployment: Cloud-first, HPC expansion, AI immersion last

**Phase C — Full integration + documentation**

- All modules made phase-aware with backward-compatible defaults
- MVP dashboard expanded to 4 figures (added phase comparison)
- Documentation updated across all deliverables
- 31 tests passing, `make all` clean

### Current State

| Metric            | Value                                              |
| ----------------- | -------------------------------------------------- |
| Git commits       | 1 (`4d11923`, 2026-08-18)                          |
| Source files      | 18 Python files across 4 modules                   |
| Tests             | 31 passing (10 sizing + 12 PUE + 9 load profiling) |
| Config parameters | ~50 tunable values in `parameters.yaml`            |
| Output CSVs       | 12 (9 phased + 3 legacy)                           |
| Output figures    | 8 PNGs                                             |
| Lines of code     | ~1,800 (source) + ~400 (tests)                     |

---

## 2. All Assumptions

### 2.1 Power & Capacity

| #   | Assumption                                      | Source                         | Confidence     | Risk if Wrong                                       |
| --- | ----------------------------------------------- | ------------------------------ | -------------- | --------------------------------------------------- |
| P1  | Gross generation cap = 15 MW (Phase 2 baseline) | Competition brief §3.1         | ✅ Fact        | —                                                   |
| P2  | IT Load = Gross / PUE                           | Competition brief §3.1 formula | ✅ Fact        | —                                                   |
| P3  | Phase 1 = 10 MW gross                           | Our design choice              | ⚠️ Placeholder | Could be too small for first customer commitments   |
| P4  | Phase 3 = 20 MW gross                           | Competition brief upper bound  | ⚠️ Placeholder | Grid interconnection may not support 20 MW          |
| P5  | 800V DC distribution                            | Industry reference §Power      | ⚠️ Placeholder | Depends on electrical engineer's single-line design |
| P6  | N+1 redundancy for Zones A/B, 2N for Zone C     | Industry best practice         | ⚠️ Placeholder | Electrical engineer must confirm                    |
| P7  | Modular UPS (250–2500 kVA blocks)               | Industry reference §Power      | ⚠️ Placeholder | Depends on vendor selection                         |

### 2.2 Cooling & PUE

| #   | Assumption                                         | Source                                 | Confidence     | Risk if Wrong                                                         |
| --- | -------------------------------------------------- | -------------------------------------- | -------------- | --------------------------------------------------------------------- |
| C1  | Target PUE = 1.25 at 15 MW (Phase 2)               | Competition brief §3.1                 | ✅ Fact        | —                                                                     |
| C2  | PUE 1.30 at 10 MW (partial load penalty)           | Our design — chiller utilization logic | 🔴 Risk        | Must validate with ME. If PUE is 1.35 at Phase 1, IT drops to 7.41 MW |
| C3  | PUE 1.20 at 20 MW (near-optimal efficiency)        | Our design — chiller utilization logic | 🔴 Risk        | Must validate. If PUE floors at 1.22, Phase 3 IT = 16.39 MW           |
| C4  | Hybrid mix: 40% air, 35% D2C, 25% immersion        | Our design choice                      | ⚠️ Placeholder | Mechanical engineer must confirm this is achievable                   |
| C5  | Design temperature = 35°C dry-bulb                 | Competition brief §5                   | ✅ Fact        | —                                                                     |
| C6  | Humidity = 70%                                     | Industry reference                     | ⚠️ Placeholder | Actual site data needed                                               |
| C7  | Air-side economizers ineffective (wet-bulb > 24°C) | Tropical climate physics               | ✅ Fact        | —                                                                     |
| C8  | Liquid Cp ≈ 2.1 kJ/kg·K (dielectric fluid)         | Industry reference                     | ✅ Fact        | —                                                                     |
| C9  | Weighted PUE = 1.394 (calculated) vs target 1.25   | Our calculation                        | 🔴 Risk        | The 0.144 gap is hand-wavy. Judges may push on this.                  |
| C10 | Chiller utilization = gross / 20 MW × 100          | Our simplification                     | ⚠️ Placeholder | Real utilization depends on actual chiller sizing                     |

### 2.3 Workload & Load Profiling

| #   | Assumption                                            | Source                          | Confidence     | Risk if Wrong                                      |
| --- | ----------------------------------------------------- | ------------------------------- | -------------- | -------------------------------------------------- |
| W1  | GPU idle power = 30–40% of peak                       | Competition brief §1            | ✅ Fact        | —                                                  |
| W2  | Idle baseline = 35% of peak IT                        | Our design (midpoint of 30–40%) | ⚠️ Placeholder | Could be 30% or 40% — affects minimum load         |
| W3  | Diurnal Gaussian at hour 14, σ=6                      | Our design                      | ⚠️ Placeholder | Real diurnal curves are not perfectly Gaussian     |
| W4  | Weekend reduction = 70% of weekday                    | Our design                      | ⚠️ Placeholder | Some cloud workloads don't dip on weekends         |
| W5  | ±3% Gaussian noise                                    | Our design                      | ⚠️ Placeholder | Real noise may be higher or lower                  |
| W6  | Cloud-Heavy PAR = 1.24, AI-Heavy PAR = 1.07           | Our generation                  | ✅ Derived     | —                                                  |
| W7  | Peak utilization = 95% (cloud), 98% (AI), 92% (mixed) | Our design                      | ⚠️ Placeholder | Industry data suggests AI runs at 95–100% for days |

### 2.4 Zone Topology

| #   | Assumption                                        | Source                 | Confidence     | Risk if Wrong                                          |
| --- | ------------------------------------------------- | ---------------------- | -------------- | ------------------------------------------------------ |
| Z1  | Zone A: 20 kW/rack, 250 racks (Phase 2)           | Competition brief §3.2 | ✅ Fact        | —                                                      |
| Z2  | Zone B: 50 kW/rack, 80 racks (Phase 2)            | Competition brief §3.2 | ✅ Fact        | —                                                      |
| Z3  | Zone C: 100 kW/rack, 30 racks (Phase 2)           | Competition brief §3.2 | ✅ Fact        | —                                                      |
| Z4  | Zone deployment: Cloud-first, HPC second, AI last | Our design choice      | ⚠️ Placeholder | Business logic — needs financial model validation      |
| Z5  | Phase 1 deploys 180/60/10 racks (A/B/C)           | Our design             | ⚠️ Placeholder | Could start with fewer racks if capital is constrained |
| Z6  | Phase 3 expands to 330/120/40 racks               | Our design             | ⚠️ Placeholder | May not need this many if compute density increases    |

### 2.5 Commercial & Financial

| #   | Assumption                                   | Source               | Confidence     | Risk if Wrong                                   |
| --- | -------------------------------------------- | -------------------- | -------------- | ----------------------------------------------- |
| F1  | Revenue = ~$8M/year per MW IT (illustrative) | Our rough estimate   | 🔴 Risk        | Real revenue depends on CS #2's financial model |
| F2  | Take-or-pay is a software scheduling concern | Competition brief §2 | ✅ Fact        | —                                               |
| F3  | VPPA settlement exists                       | Competition brief §2 | ✅ Fact        | —                                               |
| F4  | IT equipment = 60% of total CAPEX            | Industry reference   | ⚠️ Placeholder | Depends on site, local costs, vendor pricing    |

---

## 3. What Is Built

### 3.1 Module Architecture

```
data/config/parameters.yaml  ← single source of truth
       │
   ┌───┼───┐
   │   │   │
it_sizing  pue_analysis  load_profiling  ← independent modules
   │   │   │
   └───┼───┘
       │
     mvp/  ← imports all 3, generates dashboard
       │
  data/output/  ← CSVs + figures
```

### 3.2 Module Inventory

#### `src/it_sizing/` — IT Capacity & Rack Allocation

| File                   | Key Functions                                             | What It Does                                                                       |
| ---------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `topology.py`          | `Zone` dataclass, `load_zones()`, `load_zones_by_phase()` | Loads zone definitions from YAML. Phase-aware variant loads per-phase rack counts. |
| `sizing_calculator.py` | `calculate_it_load()`, `calculate_it_load_by_phase()`     | Core formula: `IT = Gross / PUE`. Phase variant iterates all 3 phases.             |
| `rack_allocation.py`   | `allocate_racks()`, `allocate_racks_by_phase()`           | Distributes racks across zones. Phase variant returns per-phase allocations.       |
| `calculate.py`         | `main()`                                                  | CLI entry point. Prints Phase 2 spec + 3-phase comparison table.                   |

#### `src/pue_analysis/` — PUE Benchmarking

| File                    | Key Functions                                                 | What It Does                                     |
| ----------------------- | ------------------------------------------------------------- | ------------------------------------------------ |
| `pue_calculator.py`     | `calculate_pue()`, `calculate_dcie()`, `energy_breakdown()`   | Math functions with zero-division guards         |
| `cooling_comparison.py` | `comparison_table()`                                          | 4-technology PUE comparison matrix               |
| `tropical_benchmark.py` | `get_tropical_pue_target()`, `get_pue_sensitivity_by_phase()` | Weighted PUE from hybrid mix + phase sensitivity |
| `analyze.py`            | `main()`                                                      | CLI entry point. Full PUE analysis output.       |

#### `src/load_profiling/` — 8760-Hour Demand Curves

| File                   | Key Functions                                                                                       | What It Does                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `scenarios.py`         | `Scenario` dataclass, `load_scenarios()`                                                            | Loads 3 scenario definitions from YAML                                |
| `profile_generator.py` | `generate_load_profiles()`, `generate_all_phase_profiles()`                                         | Core generator with diurnal Gaussian, AI floor, weekend effect, noise |
| `visualize.py`         | `plot_diurnal_curves()`, `plot_annual_curves()`, `plot_facility_vs_it()`, `plot_phase_comparison()` | matplotlib time-series plots                                          |
| `generate.py`          | `main()`                                                                                            | CLI entry point. Generates 9 CSVs + 4 figures.                        |

#### `src/mvp/` — Visual Integration Dashboard

| File                  | Key Functions     | What It Does                                                                        |
| --------------------- | ----------------- | ----------------------------------------------------------------------------------- |
| `dashboard.py`        | `run_dashboard()` | 4-figure dashboard: sizing overview, load profiles, summary table, phase comparison |
| `report_generator.py` | `main()`          | Thin wrapper                                                                        |

### 3.3 Configuration System

All 50+ tunable parameters live in `data/config/parameters.yaml`. No hardcoded constants in source code. Key sections:

- `facility` — default gross MW and PUE (backward compatible)
- `phases` — per-phase MW, PUE, and zone rack counts
- `zones` — rack density definitions per zone type
- `cooling` — hybrid mix percentages
- `cooling_technologies` — PUE ranges per technology
- `tropical_climate` — design temp, humidity, ambient range
- `power` — idle power ratios
- `load_profiling.scenarios` — per-scenario utilization and diurnal params

### 3.4 Test Coverage

| Test File                | Tests | What's Covered                                                                  |
| ------------------------ | ----- | ------------------------------------------------------------------------------- |
| `test_sizing.py`         | 10    | IT load calc, DCiE, overhead, zone allocation, topology loading, zero-edge case |
| `test_pue.py`            | 12    | PUE/DCiE math, zero-division, negative input, cooling table, tropical benchmark |
| `test_load_profiling.py` | 9     | Scenario loading, 8760-hour generation, value ranges, CSV round-trip            |

**What's NOT tested**: Phase-specific functions (`calculate_it_load_by_phase`, `allocate_racks_by_phase`, `generate_all_phase_profiles`, `get_pue_sensitivity_by_phase`). These were added later and tests weren't updated.

### 3.5 Output Artifacts

**12 CSVs** (8760 rows each, hourly resolution):

- 3 legacy (no phase prefix) + 9 phased (phase_1/2/3 x cloud/ai/mixed)
- Schema: `hour, hour_of_day, day_of_year, it_load_kw, facility_load_kw, utilization, scenario`

**8 PNGs**:

- `diurnal_profiles.png` — hour-of-day averaged curves with ±1σ shading
- `annual_profiles.png` — 24h rolling average annual curves
- `facility_vs_it_load.png` — IT vs facility load (cooling overhead shaded)
- `phase_comparison.png` — 3-panel side-by-side diurnal comparison
- `mvp_sizing_overview.png` — 4-panel: zone power, rack pie, energy breakdown, cooling
- `mvp_load_profiles.png` — 3×2 grid: diurnal + annual per scenario
- `mvp_summary_table.png` — formatted stats table
- `mvp_phase_comparison.png` — 4-panel: IT by phase, PUE sensitivity, racks, revenue

---

## 4. Gap Analysis vs. Competition Brief

Cross-referencing against the 4 reference documents to identify what we've done, what's missing, and what's explicitly out of scope.

### 4.1 CS #1 Scope Coverage

| Requirement (from `TECHNO-ECONOMIC MODEL`)                | Status      | Evidence                                                                     |
| --------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------- |
| **IT Sizing**: MW capacity, rack counts, density zones    | ✅ Done     | `make sizing`, `docs/refined/it-sizing-spec.md`                              |
| **Load Profiles**: 8760-hour CSVs, 3 scenarios            | ✅ Done     | `make profiles`, `docs/refined/load-profiling-spec.md`                       |
| **PUE Benchmark**: Target PUE with tropical justification | ✅ Done     | `make pue`, `docs/refined/pue-benchmark-memo.md`                             |
| **Compute vs. Storage breakdown**                         | ❌ Not done | Brief asks for this but we don't distinguish compute from storage power      |
| **Server count estimate**                                 | ❌ Not done | Brief asks for "based on average server wattage (e.g., 1 kW per GPU server)" |

### 4.2 Primary Spec Coverage

From `Data-Center-Architecture-and-Load-Profiling.md` (417-line CS #1 spec):

| Requirement                      | Status      | Evidence                                                       |
| -------------------------------- | ----------- | -------------------------------------------------------------- |
| §3.1 IT Sizing (15 MW baseline)  | ✅ Done     | `calculate_it_load()`                                          |
| §3.2 Rack Density Allocation     | ✅ Done     | `allocate_racks()`                                             |
| §4 Workload Profiling            | ✅ Done     | `generate_load_profiles()`                                     |
| §5 Tropical PUE Benchmarking     | ✅ Done     | `get_tropical_pue_target()`                                    |
| §6 SDLC — Telemetry Architecture | ❌ Not done | Apache Kafka + TimescaleDB not implemented                     |
| §6 SDLC — PID Thermal Control    | ❌ Not done | `DynamicPUEController` class not implemented                   |
| §6 SDLC — Take-or-Pay Dispatcher | ❌ Not done | `TakeOrPayWorkloadScheduler` class not implemented             |
| §6 SDLC — TimescaleDB Schema     | ❌ Not done | Hypertable + materialized view not implemented                 |
| §7 Cross-Role Matrix             | ⚠️ Partial  | We define outputs but haven't received inputs from other roles |
| §8 Team Coordination Checklist   | ✅ Done     | Target IT locked, rack distribution confirmed                  |

### 4.3 What's Explicitly NOT Implemented (and Why)

| Item                                        | Reason                                                                            | Should We Add It?                       |
| ------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------- |
| **Telemetry pipeline** (Kafka, TimescaleDB) | Software engineering deliverable, not analytical. MVP focuses on numerical model. | Maybe — judges may expect it            |
| **PID controller**                          | Brief shows pseudocode for `DynamicPUEController`.                                | Maybe — at minimum, document the design |
| **Take-or-pay dispatcher**                  | Brief shows pseudocode for `TakeOrPayWorkloadScheduler`.                          | Maybe — at minimum, document the design |
| **Hardware-in-the-Loop testing**            | Requires actual hardware/simulators. Not feasible.                                | No — out of scope                       |
| **Edge/cloud hybrid deployment**            | Requires actual infrastructure. Not feasible.                                     | No — out of scope                       |
| **ML heat-rejection model retraining**      | Requires operational data we don't have.                                          | No — out of scope                       |

### 4.4 Industry Reference Coverage

From `Data-Center-Optimization.md` (industry reference):

| Recommendation                                | Status        | Evidence                                                     |
| --------------------------------------------- | ------------- | ------------------------------------------------------------ |
| Deploy in 2–5 MW increments                   | ✅ Done       | 3-phase strategy (5 MW increments)                           |
| 800V DC distribution                          | ⚠️ Documented | Mentioned in sizing spec but not implemented                 |
| Liquid cooling breaks even at >30 kW/rack     | ✅ Addressed  | Zone B (50 kW) uses D2C, Zone C (100 kW) uses immersion      |
| BESS 5–10 MW for peak shaving                 | ❌ Not done   | Out of CS #1 scope — Electrical Eng concern                  |
| Shift 30–40% load to off-peak                 | ❌ Not done   | Scheduling concern, not yet implemented                      |
| Power capping: install 25–30 MW, cap at 20 MW | ⚠️ Documented | Phase 3 is 20 MW but we don't model "install more, cap less" |

---

## 5. Potential Judge Questions & Answers

### Theme 1: PUE Credibility

**Q1: "Your PUE improves from 1.30 to 1.20 as you scale. What's the physical basis for this?"**

> At Phase 1 (10 MW), chillers operate at ~50% capacity. Centrifugal chillers lose 10-15% COP at half load due to part-load inefficiency. At Phase 3 (20 MW), chillers operate at ~95% capacity, achieving near-peak COP. This is a well-documented HVAC phenomenon. The exact PUE values need validation with mechanical engineer COP curves, but the directional claim is physically sound.

**Where in code**: `src/pue_analysis/tropical_benchmark.py:get_pue_sensitivity_by_phase()`

**Q2: "You calculated a weighted PUE of 1.394 but target 1.25. How do you reconcile this 0.14 gap?"**

> The weighted PUE (1.394) is a worst-case blend of individual technology midpoints. The target (1.25) accounts for: (a) immersion-cooled Zone C contributing zero overhead, (b) D2C-cooled Zone B contributing minimal overhead, and (c) not all air-cooled racks run at legacy DX efficiency — modern CRAC units with VFDs perform better than the legacy midpoint. This needs stronger justification with actual manufacturer data.

**Where in docs**: `docs/refined/pue-benchmark-memo.md §5`

**Q3: "The competition brief says tropical PUE is 1.45-1.60 air-cooled, 1.20-1.30 liquid-cooled. Why should we believe 1.25 at only 15 MW?"**

> Our hybrid mix (40% air, 35% D2C, 25% immersion) is not all-air. The 1.25 target sits within the 1.20-1.30 liquid-cooled range from the brief. The air-cooled portion (Zone A, 40% of IT load) pulls PUE up from pure liquid numbers, while the immersion portion (Zone C, 25%) pulls it down. The blend lands at 1.25.

**Where in docs**: `docs/refined/pue-benchmark-memo.md §3, §5`

### Theme 2: Load Profile Realism

**Q4: "Your diurnal curve is a Gaussian. Real data centers don't follow a perfect bell curve."**

> Correct. The Gaussian is a first-order approximation. Real diurnal curves have sharper morning ramps, plateaus during business hours, and gradual evening declines. For the competition, this captures the essential behavior (peak at 2 PM, trough at night). A more realistic model would use measured data or a piecewise function, but the Gaussian is sufficient for sizing purposes where we care about peak-to-average ratio, not exact hourly shapes.

**Where in code**: `src/load_profiling/profile_generator.py:_diurnal_shape()`

**Q5: "Your AI-Heavy scenario has PAR of 1.07. If AI training is truly 95-100% sustained, why isn't PAR closer to 1.0?"**

> Because we model a 35% idle baseline (always-on servers, networking, fans) plus a 70% AI batch floor. The remaining 5% headroom creates small fluctuations from thermal throttling and job transitions. A truly flat line (PAR = 1.0) would imply zero variation, which is unrealistic even for sustained training.

**Where in code**: `src/load_profiling/profile_generator.py` — the `noise` term and clipping logic

**Q6: "Why only 3 scenarios? What about inference-heavy or batch-processing workloads?"**

> The competition brief explicitly defines 3 scenarios: Cloud-Heavy, AI-Heavy, Mixed. We match this exactly. Inference-heavy workloads would behave similarly to Cloud-Heavy (diurnal, bursty). Batch processing would be similar to AI-Heavy (sustained). Adding more scenarios would increase complexity without changing the sizing result, since peak IT load is the same across scenarios.

**Where in docs**: `docs/references/TECHNO-ECONOMIC MODEL FOR ENERGYTHON 2026.md §1`

### Theme 3: Phasing Strategy

**Q7: "Why start at 10 MW instead of going straight to 15 MW?"**

> Three reasons: (a) reduced upfront CAPEX — don't build cooling capacity before you have customers, (b) PUE improves with scale — starting small and scaling demonstrates operational maturity, (c) grid interconnection lead times are 24-36 months — you may not get 15 MW connection on day one. The 10 MW starting point gives a realistic initial deployment while the grid connection scales up.

**Where in docs**: `docs/refined/it-sizing-spec.md §6`, `docs/refined/pue-benchmark-memo.md §8`

**Q8: "Your Phase 3 assumes 20 MW grid connection. Is that realistic for tropical Africa?"**

> This is a valid concern. The competition brief lists 10-20 MW as the range. Grid interconnection at 20 MW requires dedicated 13.8 kV medium-voltage feed with 24-36 month lead time (per industry reference). In some African markets, this may require dedicated generation instead of grid connection. This needs validation with the electrical engineer and petroleum engineer (for gas supply at 20 MW).

**Where in docs**: `docs/refined/it-sizing-spec.md §5`

### Theme 4: Financial Viability

**Q9: "What's the revenue per MW IT? How did you get $8M/year?"**

> The $8M/MW figure in the MVP dashboard is illustrative only. Real revenue depends on: (a) contract mix (reserved vs. spot vs. on-demand), (b) market rates in the target country, (c) PPA structures, and (d) utilization rates. CS #2's financial model should provide this number. We included it in the dashboard to show the revenue scaling across phases, but it must be replaced with actual financial projections.

**Where in code**: `src/mvp/dashboard.py` — the `revenue_per_mw = 8` variable

**Q10: "How does PUE sensitivity affect LCOE?"**

> Every 0.01 improvement in PUE at 15 MW saves approximately 120 kW of cooling overhead, which translates to ~1,050 MWh/year of fuel. At $8/MMBtu, that's ~$30,000/year. Over 20 years, a 0.05 PUE improvement (1.30 to 1.25) saves ~$3M in fuel OPEX. This is material for NPV calculations and directly feeds CS #2's model.

**Where in docs**: `docs/refined/pue-benchmark-memo.md §7`

### Theme 5: Technical Depth

**Q11: "You mention 800V DC distribution and modular UPS but don't model them. Why?"**

> These are electrical engineering decisions that affect CAPEX and parasitic losses. Our scope is IT sizing and load profiling — we define the demand side. The electrical engineer defines the supply side (generator, UPS, distribution). We document the 800V DC recommendation in the sizing spec based on industry best practice (45% copper reduction), but the actual implementation depends on vendor selection and single-line design.

**Where in docs**: `docs/refined/it-sizing-spec.md §5`

**Q12: "Your idle power is 35%. The competition brief says 30-40% for GPUs. What about CPUs?"**

> We use 35% as a midpoint for the blended idle ratio across all rack types. CPU-only racks (Zone A) may idle at 20-30%, while GPU racks (Zone C) idle at 30-40%. A more precise model would set different idle ratios per zone, but for facility-level sizing, the blended 35% is sufficient. The competition brief's 30-40% range applies specifically to GPU servers.

**Where in code**: `data/config/parameters.yaml` — `power.idle_power_ratio: 0.35`

**Q13: "Why ±3% noise? Where does that come from?"**

> It's a reasonable approximation for stochastic variation from: thermal throttling, minor load shifts, fan speed adjustments, and measurement uncertainty. The exact value doesn't materially affect sizing (which depends on peak, not noise). A larger noise band (±5%) would slightly increase peak clips; a smaller band (±1%) would be unrealistically smooth. ±3% is a conservative middle ground.

**Where in code**: `src/load_profiling/profile_generator.py` — `np.random.normal(0, 0.03, hours)`

### Theme 6: Competition Deliverables

**Q14: "The brief asks for a PID controller and take-or-pay dispatcher. Where are they?"**

> These are software engineering deliverables listed in the SDLC section of the primary spec. Our current implementation focuses on the analytical model (sizing, profiling, PUE benchmarking). The PID controller and take-or-pay dispatcher are algorithmic modules that would be implemented in a production system. For the competition, we've documented the design intent in the sizing spec and load profiling spec, but haven't written the actual control code. This is a gap we should address — at minimum by adding pseudocode or design documents.

**Where in docs**: `docs/references/Data-Center-Architecture-and-Load-Profiling.md §6`

**Q15: "The brief mentions TimescaleDB hypertables. Is your telemetry architecture real?"**

> No. The TimescaleDB schema and Kafka pipeline are architectural designs in the competition brief, not implementations. Our code generates static CSVs and PNGs. A production system would stream telemetry to TimescaleDB and run real-time PUE calculations. For the competition, we should document this architecture as a design decision, noting that the analytical model feeds into it.

**Where in docs**: `docs/references/Data-Center-Architecture-and-Load-Profiling.md §6.3`

**Q16: "What cross-role data have you actually exchanged with other team members?"**

> So far, none. This is a solo implementation based on competition brief assumptions. The sizing spec documents what we need from each role (fuel cost from Petroleum, COP curves from Mechanical, CAPEX from Electrical), but we haven't received any of these inputs yet. The PUE values, in particular, are placeholders that must be validated with the mechanical engineer.

**Where in docs**: `docs/refined/it-sizing-spec.md §6`, `docs/refined/pue-benchmark-memo.md §8`

---

## 6. Questions for Team Members

These are specific questions our implementation surfaces that need answers from each team role to make the model production-ready.

### 6.1 For Petroleum Engineer

| #   | Question                                                                           | Why It Matters                                                                                                                         | Our Current Assumption            |
| --- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| PE1 | What's the delivered fuel cost ($/MMBtu) for natural gas at the target site?       | Directly affects OPEX and LCOE. CS #2 needs this for financial model.                                                                  | None — we don't model fuel cost   |
| PE2 | What are the take-or-pay contract terms (minimum hourly gas volume, penalty rate)? | The competition brief mentions take-or-pay as a software scheduling concern. We need the contractual numbers to design the dispatcher. | None — we don't model take-or-pay |
| PE3 | Is the gas supply pipeline-ready, or do we need LNG/CNG trucks?                    | Pipeline gas is cheaper but requires infrastructure. Trucked gas is more expensive but faster to deploy.                               | None — we assume pipeline         |
| PE4 | What's the gas supply pressure and flow rate capacity?                             | Determines maximum hourly fuel consumption, which caps generation capacity.                                                            | None                              |
| PE5 | Are there seasonal supply variations?                                              | Some regions have gas supply constraints in dry season. Would affect load scheduling.                                                  | None — we assume constant supply  |

### 6.2 For Mechanical Engineer

| #   | Question                                                                                | Why It Matters                                                                                                                                                                                  | Our Current Assumption                         |
| --- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| ME1 | **What are the actual chiller COP curves at 50%, 75%, and 95% load?**                   | This is the #1 unknown. Our PUE-by-phase values (1.30/1.25/1.20) are based on a simplified chiller utilization model. Real COP curves would validate or invalidate the entire phasing strategy. | PUE improves linearly with chiller utilization |
| ME2 | What's the actual hybrid cooling mix we can achieve? (40% air, 35% D2C, 25% immersion)  | This determines the weighted PUE. If we can't achieve 25% immersion (maybe only 15%), PUE goes up.                                                                                              | 40/35/25 split                                 |
| ME3 | What are the COP curves for the D2C and immersion systems at the target ambient (35°C)? | Liquid cooling is "less sensitive" to ambient, but not immune. We need actual numbers.                                                                                                          | Immersion PUE 1.08-1.15, D2C PUE 1.18-1.25     |
| ME4 | What's the thermal design margin? Do we oversize cooling by 10%, 20%, 30%?              | Oversizing affects both CAPEX and part-load PUE. If we oversize by 30%, Phase 1 PUE could be worse than 1.30.                                                                                   | We don't model oversizing margin               |
| ME5 | What's the water availability at the site? Affects evaporative cooling viability.       | Chilled water + evaporative towers need significant water. In water-scarce areas, immersion is preferred.                                                                                       | We assume water is available                   |
| ME6 | Can you confirm the dielectric fluid Cp (2.1 kJ/kg·K) and flow rates for Zone C?        | Used in thermal load calculations for immersion cooling design.                                                                                                                                 | Cp = 2.1 kJ/kg·K from industry reference       |

### 6.3 For Electrical Engineer

| #   | Question                                                                      | Why It Matters                                                                                                         | Our Current Assumption                    |
| --- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| EE1 | What generator technology are we using (gas engine CHP, CCGT, reciprocating)? | Affects electrical efficiency (43-48% for gas engines, 50-55% for CCGT) and waste heat availability for cooling.       | None — we assume gross MW as given        |
| EE2 | What's the grid interconnection voltage and available capacity?               | Determines if 20 MW (Phase 3) is achievable. Some sites may cap at 15 MW.                                              | 13.8 kV MV feed assumed                   |
| EE3 | What's the UPS topology and efficiency?                                       | UPS losses are part of PUE overhead. At 96% efficiency, a 12 MW IT load adds 480 kW UPS loss.                          | We model UPS loss as part of PUE overhead |
| EE4 | What's the generator response time for load steps?                            | Affects how quickly we can ramp AI jobs. If generator takes 30 seconds to respond, we can't do rapid burst scheduling. | None — we don't model ramp rates          |
| EE5 | What's the power factor at each zone?                                         | Low power factor increases apparent power and affects generator/transformer sizing.                                    | We assume unity power factor              |
| EE6 | Are we designing for N+1 or 2N redundancy? Affects available IT capacity.     | If generators are N+1, one unit is always idle (backup). Available capacity = nameplate x (N/(N+1)).                   | We assume N+1 for A/B, 2N for C           |

### 6.4 For CS #2 (Financial Model)

| #     | Question                                                              | Why It Matters                                                                                        | Our Current Assumption   |
| ----- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------ |
| CS2-1 | What revenue per MW IT should we use? ($/MW/year or $/kWh)            | The MVP dashboard uses $8M/MW (illustrative). Real number needed for phase comparison.                | $8M/MW illustrative      |
| CS2-2 | What discount rate and project lifetime should we use for NPV?        | Affects whether Phase 1 alone is viable or if Phase 3 is needed for positive NPV.                     | None                     |
| CS2-3 | How does the take-or-pay shortfall penalty affect operating income?   | If we under-consume gas, we pay penalties. This affects minimum load scheduling.                      | None                     |
| CS2-4 | What's the target IRR for the project?                                | Determines whether the phased approach is acceptable or if investors require full 15 MW from day one. | None                     |
| CS2-5 | Should we model different PPA structures (VPPA, bilateral, merchant)? | Different structures have different risk/return profiles. Affects which phase is most profitable.     | None                     |
| CS2-6 | How should we handle the PUE sensitivity in the financial model?      | Should CS #2 use our phased PUE values (1.30/1.25/1.20) or a single blended value?                    | We provide phased values |

### 6.5 For Self (CS #1 — Implementation Gaps)

| #      | Question                                                                      | Priority | Effort       |
| ------ | ----------------------------------------------------------------------------- | -------- | ------------ |
| CS1-1  | Should we implement the PID controller pseudocode from the competition brief? | Medium   | 2-3 hours    |
| CS1-2  | Should we implement the take-or-pay dispatcher pseudocode?                    | Medium   | 2-3 hours    |
| CS1-3  | Should we add the TimescaleDB schema as a design artifact?                    | Low      | 1 hour       |
| CS1-4  | Should we add compute vs. storage power breakdown?                            | Medium   | 2-3 hours    |
| CS1-5  | Should we add server count estimates?                                         | Low      | 1 hour       |
| CS1-6  | Should we update tests to cover phase-specific functions?                     | High     | 2 hours      |
| CS1-7  | Should we add per-zone idle ratios instead of a global 35%?                   | Low      | 2 hours      |
| CS1-8  | Should we replace the Gaussian diurnal with a more realistic piecewise model? | Low      | 3-4 hours    |
| CS1-9  | Should we model power capping (install 25 MW, cap at 20 MW)?                  | Low      | 2 hours      |
| CS1-10 | Should we add a BESS/peak-shaving model?                                      | Low      | Out of scope |

---

## Appendix A: Key Numbers Quick Reference

| Metric         | Phase 1           | Phase 2           | Phase 3           |
| -------------- | ----------------- | ----------------- | ----------------- |
| Gross MW       | 10.0              | 15.0              | 20.0              |
| PUE            | 1.30              | 1.25              | 1.20              |
| IT MW          | 7.69              | 12.00             | 16.67             |
| DCiE           | 76.9%             | 80.0%             | 83.3%             |
| Total Racks    | 250               | 360               | 490               |
| Zone A (Cloud) | 180 racks, 3.6 MW | 250 racks, 5.0 MW | 330 racks, 6.6 MW |
| Zone B (HPC)   | 60 racks, 3.0 MW  | 80 racks, 4.0 MW  | 120 racks, 6.0 MW |
| Zone C (AI)    | 10 racks, 1.0 MW  | 30 racks, 3.0 MW  | 40 racks, 4.0 MW  |
| Chiller Util % | ~50%              | ~75%              | ~95%              |

### Scenario Metrics (Phase 2 / 15 MW)

| Scenario    | Avg IT (MW) | Peak IT (MW) | Min IT (MW) | PAR  |
| ----------- | ----------- | ------------ | ----------- | ---- |
| Cloud-Heavy | 10.13       | 12.60        | 7.75        | 1.24 |
| AI-Heavy    | 11.76       | 12.60        | 10.24       | 1.07 |
| Mixed       | 10.83       | 12.60        | 9.09        | 1.16 |

---

## Appendix B: File Inventory

### Source Files (18)

```
src/__init__.py
src/it_sizing/__init__.py
src/it_sizing/topology.py
src/it_sizing/sizing_calculator.py
src/it_sizing/rack_allocation.py
src/it_sizing/calculate.py
src/pue_analysis/__init__.py
src/pue_analysis/pue_calculator.py
src/pue_analysis/cooling_comparison.py
src/pue_analysis/tropical_benchmark.py
src/pue_analysis/analyze.py
src/load_profiling/__init__.py
src/load_profiling/scenarios.py
src/load_profiling/profile_generator.py
src/load_profiling/visualize.py
src/load_profiling/generate.py
src/mvp/__init__.py
src/mvp/dashboard.py
src/mvp/report_generator.py
```

### Test Files (3)

```
tests/test_sizing.py      (10 tests)
tests/test_pue.py         (12 tests)
tests/test_load_profiling.py  (9 tests)
```

### Config (1)

```
data/config/parameters.yaml  (117 lines, ~50 parameters)
```

### Documentation (7)

```
README.md
ARCHITECTURE.md
AGENTS.md
CLAUDE.md
docs/refined/it-sizing-spec.md
docs/refined/pue-benchmark-memo.md
docs/refined/load-profiling-spec.md
```

### References (4, read-only)

```
docs/references/SPE-Energython-overview.md
docs/references/Data-Center-Architecture-and-Load-Profiling.md
docs/references/Data-Center-Optimization.md
docs/references/TECHNO-ECONOMIC MODEL FOR ENERGYTHON 2026.md
```
