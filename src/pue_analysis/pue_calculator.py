def calculate_pue(e_total_kw: float, e_it_kw: float) -> float:
    if e_it_kw <= 0:
        return 1.0
    return e_total_kw / e_it_kw


def calculate_dcie(pue: float) -> float:
    if pue <= 0:
        return 0.0
    return (1.0 / pue) * 100.0


def calculate_overhead_ratio(pue: float) -> float:
    return pue - 1.0


def calculate_thermal_load(mass_flow_kgs: float, cp_kj_per_kgk: float, delta_t_c: float) -> float:
    return mass_flow_kgs * cp_kj_per_kgk * delta_t_c


def energy_breakdown(e_total_kw: float, e_it_kw: float) -> dict:
    pue = calculate_pue(e_total_kw, e_it_kw)
    overhead = e_total_kw - e_it_kw
    return {
        "e_total_kw": e_total_kw,
        "e_it_kw": e_it_kw,
        "e_overhead_kw": round(overhead, 2),
        "pue": round(pue, 4),
        "dcie_pct": round(calculate_dcie(pue), 2),
        "overhead_ratio": round(calculate_overhead_ratio(pue), 4),
    }
