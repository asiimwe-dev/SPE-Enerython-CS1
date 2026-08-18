from .sizing_calculator import calculate_it_load
from .rack_allocation import allocate_racks
import json


def main():
    sizing = calculate_it_load()
    racks = allocate_racks()

    print("=" * 60)
    print("IT SIZING SPECIFICATION — 15 MW Baseline Case")
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
            print(f"\n{'TOTAL':<30} {v['rack_count']:<10} racks   {v['zone_mw']:<10} MW")
        else:
            print(f"{v['zone']:<30} {v['rack_count']:<10} racks   {v['zone_mw']:<10} MW  ({v['cooling']})")


if __name__ == "__main__":
    main()
