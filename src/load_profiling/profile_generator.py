import numpy as np
import pandas as pd
import yaml
from pathlib import Path

from .scenarios import Scenario, SCENARIOS

CONFIG_PATH = Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"


def _diurnal_shape(hour: float, peak_hour: float = 14.0, width: float = 6.0) -> float:
    """Gaussian-ish diurnal profile peaking at peak_hour."""
    return np.exp(-0.5 * ((hour - peak_hour) / width) ** 2)


def generate_load_profiles(
    it_mw: float | None = None,
    pue: float | None = None,
    scenarios: dict[str, Scenario] | None = None,
    config_path: Path = CONFIG_PATH,
) -> dict[str, pd.DataFrame]:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    if it_mw is None:
        gross = cfg["facility"]["gross_generation_mw"]
        pue_val = cfg["facility"]["target_pue"]
        it_mw = gross / pue_val

    if scenarios is None:
        scenarios = SCENARIOS

    hours_per_year = cfg["load_profiling"]["hours_per_year"]
    idle_ratio = cfg["power"]["idle_power_ratio"]

    it_kw = it_mw * 1000
    base_idle = it_kw * idle_ratio
    compute_headroom = it_kw - base_idle

    results = {}
    rng = np.random.default_rng(42)

    for key, scenario in scenarios.items():
        hours = np.arange(hours_per_year)
        hour_of_day = hours % 24
        day_of_year = hours // 24

        # Diurnal component
        diurnal = _diurnal_shape(hour_of_day, peak_hour=14.0, width=6.0)

        # Business day boost (weekday effect)
        weekday_mask = (day_of_year % 7) < 5
        business_boost = np.where(weekday_mask, 1.0, 0.7)

        # Compute utilization band
        util_range = scenario.peak_utilization - scenario.offpeak_utilization
        utilization = (
            scenario.offpeak_utilization
            + util_range * diurnal * business_boost
        )

        # AI batch floor — sustained high load that reduces diurnal swing
        ai_floor = scenario.ai_batch_pct * compute_headroom
        cloud_component = (1.0 - scenario.ai_batch_pct) * compute_headroom * utilization

        # Stochastic noise (±3%)
        noise = 1.0 + rng.normal(0, 0.03, hours_per_year)

        it_load_kw = (base_idle + ai_floor + cloud_component) * noise
        it_load_kw = np.clip(it_load_kw, base_idle * 0.9, it_kw * 1.05)

        facility_kw = it_load_kw * cfg["facility"]["target_pue"]

        df = pd.DataFrame({
            "hour": hours,
            "hour_of_day": hour_of_day.astype(int),
            "day_of_year": day_of_year.astype(int),
            "it_load_kw": np.round(it_load_kw, 1),
            "facility_load_kw": np.round(facility_kw, 1),
            "utilization": np.round(utilization, 4),
            "scenario": key,
        })

        results[key] = df

    return results


def save_profiles(profiles: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for key, df in profiles.items():
        path = output_dir / f"load_profile_{key}.csv"
        df.to_csv(path, index=False)
        paths.append(path)
    return paths


if __name__ == "__main__":
    profiles = generate_load_profiles()
    out = Path(__file__).resolve().parents[2] / "data" / "output" / "csv"
    paths = save_profiles(profiles, out)
    for p in paths:
        print(f"Saved: {p}")
