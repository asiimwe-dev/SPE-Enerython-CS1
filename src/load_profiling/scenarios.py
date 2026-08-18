from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"
)


@dataclass
class Scenario:
    name: str
    description: str
    peak_utilization: float
    offpeak_utilization: float
    diurnal_amplitude: float
    ai_batch_pct: float


def load_scenarios(config_path: Path = CONFIG_PATH) -> dict[str, Scenario]:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    scenarios = {}
    for key, val in cfg["load_profiling"]["scenarios"].items():
        scenarios[key] = Scenario(
            name=key,
            description=val["description"],
            peak_utilization=val["peak_utilization"],
            offpeak_utilization=val["offpeak_utilization"],
            diurnal_amplitude=val["diurnal_amplitude"],
            ai_batch_pct=val["ai_batch_pct"],
        )
    return scenarios


SCENARIOS = load_scenarios()
