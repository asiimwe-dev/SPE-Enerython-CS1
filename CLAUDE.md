# CLAUDE.md

## What this is
SPE AMTS Energython 2026 — techno-economic model for a 10–20 MW natural gas-powered
data center in tropical Africa. This repo covers the **Data Center Architecture &
Load Profiling** role (CS #1) only.

## Team
5 members: Petroleum Eng, Mechanical Eng, Electrical Eng, 2 CS students.
This repo is **CS #1's scope**. CS #2 (financial modeling) lives elsewhere.

## Your 3 deliverables
1. **Load Profiles** — 8760-hour synthetic demand curves (Cloud-heavy, AI-heavy, Mixed)
2. **PUE Benchmark Memo** — Target PUE for tropical climate with cooling tech justification
3. **IT Sizing Spec** — MW capacity, rack counts, density zones, compute vs storage

## Key domain constraints (get these right)
- IT capacity: 12.0 MW net within 15.0 MW gross generation cap
- Target PUE: 1.25 (tropical, hybrid liquid cooling) — NOT 1.15 (temperate)
- Rack zones: 250 racks @ 20 kW (cloud), 80 @ 50 kW (HPC), 30 @ 100 kW (AI immersion)
- Cooling: hybrid — air + direct-to-chip + single-phase immersion
- GPU idle power: 30–40% of peak (not zero)
- Take-or-pay fuel alignment is a software scheduling concern, not just commercial

## Tech stack
Python 3.10+, pandas, numpy, matplotlib. No notebooks — reusable scripts only.

## Running the project
    make install        # pip install -r requirements.txt
    make profiles       # Generate load curve CSVs + plots → data/output/
    make pue            # Generate PUE analysis + comparison tables → data/output/
    make sizing         # Generate IT sizing spec → data/output/
    make mvp            # Run full visual MVP dashboard
    make test           # Run tests
    make all            # Everything above in order

## File conventions
- src/ modules are importable; each has __init__.py
- data/config/ holds tunable parameters (target MW, PUE assumptions, zone definitions)
- docs/refined/ contains polished markdown deliverables for team review
- docs/references/ has the original competition briefs — do not edit
- All figures saved as PNG to data/output/figures/
- All data exported as CSV to data/output/csv/

## Domain vocabulary
PUE, DCiE, CHP, BESS, VPPA, PID control, VFD, Modbus/SNMP/BACnet,
hypertable, diurnal load curve, take-or-pay, Peak-to-Average Ratio (PAR).
See docs/references/Data-Center-Architecture-and-Load-Profiling.md §2 for full definitions.

## When editing these docs
- docs/refined/ deliverables use academic/technical tone, LaTeX math ($...$), tables
- Source references belong in footers, not inline
- PUE formulas must use the notation from the competition briefs (E_Total, E_IT)
- Do not modify files in docs/references/
