import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"


def get_tropical_pue_target(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    tropical = cfg["tropical_climate"]
    facility = cfg["facility"]
    cooling_mix = cfg["cooling"]["hybrid_mix"]

    # Weighted PUE estimate from hybrid cooling mix
    cooling_techs = cfg["cooling_technologies"]
    air_pue = sum(cooling_techs["legacy_dx"]["pue_range"]) / 2
    d2c_pue = sum(cooling_techs["direct_to_chip"]["pue_range"]) / 2
    imm_pue = sum(cooling_techs["immersion"]["pue_range"]) / 2

    weighted_pue = (
        cooling_mix["air_cooled_pct"] * air_pue
        + cooling_mix["direct_to_chip_pct"] * d2c_pue
        + cooling_mix["immersion_pct"] * imm_pue
    )

    return {
        "design_temp_c": tropical["design_temp_c"],
        "humidity_pct": tropical["humidity_pct"],
        "ambient_range_c": tropical["ambient_range_c"],
        "hybrid_mix": cooling_mix,
        "calculated_weighted_pue": round(weighted_pue, 3),
        "target_pue": facility["target_pue"],
        "justification": (
            f"Hybrid cooling ({cooling_mix['air_cooled_pct']*100:.0f}% air, "
            f"{cooling_mix['direct_to_chip_pct']*100:.0f}% D2C, "
            f"{cooling_mix['immersion_pct']*100:.0f}% immersion) at "
            f"{tropical['design_temp_c']}°C design temperature yields "
            f"weighted PUE of {weighted_pue:.3f}. Target set to "
            f"{facility['target_pue']} accounting for tropical overhead."
        ),
    }


if __name__ == "__main__":
    result = get_tropical_pue_target()
    print("TROPICAL PUE BENCHMARK")
    print("-" * 60)
    print(f"Design Temperature:  {result['design_temp_c']}°C")
    print(f"Target PUE:          {result['target_pue']}")
    print(f"Weighted PUE:        {result['calculated_weighted_pue']}")
    print(f"\nJustification: {result['justification']}")
