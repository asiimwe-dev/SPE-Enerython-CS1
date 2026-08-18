import matplotlib

matplotlib.use("Agg")
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from src.it_sizing.rack_allocation import allocate_racks, allocate_racks_by_phase
from src.it_sizing.sizing_calculator import (
    calculate_it_load,
    calculate_it_load_by_phase,
)
from src.load_profiling.profile_generator import (
    generate_all_phase_profiles,
    generate_load_profiles,
)
from src.pue_analysis.cooling_comparison import comparison_table
from src.pue_analysis.pue_calculator import energy_breakdown
from src.pue_analysis.tropical_benchmark import (
    get_pue_sensitivity_by_phase,
    get_tropical_pue_target,
)


def run_dashboard(output_dir: Path | None = None) -> list[Path]:
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[2] / "data" / "output" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = (
        Path(__file__).resolve().parents[2] / "data" / "config" / "parameters.yaml"
    )

    sizing = calculate_it_load()
    racks = allocate_racks()
    breakdown = energy_breakdown(
        sizing["gross_generation_mw"] * 1000,
        sizing["it_load_mw"] * 1000,
    )
    cooling = comparison_table()
    tropical = get_tropical_pue_target()
    profiles = generate_load_profiles()

    phase_sizing = calculate_it_load_by_phase()
    phase_racks = allocate_racks_by_phase()
    pue_sensitivity = get_pue_sensitivity_by_phase()

    paths = []

    # --- Figure 1: Sizing Overview (Phase 2) ---
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, hspace=0.35, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    zone_names = [racks[k]["zone"] for k in racks if k != "total"]
    zone_mws = [racks[k]["zone_mw"] for k in racks if k != "total"]
    colors = ["#2196F3", "#FF9800", "#F44336"]
    bars = ax1.bar(zone_names, zone_mws, color=colors, edgecolor="white", linewidth=1.5)
    for bar, mw in zip(bars, zone_mws):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{mw} MW",
            ha="center",
            fontweight="bold",
            fontsize=10,
        )
    ax1.set_ylabel("IT Power (MW)")
    ax1.set_title("Zone Power Distribution (Phase 2)")
    ax1.set_ylim(0, max(zone_mws) * 1.3)
    ax1.grid(axis="y", alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    zone_racks = [racks[k]["rack_count"] for k in racks if k != "total"]
    ax2.pie(
        zone_racks,
        labels=zone_names,
        autopct="%1.0f%%",
        colors=colors,
        startangle=90,
        textprops={"fontsize": 10},
    )
    ax2.set_title("Rack Distribution (Phase 2)")

    ax3 = fig.add_subplot(gs[1, 0])
    categories = ["IT Load", "Cooling/Overhead"]
    values = [breakdown["e_it_kw"] / 1000, breakdown["e_overhead_kw"] / 1000]
    bar_colors = ["#4CAF50", "#FF5722"]
    bars3 = ax3.bar(
        categories, values, color=bar_colors, edgecolor="white", linewidth=1.5
    )
    for bar, val in zip(bars3, values):
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{val:.1f} MW",
            ha="center",
            fontweight="bold",
            fontsize=10,
        )
    ax3.set_ylabel("Power (MW)")
    ax3.set_title(f"Energy Breakdown (PUE = {breakdown['pue']})")
    ax3.set_ylim(0, max(values) * 1.3)
    ax3.grid(axis="y", alpha=0.3)

    ax4 = fig.add_subplot(gs[1, 1])
    tech_names = [
        c["technology"]
        .replace(" (D2C) Liquid", "\n(D2C)")
        .replace(" + Evaporative Towers", "\n+ Evap.")
        for c in cooling
    ]
    pue_mids = [c["pue_midpoint"] for c in cooling]
    pue_lows = [c["pue_low"] for c in cooling]
    pue_highs = [c["pue_high"] for c in cooling]
    yerr_low = [m - l for m, l in zip(pue_mids, pue_lows)]
    yerr_high = [h - m for m, h in zip(pue_mids, pue_highs)]

    tech_colors = ["#9E9E9E", "#607D8B", "#2196F3", "#00BCD4"]
    ax4.barh(
        tech_names,
        pue_mids,
        xerr=[yerr_low, yerr_high],
        color=tech_colors,
        edgecolor="white",
        linewidth=1.5,
        capsize=5,
    )
    ax4.axvline(
        x=tropical["target_pue"],
        color="#F44336",
        linestyle="--",
        linewidth=2,
        label=f"Target: {tropical['target_pue']}",
    )
    ax4.set_xlabel("PUE")
    ax4.set_title("Cooling Tech PUE Comparison")
    ax4.legend()
    ax4.grid(axis="x", alpha=0.3)

    fig.suptitle(
        "SPE Energython 2026 — IT Architecture & Load Profiling MVP",
        fontsize=16,
        fontweight="bold",
        y=1.01,
    )
    path1 = output_dir / "mvp_sizing_overview.png"
    fig.savefig(path1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(path1)

    # --- Figure 2: Load Profile Dashboard (Phase 2) ---
    fig2, axes2 = plt.subplots(3, 2, figsize=(16, 12))
    colors_map = {"cloud_heavy": "#2196F3", "ai_heavy": "#FF5722", "mixed": "#4CAF50"}

    for i, (key, df) in enumerate(profiles.items()):
        color = colors_map[key]

        avg_by_hour = df.groupby("hour_of_day")["it_load_kw"].mean() / 1000
        std_by_hour = df.groupby("hour_of_day")["it_load_kw"].std() / 1000
        ax_l = axes2[i, 0]
        ax_l.fill_between(
            avg_by_hour.index,
            avg_by_hour - std_by_hour,
            avg_by_hour + std_by_hour,
            alpha=0.2,
            color=color,
        )
        ax_l.plot(avg_by_hour.index, avg_by_hour.values, color=color, linewidth=2)
        ax_l.set_ylabel("IT Load (MW)")
        ax_l.set_title(f"{key.replace('_', ' ').title()} — Diurnal")
        ax_l.set_xlabel("Hour of Day")
        ax_l.set_xlim(0, 23)
        ax_l.grid(True, alpha=0.3)

        ax_r = axes2[i, 1]
        rolling = df["it_load_kw"].rolling(24, center=True).mean() / 1000
        ax_r.plot(df["hour"], rolling.values, color=color, linewidth=1)
        ax_r.set_ylabel("IT Load (MW)")
        ax_r.set_title(f"{key.replace('_', ' ').title()} — Annual (24h avg)")
        ax_r.set_xlabel("Hour of Year")
        ax_r.grid(True, alpha=0.3)

    fig2.suptitle(
        "Load Profiles — Phase 2 (15 MW / 12 MW IT)", fontsize=14, fontweight="bold"
    )
    plt.tight_layout()
    path2 = output_dir / "mvp_load_profiles.png"
    fig2.savefig(path2, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    paths.append(path2)

    # --- Figure 3: Summary Table ---
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

    table = ax3t.table(
        cellText=table_data, loc="center", cellLoc="center", colWidths=[0.4, 0.3]
    )
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

    ax3t.set_title(
        "IT Sizing Summary — Phase 2 (Full Deployment)",
        fontsize=13,
        fontweight="bold",
        pad=20,
    )
    path3 = output_dir / "mvp_summary_table.png"
    fig3.savefig(path3, dpi=150, bbox_inches="tight")
    plt.close(fig3)
    paths.append(path3)

    # --- Figure 4: 3-Phase Comparison ---
    fig4 = plt.figure(figsize=(16, 10))
    gs4 = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.3)

    # 4a: IT Capacity by Phase (bar chart)
    ax_ph1 = fig4.add_subplot(gs4[0, 0])
    phase_labels = ["Phase 1\n(10 MW)", "Phase 2\n(15 MW)", "Phase 3\n(20 MW)"]
    phase_it = [phase_sizing[f"phase_{i}"]["it_load_mw"] for i in [1, 2, 3]]
    phase_pues = [phase_sizing[f"phase_{i}"]["target_pue"] for i in [1, 2, 3]]
    phase_colors = ["#FF9800", "#2196F3", "#4CAF50"]

    bars_ph = ax_ph1.bar(
        phase_labels, phase_it, color=phase_colors, edgecolor="white", linewidth=1.5
    )
    for bar, it, pue in zip(bars_ph, phase_it, phase_pues):
        ax_ph1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{it:.1f} MW\n(PUE {pue})",
            ha="center",
            fontweight="bold",
            fontsize=10,
        )
    ax_ph1.set_ylabel("IT Load (MW)")
    ax_ph1.set_title("IT Capacity by Phase")
    ax_ph1.set_ylim(0, max(phase_it) * 1.3)
    ax_ph1.grid(axis="y", alpha=0.3)

    # 4b: PUE Sensitivity (line chart)
    ax_ph2 = fig4.add_subplot(gs4[0, 1])
    gross_values = [phase_sizing[f"phase_{i}"]["gross_mw"] for i in [1, 2, 3]]
    ax_ph2.plot(
        gross_values, phase_pues, "o-", color="#F44336", linewidth=2, markersize=8
    )
    for g, p, label in zip(gross_values, phase_pues, phase_labels):
        ax_ph2.annotate(
            f"PUE {p}",
            (g, p),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=10,
        )
    ax_ph2.set_xlabel("Gross Generation (MW)")
    ax_ph2.set_ylabel("PUE")
    ax_ph2.set_title("PUE Improves with Scale")
    ax_ph2.set_ylim(1.15, 1.35)
    ax_ph2.grid(True, alpha=0.3)

    # 4c: Rack Count by Phase (stacked bar)
    ax_ph3 = fig4.add_subplot(gs4[1, 0])
    zone_keys = ["zone_a", "zone_b", "zone_c"]
    zone_labels = ["Cloud (20 kW)", "HPC (50 kW)", "AI Immersion (100 kW)"]
    zone_colors = ["#2196F3", "#FF9800", "#F44336"]
    x_pos = np.arange(3)
    width = 0.6

    bottoms = np.zeros(3)
    for zk, zl, zc in zip(zone_keys, zone_labels, zone_colors):
        counts = [
            phase_racks[f"phase_{i}"]["zones"][zk]["rack_count"] for i in [1, 2, 3]
        ]
        ax_ph3.bar(
            x_pos, counts, width, bottom=bottoms, label=zl, color=zc, edgecolor="white"
        )
        bottoms += np.array(counts)

    ax_ph3.set_xticks(x_pos)
    ax_ph3.set_xticklabels(phase_labels)
    ax_ph3.set_ylabel("Rack Count")
    ax_ph3.set_title("Rack Deployment by Phase (Zone-Based)")
    ax_ph3.legend(loc="upper left")
    ax_ph3.grid(axis="y", alpha=0.3)

    # 4d: Revenue Potential (horizontal bar)
    ax_ph4 = fig4.add_subplot(gs4[1, 1])
    # Estimate revenue potential: $X per MW IT (illustrative)
    revenue_per_mw = 8  # $8M/year per MW IT (illustrative)
    revenues = [it * revenue_per_mw for it in phase_it]
    bars_rev = ax_ph4.barh(
        phase_labels, revenues, color=phase_colors, edgecolor="white", linewidth=1.5
    )
    for bar, rev, it in zip(bars_rev, revenues, phase_it):
        ax_ph4.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"${rev:.0f}M/yr\n({it:.1f} MW IT)",
            va="center",
            fontsize=10,
        )
    ax_ph4.set_xlabel("Estimated Annual Revenue ($M)")
    ax_ph4.set_title("Revenue Potential by Phase")
    ax_ph4.set_xlim(0, max(revenues) * 1.3)
    ax_ph4.grid(axis="x", alpha=0.3)

    fig4.suptitle("3-Phase Deployment Strategy", fontsize=16, fontweight="bold", y=1.01)
    path4 = output_dir / "mvp_phase_comparison.png"
    fig4.savefig(path4, dpi=150, bbox_inches="tight")
    plt.close(fig4)
    paths.append(path4)

    return paths


def main():
    paths = run_dashboard()
    print("MVP DASHBOARD COMPLETE")
    print("-" * 60)
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
