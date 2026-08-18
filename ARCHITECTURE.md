# Architecture

Implementation details for the Data Center Architecture & Load Profiling engine.

## System Overview

```
                    data/config/parameters.yaml
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
        │  it_sizing  │ │ pue_analysis│ │ load_profiling  │
        │             │ │             │ │                 │
        │ IT = G / P  │ │ PUE math    │ │ Diurnal model   │
        │ Zone alloc  │ │ Cooling cmp │ │ Scenario gen    │
        │ Rack counts │ │ Tropical    │ │ CSV + plots     │
        │ Phase aware │ │ Phase aware │ │ Phase aware     │
        └──────┬──────┘ └──────┬──────┘ └────────┬────────┘
               │               │                 │
               └───────────────┼─────────────────┘
                               ▼
                        ┌─────────────┐
                        │    mvp/     │
                        │  Dashboard  │
                        │  (4 figs)   │
                        └─────────────┘
                               │
                               ▼
                     data/output/
                     ├── csv/        (9 CSVs, 8760 rows each)
                     └── figures/    (8 PNGs)
```

All three analytical modules read from the same `parameters.yaml` config. They are independent of each other — you can run `make sizing` without running `make pue` or `make profiles`. The `mvp/` module imports from all three to produce the integrated dashboard.

**Phase-aware design**: Every module exports both single-phase (backward compatible) and multi-phase functions. Phase functions accept a `phase_key` parameter (`phase_1`, `phase_2`, `phase_3`) and return phase-specific results.

## Module Map

| Module                | Purpose                    | Key Functions                                                                                                          | Output                                        |
| --------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `src/it_sizing/`      | Capacity and rack planning | `calculate_it_load()`, `calculate_it_load_by_phase()`, `allocate_racks()`, `allocate_racks_by_phase()`                 | Zone tables, rack counts, 3-phase comparison  |
| `src/pue_analysis/`   | Efficiency benchmarking    | `calculate_pue()`, `comparison_table()`, `get_tropical_pue_target()`, `get_pue_sensitivity_by_phase()`                 | PUE/DCiE metrics, phase sensitivity           |
| `src/load_profiling/` | Demand curve generation    | `generate_load_profiles()`, `generate_all_phase_profiles()`, `save_profiles()`, `plot_all()`, `plot_all_with_phases()` | 9 CSVs (3×3), time-series plots               |
| `src/mvp/`            | Visual integration         | `run_dashboard()`                                                                                                      | 4 dashboard PNGs (sizing + profiles + phases) |

## Configuration System

Every module resolves its config path the same way:

```python
CONFIG_PATH = Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"
```

This walks up from the module file to the repo root, then into `data/config/`. All domain values are centralized in `parameters.yaml` — no hardcoded constants in source code.

**To add a new parameter**: Add the key to `parameters.yaml`, then access it in the module via `cfg["section"]["key"]`. No schema validation exists yet — if the YAML key is missing, you'll get a `KeyError`.

### Config Sections

| Section                    | Used By                              | What It Controls                                                 |
| -------------------------- | ------------------------------------ | ---------------------------------------------------------------- |
| `facility`                 | sizing, load_profiling               | Default gross MW, target PUE (single-phase, backward compatible) |
| `phases`                   | sizing, pue_analysis, load_profiling | Per-phase gross MW, PUE, zone rack counts                        |
| `zones`                    | sizing                               | Rack density definitions per zone type                           |
| `cooling`                  | pue_analysis                         | Hybrid mix percentages                                           |
| `cooling_technologies`     | pue_analysis                         | PUE ranges per technology                                        |
| `tropical_climate`         | pue_analysis                         | Design temp, humidity, ambient range                             |
| `power`                    | load_profiling                       | Idle power ratios                                                |
| `load_profiling.scenarios` | load_profiling                       | Per-scenario utilization and diurnal params                      |

### Phase Configuration

```yaml
phases:
  phase_1:
    name: "Initial Deployment"
    gross_mw: 10.0
    target_pue: 1.30
    zones:
      zone_a: { rack_count: 180 }
      zone_b: { rack_count: 60 }
      zone_c: { rack_count: 10 }
  phase_2:
    name: "Full Deployment"
    gross_mw: 15.0
    target_pue: 1.25
    zones:
      zone_a: { rack_count: 250 }
      zone_b: { rack_count: 80 }
      zone_c: { rack_count: 30 }
  phase_3:
    name: "Full Build-Out"
    gross_mw: 20.0
    target_pue: 1.20
    zones:
      zone_a: { rack_count: 330 }
      zone_b: { rack_count: 120 }
      zone_c: { rack_count: 40 }
```

## Data Flow

### Sizing Pipeline

