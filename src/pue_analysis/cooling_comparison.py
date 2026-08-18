import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"


def load_cooling_technologies(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    return cfg.get("cooling_technologies", {})


COOLING_TECHNOLOGIES = load_cooling_technologies()


def comparison_table() -> list[dict]:
    rows = []
    for key, tech in COOLING_TECHNOLOGIES.items():
        pue_low, pue_high = tech["pue_range"]
        mid_pue = (pue_low + pue_high) / 2.0
        dcie_low = round((1.0 / pue_high) * 100.0, 1)
        dcie_high = round((1.0 / pue_low) * 100.0, 1)
        overhead_low = round(pue_low - 1.0, 2)
        overhead_high = round(pue_high - 1.0, 2)
        rows.append({
            "technology": tech["name"],
            "pue_low": pue_low,
            "pue_high": pue_high,
            "pue_midpoint": round(mid_pue, 3),
            "dcie_range": f"{dcie_low}% – {dcie_high}%",
            "overhead_range": f"{overhead_low} – {overhead_high}",
            "water_usage": tech["water_usage"],
        })
    return rows


if __name__ == "__main__":
    print("COOLING TECHNOLOGY COMPARISON")
    print("-" * 80)
    for row in comparison_table():
        print(f"\n{row['technology']}")
        print(f"  PUE:     {row['pue_low']} – {row['pue_high']}  (midpoint: {row['pue_midpoint']})")
        print(f"  DCiE:    {row['dcie_range']}")
        print(f"  Water:   {row['water_usage']}")
