from .cooling_comparison import comparison_table
from .pue_calculator import calculate_dcie, calculate_pue, energy_breakdown
from .tropical_benchmark import get_pue_sensitivity_by_phase, get_tropical_pue_target


def main():
    sizing_mw = 15.0
    it_mw = 12.0
    total_kw = sizing_mw * 1000
    it_kw = it_mw * 1000

    breakdown = energy_breakdown(total_kw, it_kw)

    print("=" * 60)
    print("PUE BENCHMARK ANALYSIS — Phase 2 (Full Deployment)")
    print("=" * 60)
    print(f"\nGross Generation:  {breakdown['e_total_kw'] / 1000:.1f} MW")
    print(f"IT Load:           {breakdown['e_it_kw'] / 1000:.1f} MW")
    print(f"PUE:               {breakdown['pue']}")
    print(f"DCiE:              {breakdown['dcie_pct']}%")
    print(f"Overhead:          {breakdown['overhead_ratio']}")
    print(f"Overhead Power:    {breakdown['e_overhead_kw'] / 1000:.2f} MW")

    print("\n\nCOOLING TECHNOLOGY COMPARISON")
    print("-" * 60)
    for row in comparison_table():
        print(f"\n{row['technology']}")
        print(
            f"  PUE:     {row['pue_low']} – {row['pue_high']}  (mid: {row['pue_midpoint']})"
        )
        print(f"  DCiE:    {row['dcie_range']}")
        print(f"  Water:   {row['water_usage']}")

    print("\n\nTROPICAL BENCHMARK")
    print("-" * 60)
    tropical = get_tropical_pue_target()
    print(f"Design Temp:  {tropical['design_temp_c']}°C")
    print(f"Target PUE:   {tropical['target_pue']}")
    print(f"Weighted PUE: {tropical['calculated_weighted_pue']}")
    print(f"\n{tropical['justification']}")

    print("\n\nPUE SENSITIVITY BY PHASE")
    print("-" * 60)
    sensitivity = get_pue_sensitivity_by_phase()
    print(
        f"\n{'Phase':<20} {'Gross MW':<10} {'PUE':<8} {'IT MW':<10} {'Chiller %':<10}"
    )
    print("-" * 58)
    for pk in ["phase_1", "phase_2", "phase_3"]:
        s = sensitivity[pk]
        print(
            f"{s['name']:<20} {s['gross_mw']:<10} {s['target_pue']:<8} {s['it_mw']:<10} {s['chiller_utilization_pct']:<10.0f}"
        )
    print()
    for pk in ["phase_1", "phase_2", "phase_3"]:
        s = sensitivity[pk]
        print(f"  {s['name']}: {s['justification']}")


if __name__ == "__main__":
    main()
