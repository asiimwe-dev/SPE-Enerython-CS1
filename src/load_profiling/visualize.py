import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from pathlib import Path


def plot_diurnal_curves(profiles: dict[str, pd.DataFrame], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(len(profiles), 1, figsize=(14, 5 * len(profiles)), sharex=False)
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
            alpha=0.2, color=color,
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
        # 24-hour rolling average for readability
        rolling = df["it_load_kw"].rolling(24, center=True).mean() / 1000
        ax.plot(df["hour"], rolling.values, label=key.replace("_", " ").title(),
                color=colors.get(key, "#333"), linewidth=1.2)

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

        ax.fill_between(df["hour"], rolling_it, rolling_fac, alpha=0.3, color="#FF9800",
                        label="Cooling/Overhead")
        ax.plot(df["hour"], rolling_fac, color="#F44336", linewidth=1.5, label="Facility Total")
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


def plot_all(profiles: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    paths = []
    paths.append(plot_diurnal_curves(profiles, output_dir))
    paths.append(plot_annual_curves(profiles, output_dir))
    paths.append(plot_facility_vs_it(profiles, output_dir))
    return paths
