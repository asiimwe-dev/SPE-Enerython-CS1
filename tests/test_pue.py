import pytest
from src.pue_analysis.pue_calculator import (
    calculate_pue, calculate_dcie, calculate_overhead_ratio,
    calculate_thermal_load, energy_breakdown,
)
from src.pue_analysis.cooling_comparison import comparison_table
from src.pue_analysis.tropical_benchmark import get_tropical_pue_target


class TestPUECalculator:
    def test_pue_calculation(self):
        assert calculate_pue(15000, 12000) == 1.25

    def test_pue_zero_it(self):
        assert calculate_pue(15000, 0) == 1.0

    def test_pue_negative_it(self):
        assert calculate_pue(15000, -100) == 1.0

    def test_dcie(self):
        assert calculate_dcie(1.25) == 80.0

    def test_dcie_zero_pue(self):
        assert calculate_dcie(0) == 0.0

    def test_overhead_ratio(self):
        assert calculate_overhead_ratio(1.25) == 0.25

    def test_thermal_load(self):
        result = calculate_thermal_load(10.0, 4.186, 5.0)
        assert abs(result - 209.3) < 0.1

    def test_energy_breakdown(self):
        result = energy_breakdown(15000, 12000)
        assert result["pue"] == 1.25
        assert result["e_overhead_kw"] == 3000.0
        assert result["dcie_pct"] == 80.0


class TestCoolingComparison:
    def test_comparison_table_length(self):
        table = comparison_table()
        assert len(table) == 4

    def test_comparison_has_required_fields(self):
        table = comparison_table()
        for row in table:
            assert "technology" in row
            assert "pue_low" in row
            assert "pue_high" in row
            assert "dcie_range" in row
            assert "water_usage" in row


class TestTropicalBenchmark:
    def test_tropical_returns_dict(self):
        result = get_tropical_pue_target()
        assert "target_pue" in result
        assert "calculated_weighted_pue" in result
        assert "justification" in result

    def test_target_pue(self):
        result = get_tropical_pue_target()
        assert result["target_pue"] == 1.25

    def test_design_temp(self):
        result = get_tropical_pue_target()
        assert result["design_temp_c"] == 35
