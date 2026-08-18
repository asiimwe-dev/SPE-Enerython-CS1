import pytest

from src.it_sizing.rack_allocation import allocate_racks
from src.it_sizing.sizing_calculator import calculate_it_load
from src.it_sizing.topology import ZONES


class TestSizingCalculator:
    def test_it_load_calculation(self):
        result = calculate_it_load(gross_mw=15.0, pue=1.25)
        assert result["it_load_mw"] == 12.0
        assert result["target_pue"] == 1.25
        assert result["gross_generation_mw"] == 15.0

    def test_dcie(self):
        result = calculate_it_load(gross_mw=15.0, pue=1.25)
        assert result["dcie_pct"] == 80.0

    def test_overhead_ratio(self):
        result = calculate_it_load(gross_mw=15.0, pue=1.25)
        assert result["overhead_ratio"] == 0.25

    def test_different_pue(self):
        result = calculate_it_load(gross_mw=20.0, pue=1.4)
        assert abs(result["it_load_mw"] - 14.29) < 0.01

    def test_zero_it_load_edge_case(self):
        result = calculate_it_load(gross_mw=0.0, pue=1.25)
        assert result["it_load_mw"] == 0.0


class TestRackAllocation:
    def test_total_racks(self):
        alloc = allocate_racks()
        assert alloc["total"]["rack_count"] == 360

    def test_zone_counts(self):
        alloc = allocate_racks()
        assert alloc["zone_a"]["rack_count"] == 250
        assert alloc["zone_b"]["rack_count"] == 80
        assert alloc["zone_c"]["rack_count"] == 30

    def test_zone_mw(self):
        alloc = allocate_racks()
        assert alloc["zone_a"]["zone_mw"] == 5.0
        assert alloc["zone_b"]["zone_mw"] == 4.0
        assert alloc["zone_c"]["zone_mw"] == 3.0


class TestTopology:
    def test_zones_loaded(self):
        assert len(ZONES) == 3
        assert "zone_a" in ZONES
        assert "zone_b" in ZONES
        assert "zone_c" in ZONES

    def test_zone_properties(self):
        assert ZONES["zone_a"].rack_density_kw == 20
        assert ZONES["zone_b"].rack_density_kw == 50
        assert ZONES["zone_c"].rack_density_kw == 100
