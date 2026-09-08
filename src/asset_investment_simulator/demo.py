"""Small deterministic demonstration portfolio for the Streamlit app and tests."""
from __future__ import annotations

import pandas as pd


def demo_assets() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "caisse_id": "C001", "site_id": "C001-S01", "site_name": "Demo Québec",
            "asset_status": "active", "gross_floor_area": 8200, "crv": 4_100_000,
            "technical_backlog": 615_000, "functional_backlog": 300_000, "capacity_backlog": 120_000,
            "annual_opex": 275_000, "energy_intensity": 220, "emission_factor_kgco2e_per_energy_unit": 0.035,
            "service_demand": 92, "service_capacity": 110,
        },
        {
            "caisse_id": "C001", "site_id": "C001-S02", "site_name": "Demo Lévis",
            "asset_status": "active", "gross_floor_area": 5100, "crv": 2_550_000,
            "technical_backlog": 510_000, "functional_backlog": 255_000, "capacity_backlog": 0,
            "annual_opex": 190_000, "energy_intensity": 260, "emission_factor_kgco2e_per_energy_unit": 0.040,
            "service_demand": 55, "service_capacity": 75,
        },
        {
            "caisse_id": "C002", "site_id": "C002-S01", "site_name": "Demo Rimouski",
            "asset_status": "active", "gross_floor_area": 7000, "crv": 3_500_000,
            "technical_backlog": 350_000, "functional_backlog": 140_000, "capacity_backlog": 175_000,
            "annual_opex": 230_000, "energy_intensity": 205, "emission_factor_kgco2e_per_energy_unit": 0.025,
            "service_demand": 88, "service_capacity": 85,
        },
    ])


def demo_systems() -> pd.DataFrame:
    return pd.DataFrame([
        {"site_id": "C001-S01", "system_life": 20, "percent_used": 0.90, "percent_original_cost": 0.12, "percent_renewed": 1.0},
        {"site_id": "C001-S02", "system_life": 15, "percent_used": 0.80, "percent_original_cost": 0.10, "percent_renewed": 1.0},
        {"site_id": "C002-S01", "system_life": 25, "percent_used": 0.60, "percent_original_cost": 0.15, "percent_renewed": 1.0},
    ])
