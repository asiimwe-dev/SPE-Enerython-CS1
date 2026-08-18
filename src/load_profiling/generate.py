from pathlib import Path

import yaml

from .profile_generator import (
    generate_all_phase_profiles,
    generate_load_profiles,
    save_profiles,
)
from .visualize import plot_all, plot_all_with_phases


def main():
    config_path = (
        Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"
    )
    csv_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "csv"
    fig_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "figures"

    # Generate all 9 profiles (3 phases x 3 scenarios)
    all_profiles = generate_all_phase_profiles(config_path=config_path)
    csv_paths = save_profiles(all_profiles, csv_dir)

    # Load phase sizing for plots
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    phase_sizing = {}
    for pk in ["phase_1", "phase_2", "phase_3"]:
        phase = cfg["phases"][pk]
        phase_sizing[pk] = {
            "it_load_mw": round(phase["gross_mw"] / phase["target_pue"], 2),
            "target_pue": phase["target_pue"],
        }

    fig_paths = plot_all_with_phases(all_profiles, phase_sizing, fig_dir)

    print("LOAD PROFILE GENERATION COMPLETE (3 PHASES x 3 SCENARIOS)")
    print("=" * 60)
    print(f"\nGenerated {len(csv_paths)} CSV files:")
    for p in csv_paths:
        print(f"  {p.name}")
    print(f"\nGenerated {len(fig_paths)} figures:")
    for p in fig_paths:
        print(f"  {p.name}")

    # Summary stats per phase
    print("\n\nPHASE SUMMARY")
    print("=" * 60)
    for phase_key in ["phase_1", "phase_2", "phase_3"]:
        phase = cfg["phases"][phase_key]
        it_mw = phase["gross_mw"] / phase["target_pue"]
        print(
            f"\n{phase['name']} ({phase['gross_mw']} MW gross / PUE {phase['target_pue']}):"
        )
        print(f"  IT Capacity: {it_mw:.2f} MW")
        for scenario_key in ["cloud_heavy", "ai_heavy", "mixed"]:
            df = all_profiles[f"{phase_key}_{scenario_key}"]
            avg = df["it_load_kw"].mean() / 1000
            peak = df["it_load_kw"].max() / 1000
            mn = df["it_load_kw"].min() / 1000
            par = peak / avg if avg > 0 else 0
            print(
                f"  {scenario_key:<15} Avg: {avg:.2f} MW  Peak: {peak:.2f}  Min: {mn:.2f}  PAR: {par:.2f}"
            )


if __name__ == "__main__":
    main()
