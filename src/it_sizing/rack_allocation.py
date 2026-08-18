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


def allocate_racks_by_phase(config_path=None) -> dict:
    if config_path is None:
        from .topology import CONFIG_PATH
        config_path = CONFIG_PATH
    import yaml
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    results = {}
    for phase_key in ["phase_1", "phase_2", "phase_3"]:
        phase = cfg["phases"][phase_key]
        zones = cfg["zones"]
        alloc = {}
        total_racks = 0
        total_mw = 0.0
        for zone_key, zone_cfg in phase["zones"].items():
            total_racks += zone_cfg["rack_count"]
            total_mw += zone_cfg["total_mw"]
            alloc[zone_key] = {
                "zone": zones[zone_key]["name"],
                "rack_count": zone_cfg["rack_count"],
                "density_kw": zones[zone_key]["rack_density_kw"],
                "zone_mw": zone_cfg["total_mw"],
            }
        alloc["total"] = {"rack_count": total_racks, "zone_mw": round(total_mw, 2)}
        results[phase_key] = {
            "name": phase["name"],
            "gross_mw": phase["gross_mw"],
            "target_pue": phase["target_pue"],
            "it_mw": round(total_mw, 2),
            "zones": alloc,
        }
    return results


if __name__ == "__main__":
    alloc = allocate_racks()
    for k, v in alloc.items():
        if k == "total":
            print(f"\nTotal: {v['rack_count']} racks, {v['zone_mw']} MW")
        else:
            print(f"{v['zone']}: {v['rack_count']} racks @ {v['density_kw']} kW = {v['zone_mw']} MW")
