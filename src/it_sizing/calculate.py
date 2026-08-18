from .rack_allocation import allocate_racks, allocate_racks_by_phase
from .sizing_calculator import calculate_it_load, calculate_it_load_by_phase


def main():
    sizing = calculate_it_load()
    racks = allocate_racks()

    print("=" * 60)
    print("IT SIZING SPECIFICATION — Phase 2 (Full Deployment)")
    print("=" * 60)
    print(f"\nGross Generation Cap:  {sizing['gross_generation_mw']} MW")
    print(f"Target PUE:           {sizing['target_pue']}")
    print(f"Max IT Compute Load:   {sizing['it_load_mw']} MW")
    print(f"DCiE:                  {sizing['dcie_pct']}%")
    print(f"Overhead Ratio:        {sizing['overhead_ratio']}")
    print()

    print("RACK ALLOCATION BY ZONE")
    print("-" * 60)
    for k, v in racks.items():
        if k == "total":
            print(
                f"\n{'TOTAL':<30} {v['rack_count']:<10} racks   {v['zone_mw']:<10} MW"
            )
        else:
            print(
                f"{v['zone']:<30} {v['rack_count']:<10} racks   {v['zone_mw']:<10} MW  ({v['cooling']})"
            )

    # Phase comparison
    print("\n\n")
    print("=" * 60)
    print("3-PHASE DEPLOYMENT COMPARISON")
    print("=" * 60)
    phase_sizing = calculate_it_load_by_phase()
    phase_racks = allocate_racks_by_phase()

    print(f"\n{'Phase':<20} {'Gross MW':<10} {'PUE':<8} {'IT MW':<10} {'Racks':<8}")
    print("-" * 56)
    for pk in ["phase_1", "phase_2", "phase_3"]:
        s = phase_sizing[pk]
        r = phase_racks[pk]
        print(
            f"{s['name']:<20} {s['gross_mw']:<10} {s['target_pue']:<8} {s['it_load_mw']:<10} {r['zones']['total']['rack_count']:<8}"
        )


if __name__ == "__main__":
    main()
