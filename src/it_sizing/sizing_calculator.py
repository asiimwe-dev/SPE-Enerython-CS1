import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"


def calculate_it_load(
    gross_mw: float | None = None,
    pue: float | None = None,
    config_path: Path = CONFIG_PATH,
) -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    if gross_mw is None:
        gross_mw = cfg["facility"]["gross_generation_mw"]
    if pue is None:
        pue = cfg["facility"]["target_pue"]

    it_mw = gross_mw / pue
    overhead_ratio = pue - 1.0
    dcie = (1.0 / pue) * 100.0

    return {
        "gross_generation_mw": gross_mw,
        "target_pue": pue,
        "it_load_mw": round(it_mw, 2),
        "overhead_ratio": round(overhead_ratio, 4),
        "dcie_pct": round(dcie, 2),
    }


def calculate_zone_power(zones: dict, it_mw: float) -> dict:
    total_zone_mw = sum(z.total_mw for z in zones.values())
    scaling = it_mw / total_zone_mw if total_zone_mw > 0 else 1.0
    result = {}
    for key, z in zones.items():
        result[key] = {
            "name": z.name,
            "nominal_mw": z.total_mw,
            "scaled_mw": round(z.total_mw * scaling, 2),
            "rack_count": z.rack_count,
            "density_kw": z.rack_density_kw,
        }
    return result


if __name__ == "__main__":
    sizing = calculate_it_load()
    print(f"IT Load: {sizing['it_load_mw']} MW")
    print(f"PUE: {sizing['target_pue']}")
    print(f"DCiE: {sizing['dcie_pct']}%")
    print(f"Overhead Ratio: {sizing['overhead_ratio']}")
