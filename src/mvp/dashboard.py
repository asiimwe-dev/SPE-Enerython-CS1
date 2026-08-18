import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from pathlib import Path

from src.it_sizing.sizing_calculator import calculate_it_load
from src.it_sizing.rack_allocation import allocate_racks
from src.pue_analysis.pue_calculator import energy_breakdown
from src.pue_analysis.cooling_comparison import comparison_table
from src.pue_analysis.tropical_benchmark import get_tropical_pue_target
from src.load_profiling.profile_generator import generate_load_profiles


def run_dashboard(output_dir: Path | None = None) -> list[Path]:
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    sizing = calculate_it_load()
    racks = allocate_racks()
    breakdown = energy_breakdown(
        sizing["gross_generation_mw"] * 1000,
        sizing["it_load_mw"] * 1000,
    )
    cooling = comparison_table()
    tropical = get_tropical_pue_target()
    profiles = generate_load_profiles()

    paths = []

    # --- Figure 1: Sizing Overview ---
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, hspace=0.35, wspace=0.3)

    # 1a: Zone power distribution (bar chart)
    ax1 = fig.add_subplot(gs[0, 0])
    zone_names = [racks[k]["zone"] for k in racks if k != "total"]
    zone_mws = [racks[k]["zone_mw"] for k in racks if k != "total"]
    colors = ["#2196F3", "#FF9800", "#F44336"]
    bars = ax1.bar(zone_names, zone_mws, color=colors, edgecolor="white", linewidth=1.5)
    for bar, mw in zip(bars, zone_mws):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f"{mw} MW", ha="center", fontweight="bold", fontsize=10)
    ax1.set_ylabel("IT Power (MW)")
    ax1.set_title("Zone Power Distribution")
    ax1.set_ylim(0, max(zone_mws) * 1.3)
    ax1.grid(axis="y", alpha=0.3)

    # 1b: Rack count by zone (pie)
    ax2 = fig.add_subplot(gs[0, 1])
    zone_racks = [racks[k]["rack_count"] for k in racks if k != "total"]
    ax2.pie(zone_racks, labels=zone_names, autopct="%1.0f%%",
            colors=colors, startangle=90, textprops={"fontsize": 10})
    ax2.set_title("Rack Distribution")

    # 1c: Energy breakdown (waterfall-style)
    ax3 = fig.add_subplot(gs[1, 0])
    categories = ["IT Load", "Cooling/Overhead"]
    values = [breakdown["e_it_kw"]/1000, breakdown["e_overhead_kw"]/1000]
    bar_colors = ["#4CAF50", "#FF5722"]
    bars3 = ax3.bar(categories, values, color=bar_colors, edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars3, values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f"{val:.1f} MW", ha="center", fontweight="bold", fontsize=10)
    ax3.set_ylabel("Power (MW)")
    ax3.set_title(f"Energy Breakdown (PUE = {breakdown['pue']})")
    ax3.set_ylim(0, max(values) * 1.3)
    ax3.grid(axis="y", alpha=0.3)

    # 1d: Cooling technology PUE comparison
    ax4 = fig.add_subplot(gs[1, 1])
    tech_names = [c["technology"].replace(" (D2C) Liquid", "\n(D2C)").replace(" + Evaporative Towers", "\n+ Evap.")
                  for c in cooling]
    pue_mids = [c["pue_midpoint"] for c in cooling]
    pue_lows = [c["pue_low"] for c in cooling]
    pue_highs = [c["pue_high"] for c in cooling]
    yerr_low = [m - l for m, l in zip(pue_mids, pue_lows)]
    yerr_high = [h - m for m, h in zip(pue_mids, pue_highs)]

    tech_colors = ["#9E9E9E", "#607D8B", "#2196F3", "#00BCD4"]
    ax4.barh(tech_names, pue_mids, xerr=[yerr_low, yerr_high],
             color=tech_colors, edgecolor="white", linewidth=1.5, capsize=5)
    ax4.axvline(x=tropical["target_pue"], color="#F44336", linestyle="--",
                linewidth=2, label=f"Target: {tropical['target_pue']}")
    ax4.set_xlabel("PUE")
    ax4.set_title("Cooling Tech PUE Comparison")
    ax4.legend()
    ax4.grid(axis="x", alpha=0.3)

    fig.suptitle("SPE Energython 2026 — IT Architecture & Load Profiling MVP",
                 fontsize=16, fontweight="bold", y=1.01)
    path1 = output_dir / "mvp_sizing_overview.png"
    fig.savefig(path1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(path1)

    # --- Figure 2: Load Profile Dashboard ---
    fig2, axes2 = plt.subplots(3, 2, figsize=(16, 12))
    colors_map = {"cloud_heavy": "#2196F3", "ai_heavy": "#FF5722", "mixed": "#4CAF50"}

    for i, (key, df) in enumerate(profiles.items()):
        color = colors_map[key]

        # Left: 24h diurnal
        avg_by_hour = df.groupby("hour_of_day")["it_load_kw"].mean() / 1000
        std_by_hour = df.groupby("hour_of_day")["it_load_kw"].std() / 1000
        ax_l = axes2[i, 0]
        ax_l.fill_between(avg_by_hour.index, avg_by_hour - std_by_hour,
                          avg_by_hour + std_by_hour, alpha=0.2, color=color)
        ax_l.plot(avg_by_hour.index, avg_by_hour.values, color=color, linewidth=2)
        ax_l.set_ylabel("IT Load (MW)")
        ax_l.set_title(f"{key.replace('_', ' ').title()} — Diurnal")
        ax_l.set_xlabel("Hour of Day")
        ax_l.set_xlim(0, 23)
        ax_l.grid(True, alpha=0.3)

        # Right: annual rolling
        ax_r = axes2[i, 1]
        rolling = df["it_load_kw"].rolling(24, center=True).mean() / 1000
        ax_r.plot(df["hour"], rolling.values, color=color, linewidth=1)
        ax_r.set_ylabel("IT Load (MW)")
        ax_r.set_title(f"{key.replace('_', ' ').title()} — Annual (24h avg)")
        ax_r.set_xlabel("Hour of Year")
        ax_r.grid(True, alpha=0.3)

    fig2.suptitle("Load Profiles — Three Scenarios", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path2 = output_dir / "mvp_load_profiles.png"
    fig2.savefig(path2, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    paths.append(path2)

    # --- Figure 3: Summary Stats Table ---
    fig3, ax3t = plt.subplots(figsize=(12, 4))
    ax3t.axis("off")

    table_data = [
        ["Metric", "Value"],
        ["Gross Generation Cap", f"{sizing['gross_generation_mw']} MW"],
        ["Target PUE", f"{sizing['target_pue']}"],
        ["Max IT Load", f"{sizing['it_load_mw']} MW"],
        ["DCiE", f"{sizing['dcie_pct']}%"],
        ["Total Racks", f"{racks['total']['rack_count']}"],
        ["Total Zone IT", f"{racks['total']['zone_mw']} MW"],
        ["Design Temp", f"{tropical['design_temp_c']}°C"],
    ]

    table = ax3t.table(cellText=table_data, loc="center", cellLoc="center",
                       colWidths=[0.4, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.8)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#37474F")
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#ECEFF1")
        cell.set_edgecolor("#B0BEC5")

    ax3t.set_title("IT Sizing Summary — 15 MW Baseline Case",
                   fontsize=13, fontweight="bold", pad=20)
    path3 = output_dir / "mvp_summary_table.png"
    fig3.savefig(path3, dpi=150, bbox_inches="tight")
    plt.close(fig3)
    paths.append(path3)

    return paths


def main():
    paths = run_dashboard()
    print("MVP DASHBOARD COMPLETE")
    print("-" * 60)
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
