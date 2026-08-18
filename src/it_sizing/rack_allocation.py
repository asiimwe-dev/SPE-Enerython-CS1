from .topology import ZONES, Zone


def allocate_racks(zones: dict[str, Zone] | None = None) -> dict:
    if zones is None:
        zones = ZONES
    allocation = {}
    total_racks = 0
    total_mw = 0.0
    for key, z in zones.items():
        total_racks += z.rack_count
        total_mw += z.total_mw
        allocation[key] = {
            "zone": z.name,
            "workload": z.workload,
            "rack_count": z.rack_count,
            "density_kw": z.rack_density_kw,
            "zone_mw": z.total_mw,
            "cooling": z.cooling,
        }
    allocation["total"] = {
        "rack_count": total_racks,
        "zone_mw": round(total_mw, 2),
    }
    return allocation


if __name__ == "__main__":
    alloc = allocate_racks()
    for k, v in alloc.items():
        if k == "total":
            print(f"\nTotal: {v['rack_count']} racks, {v['zone_mw']} MW")
        else:
            print(f"{v['zone']}: {v['rack_count']} racks @ {v['density_kw']} kW = {v['zone_mw']} MW")
