import pytest
import pandas as pd
from src.load_profiling.scenarios import SCENARIOS
from src.load_profiling.profile_generator import generate_load_profiles, save_profiles
from pathlib import Path
import tempfile


class TestScenarios:
    def test_scenarios_loaded(self):
        assert len(SCENARIOS) == 3
        assert "cloud_heavy" in SCENARIOS
        assert "ai_heavy" in SCENARIOS
        assert "mixed" in SCENARIOS

    def test_scenario_properties(self):
        for key, s in SCENARIOS.items():
            assert 0 < s.peak_utilization <= 1.0
            assert 0 < s.offpeak_utilization < s.peak_utilization
            assert 0 <= s.diurnal_amplitude <= 1.0
            assert 0 <= s.ai_batch_pct <= 1.0


class TestProfileGenerator:
    def test_generates_all_scenarios(self):
        profiles = generate_load_profiles()
        assert len(profiles) == 3
        assert "cloud_heavy" in profiles
        assert "ai_heavy" in profiles
        assert "mixed" in profiles

    def test_hourly_resolution(self):
        profiles = generate_load_profiles()
        for key, df in profiles.items():
            assert len(df) == 8760
            assert "hour" in df.columns
            assert "it_load_kw" in df.columns
            assert "facility_load_kw" in df.columns

    def test_it_load_positive(self):
        profiles = generate_load_profiles()
        for key, df in profiles.items():
            assert (df["it_load_kw"] > 0).all()

    def test_facility_greater_than_it(self):
        profiles = generate_load_profiles()
        for key, df in profiles.items():
            assert (df["facility_load_kw"] >= df["it_load_kw"]).all()

    def test_scenario_column(self):
        profiles = generate_load_profiles()
        for key, df in profiles.items():
            assert (df["scenario"] == key).all()

    def test_save_profiles(self):
        profiles = generate_load_profiles()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = save_profiles(profiles, Path(tmpdir))
            assert len(paths) == 3
            for p in paths:
                assert p.exists()
                df = pd.read_csv(p)
                assert len(df) == 8760