```
parameters.yaml
    │
    ▼
sizing_calculator.calculate_it_load()
    │  Input:  gross_mw (15.0), pue (1.25)
    │  Output: it_mw (12.0), dcie (80.0%), overhead (0.25)
    │
    ▼
sizing_calculator.calculate_it_load_by_phase()
    │  Input:  phases from YAML
    │  Output: {phase_1: {it_mw: 7.69, ...}, phase_2: {...}, phase_3: {...}}
    │
    ▼
rack_allocation.allocate_racks()
    │  Input:  zones from topology.py (loaded from YAML)
    │  Output: {zone_a: {250 racks, 5.0 MW}, zone_b: {80 racks, 4.0 MW}, ...}
    │
    ▼
rack_allocation.allocate_racks_by_phase()
    │  Input:  phases from YAML
    │  Output: {phase_1: {zones: {...}, total: ...}, phase_2: {...}, phase_3: {...}}
```

### PUE Pipeline

```
parameters.yaml
    │
    ├──▶ pue_calculator.energy_breakdown(total_kw, it_kw)
    │       Returns: pue, dcie, overhead_ratio, breakdown
    │
    ├──▶ cooling_comparison.comparison_table()
    │       Returns: list of 4 technologies with PUE/DCiE ranges
    │
    ├──▶ tropical_benchmark.get_tropical_pue_target()
    │       Returns: weighted PUE, justification, design conditions
    │
    └──▶ tropical_benchmark.get_pue_sensitivity_by_phase()
            Returns: {phase_1: {pue, it_mw, chiller_pct}, ...}
```

### Load Profiling Pipeline

```
parameters.yaml
    │
    ▼
scenarios.load_scenarios()
    │  Returns: 3 Scenario dataclasses (cloud_heavy, ai_heavy, mixed)
    │
    ▼
profile_generator.generate_load_profiles(phase_key="phase_2")
    │  For each scenario:
    │    1. Create 8760-hour time axis
    │    2. Compute diurnal shape:  D(h) = exp(-(h-14)² / 72)
    │    3. Apply weekday boost:    1.0 (weekday) / 0.7 (weekend)
    │    4. Calculate utilization:  offpeak + range × diurnal × weekday
    │    5. Split into AI floor + cloud component
    │    6. Add ±3% Gaussian noise
    │    7. Clip to [0.9 × idle, 1.05 × peak]
    │    8. Multiply IT by PUE for facility load
    │
    │  Output: dict of 3 DataFrames (8760 rows × 7 columns)
    │
    ▼
profile_generator.generate_all_phase_profiles()
    │  Generates all 9 profiles (3 phases × 3 scenarios)
    │
    ▼
visualize.plot_all_with_phases()
    │  Generates: diurnal_profiles.png, annual_profiles.png,
    │             facility_vs_it_load.png, phase_comparison.png
```

### MVP Dashboard

```
Import from all 3 modules:
    ├── it_sizing: calculate_it_load(), allocate_racks(), calculate_it_load_by_phase(), allocate_racks_by_phase()
    ├── pue_analysis: energy_breakdown(), comparison_table(), get_tropical_pue_target(), get_pue_sensitivity_by_phase()
    └── load_profiling: generate_load_profiles(), generate_all_phase_profiles()

Produces 4 figures:
    ├── mvp_sizing_overview.png    (4-panel: zones, racks, energy breakdown, cooling)
    ├── mvp_load_profiles.png      (3×2 grid: diurnal + annual per scenario)
    ├── mvp_summary_table.png      (formatted stats table)
    └── mvp_phase_comparison.png   (4-panel: IT by phase, PUE sensitivity, racks, revenue)
```

## Load Profile Generation

The core algorithm in `profile_generator.py`:

### Diurnal Shape

A Gaussian centered at hour 14 (2 PM) with width σ=6 hours:

```
D(h) = exp( -(h - 14)² / (2 × 6²) )
```

This peaks at 1.0 at 2 PM, drops to ~0.13 at midnight and 6 AM.

### Scenario Parameters

| Parameter             | Cloud-Heavy | AI-Heavy | Mixed |
| --------------------- | ----------- | -------- | ----- |
| `peak_utilization`    | 0.95        | 0.98     | 0.92  |
| `offpeak_utilization` | 0.45        | 0.80     | 0.55  |
| `diurnal_amplitude`   | 0.50        | 0.10     | 0.30  |
| `ai_batch_pct`        | 0.15        | 0.70     | 0.40  |

- **`ai_batch_pct`**: Fraction of compute headroom reserved for sustained AI batch jobs. Higher values flatten the diurnal curve.
- **`diurnal_amplitude`**: How much the cloud component varies between day and night. AI-heavy workloads barely dip.

### Power Composition

```
IT_load(t) = [idle + ai_floor + cloud(t)] × noise
where:
    idle       = 35% × peak IT (always-on baseline)
    ai_floor   = ai_batch_pct × (peak - idle)
    cloud(t)   = (1 - ai_batch_pct) × (peak - idle) × utilization(t)
    noise      = 1 + N(0, 0.03)   # ±3% Gaussian
```

### Phase-Aware Generation

Load profiles scale with IT capacity per phase. The same diurnal and scenario shapes apply, but the absolute MW values differ:

