from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"
)


@dataclass
class Zone:
    name: str
    workload: str
    rack_density_kw: float
    rack_count: int
    total_mw: float
    cooling: str

    @property
    def total_kw(self) -> float:
        return self.rack_density_kw * self.rack_count


def load_zones(config_path: Path = CONFIG_PATH) -> dict[str, Zone]:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    zones = {}
    for key, val in cfg["zones"].items():
        zones[key] = Zone(
            name=val["name"],
            workload=val["workload"],
            rack_density_kw=val["rack_density_kw"],
            rack_count=val["rack_count"],
            total_mw=val["total_mw"],
            cooling=val["cooling"],
        )
    return zones


def load_zones_by_phase(
    phase_key: str, config_path: Path = CONFIG_PATH
) -> dict[str, Zone]:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    phase = cfg["phases"][phase_key]
    zones = {}
    for zone_key, zone_cfg in phase["zones"].items():
        base = cfg["zones"][zone_key]
        zones[zone_key] = Zone(
            name=base["name"],
            workload=base["workload"],
            rack_density_kw=base["rack_density_kw"],
            rack_count=zone_cfg["rack_count"],
            total_mw=zone_cfg["total_mw"],
            cooling=base["cooling"],
        )
    return zones


ZONES = load_zones()
