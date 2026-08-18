from pathlib import Path
from .profile_generator import generate_load_profiles, save_profiles
from .visualize import plot_all


def main():
    profiles = generate_load_profiles()

    csv_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "csv"
    fig_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "figures"

    csv_paths = save_profiles(profiles, csv_dir)
    fig_paths = plot_all(profiles, fig_dir)

    print("LOAD PROFILE GENERATION COMPLETE")
    print("-" * 60)
    print("\nCSV files:")
    for p in csv_paths:
        print(f"  {p}")
    print("\nFigures:")
    for p in fig_paths:
        print(f"  {p}")

    # Summary stats
    print("\nSCENARIO SUMMARY")
    print("-" * 60)
    for key, df in profiles.items():
        it_mw_avg = df["it_load_kw"].mean() / 1000
        it_mw_peak = df["it_load_kw"].max() / 1000
        it_mw_min = df["it_load_kw"].min() / 1000
        par = it_mw_peak / it_mw_avg if it_mw_avg > 0 else 0
        print(f"\n{key}:")
        print(f"  Avg IT Load:   {it_mw_avg:.2f} MW")
        print(f"  Peak IT Load:  {it_mw_peak:.2f} MW")
        print(f"  Min IT Load:   {it_mw_min:.2f} MW")
        print(f"  Peak-to-Avg:   {par:.2f}")


if __name__ == "__main__":
    main()