| Phase                 | Cloud Avg (MW) | AI Avg (MW) | Mixed Avg (MW) |
| --------------------- | -------------- | ----------- | -------------- |
| Phase 1 (7.69 MW IT)  | 6.49           | 7.54        | 6.94           |
| Phase 2 (12.00 MW IT) | 10.13          | 11.76       | 10.83          |
| Phase 3 (16.67 MW IT) | 14.07          | 16.33       | 15.05          |

## Output Artifacts

| Command         | CSV Output                                 | Figure Output                      |
| --------------- | ------------------------------------------ | ---------------------------------- |
| `make sizing`   | — (stdout only)                            | —                                  |
| `make pue`      | — (stdout only)                            | —                                  |
| `make profiles` | `csv/load_profile_phase_1_cloud_heavy.csv` | `figures/diurnal_profiles.png`     |
|                 | `csv/load_profile_phase_1_ai_heavy.csv`    | `figures/annual_profiles.png`      |
|                 | `csv/load_profile_phase_1_mixed.csv`       | `figures/facility_vs_it_load.png`  |
|                 | `csv/load_profile_phase_2_cloud_heavy.csv` | `figures/phase_comparison.png`     |
|                 | `csv/load_profile_phase_2_ai_heavy.csv`    |                                    |
|                 | `csv/load_profile_phase_2_mixed.csv`       |                                    |
|                 | `csv/load_profile_phase_3_cloud_heavy.csv` |                                    |
|                 | `csv/load_profile_phase_3_ai_heavy.csv`    |                                    |
|                 | `csv/load_profile_phase_3_mixed.csv`       |                                    |
| `make mvp`      | —                                          | `figures/mvp_sizing_overview.png`  |
|                 | —                                          | `figures/mvp_load_profiles.png`    |
|                 | —                                          | `figures/mvp_summary_table.png`    |
|                 | —                                          | `figures/mvp_phase_comparison.png` |

### CSV Schema

Each load profile CSV has 8760 rows (one per hour) with columns:

| Column             | Type  | Description                         |
| ------------------ | ----- | ----------------------------------- |
| `hour`             | int   | 0–8759, hour index through the year |
| `hour_of_day`      | int   | 0–23, hour within the day           |
| `day_of_year`      | int   | 0–364, day within the year          |
| `it_load_kw`       | float | IT equipment power draw in kW       |
| `facility_load_kw` | float | Total facility power (IT × PUE)     |
| `utilization`      | float | Normalized utilization (0–1)        |
| `scenario`         | str   | Scenario identifier                 |

## Testing

31 tests across 3 files, run with `make test`:

| File                     | Tests | What's Covered                                                             |
| ------------------------ | ----- | -------------------------------------------------------------------------- |
| `test_sizing.py`         | 10    | IT load calc, DCiE, overhead, zone allocation, topology loading            |
| `test_pue.py`            | 12    | PUE/DCiE math, zero-division edge cases, cooling table, tropical benchmark |
| `test_load_profiling.py` | 9     | Scenario loading, 8760-hour generation, value ranges, CSV round-trip       |

### Adding Tests

Tests use `pytest`. Each module has its own test file. Follow the existing pattern:

```python
class TestNewFeature:
    def test_basic_case(self):
        result = my_function(input)
        assert result == expected

    def test_edge_case(self):
        result = my_function(edge_input)
        assert result == expected_value
```

## Extending the Project

### Adding a New Scenario

1. Add a section to `parameters.yaml` under `load_profiling.scenarios`:
   ```yaml
   new_scenario:
     description: "Description here"
     peak_utilization: 0.90
     offpeak_utilization: 0.50
     diurnal_amplitude: 0.25
     ai_batch_pct: 0.30
   ```
2. The `Scenario` dataclass in `scenarios.py` and `generate_load_profiles()` will pick it up automatically.

### Adding a New Phase

1. Add a section to `parameters.yaml` under `phases`:
   ```yaml
   phase_4:
     name: "Phase 4 Name"
     gross_mw: 25.0
     target_pue: 1.18
     zones:
       zone_a: { rack_count: 400 }
       zone_b: { rack_count: 150 }
       zone_c: { rack_count: 50 }
   ```
2. The `_load_phases()` function in `topology.py` will load it.
3. Call `calculate_it_load_by_phase()` with the new phase key.

### Adding a New Cooling Technology

1. Add a section to `parameters.yaml` under `cooling_technologies`:
   ```yaml
   new_tech:
     name: "Two-Phase Immersion"
     pue_range: [1.02, 1.08]
     water_usage: "Zero water loss"
   ```
2. The `comparison_table()` function will include it automatically.

### Adding a New Rack Zone

1. Add a `zone_d` section to `parameters.yaml` under `zones`
2. The `topology.py` loader and `rack_allocation.py` will pick it up
3. Update the colors list in `dashboard.py` if generating MVP figures

### Modifying the Diurnal Profile

Edit the `_diurnal_shape()` function in `profile_generator.py`. The current Gaussian peaks at hour 14 with σ=6. To shift the peak or change the width, adjust the `peak_hour` and `width` parameters.
