import matplotlib

matplotlib.use("Agg")
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_diurnal_curves(profiles: dict[str, pd.DataFrame], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        len(profiles), 1, figsize=(14, 5 * len(profiles)), sharex=False
    )
    if len(profiles) == 1:
        axes = [axes]

    colors = {"cloud_heavy": "#2196F3", "ai_heavy": "#FF5722", "mixed": "#4CAF50"}

    for ax, (key, df) in zip(axes, profiles.items()):
        avg_by_hour = df.groupby("hour_of_day")["it_load_kw"].mean() / 1000
        std_by_hour = df.groupby("hour_of_day")["it_load_kw"].std() / 1000

        color = colors.get(key, "#333333")
        ax.fill_between(
            avg_by_hour.index,
            avg_by_hour - std_by_hour,
            avg_by_hour + std_by_hour,
            alpha=0.2,
            color=color,
        )
        ax.plot(avg_by_hour.index, avg_by_hour.values, color=color, linewidth=2)
        ax.set_ylabel("IT Load (MW)")
        ax.set_title(f"Diurnal Profile — {key.replace('_', ' ').title()}")
        ax.set_xlabel("Hour of Day")
        ax.set_xlim(0, 23)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = output_dir / "diurnal_profiles.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_annual_curves(profiles: dict[str, pd.DataFrame], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 6))
    colors = {"cloud_heavy": "#2196F3", "ai_heavy": "#FF5722", "mixed": "#4CAF50"}

    for key, df in profiles.items():
        rolling = df["it_load_kw"].rolling(24, center=True).mean() / 1000
        ax.plot(
            df["hour"],
            rolling.values,
            label=key.replace("_", " ").title(),
            color=colors.get(key, "#333"),
            linewidth=1.2,
        )

    ax.set_xlabel("Hour of Year")
    ax.set_ylabel("IT Load (MW) — 24h Rolling Avg")
    ax.set_title("Annual Load Profiles — All Scenarios")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = output_dir / "annual_profiles.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_facility_vs_it(profiles: dict[str, pd.DataFrame], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(len(profiles), 1, figsize=(14, 5 * len(profiles)))
    if len(profiles) == 1:
        axes = [axes]

    for ax, (key, df) in zip(axes, profiles.items()):
        rolling_it = df["it_load_kw"].rolling(24, center=True).mean() / 1000
        rolling_fac = df["facility_load_kw"].rolling(24, center=True).mean() / 1000

        ax.fill_between(
            df["hour"],
            rolling_it,
            rolling_fac,
            alpha=0.3,
            color="#FF9800",
            label="Cooling/Overhead",
        )
        ax.plot(
            df["hour"],
            rolling_fac,
            color="#F44336",
            linewidth=1.5,
            label="Facility Total",
        )
        ax.plot(df["hour"], rolling_it, color="#2196F3", linewidth=1.5, label="IT Load")

        ax.set_ylabel("Power (MW)")
        ax.set_title(f"Facility vs IT Load — {key.replace('_', ' ').title()}")
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = output_dir / "facility_vs_it_load.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_phase_comparison(
    phase_profiles: dict[str, pd.DataFrame],
    phase_sizing: dict,
    output_dir: Path,
) -> Path:
    """Plot 3-phase diurnal comparison (mixed scenario for each phase)."""
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    phase_colors = {"phase_1": "#FF9800", "phase_2": "#2196F3", "phase_3": "#4CAF50"}
    phase_labels = {
        "phase_1": "Phase 1 (10 MW)",
        "phase_2": "Phase 2 (15 MW)",
        "phase_3": "Phase 3 (20 MW)",
    }

    for ax, phase_key in zip(axes, ["phase_1", "phase_2", "phase_3"]):
        df = phase_profiles.get(f"{phase_key}_mixed")
        if df is None:
            continue
        avg_by_hour = df.groupby("hour_of_day")["it_load_kw"].mean() / 1000
        std_by_hour = df.groupby("hour_of_day")["it_load_kw"].std() / 1000

        color = phase_colors[phase_key]
        ax.fill_between(
            avg_by_hour.index,
            avg_by_hour - std_by_hour,
            avg_by_hour + std_by_hour,
            alpha=0.2,
            color=color,
        )
        ax.plot(avg_by_hour.index, avg_by_hour.values, color=color, linewidth=2)
        ax.set_ylabel("IT Load (MW)")
        ax.set_xlabel("Hour of Day")
        s = phase_sizing[phase_key]
        ax.set_title(
            f"{phase_labels[phase_key]}\n{s['it_load_mw']} MW IT (PUE {s['target_pue']})"
        )
        ax.set_xlim(0, 23)
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        "3-Phase Deployment — Diurnal Comparison (Mixed Scenario)",
        fontsize=14,
        fontweight="bold",
    )
    plt.tight_layout()
    path = output_dir / "phase_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_all(profiles: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    paths = []
    paths.append(plot_diurnal_curves(profiles, output_dir))
    paths.append(plot_annual_curves(profiles, output_dir))
    paths.append(plot_facility_vs_it(profiles, output_dir))
    return paths


def plot_all_with_phases(
    phase_profiles: dict[str, pd.DataFrame],
    phase_sizing: dict,
    output_dir: Path,
) -> list[Path]:
    """Generate all standard plots plus phase comparison."""
    paths = plot_all(phase_profiles, output_dir)
    paths.append(plot_phase_comparison(phase_profiles, phase_sizing, output_dir))
    return paths
