"""Deterministic site -> Caisse -> portfolio simulation engine.

The engine deliberately separates:
1. Wooldridge-derived equations from formulas.py;
2. Caisse portfolio extensions from extensions.py; and
3. scenario policy from scenarios.py / models.py.

All monetary calculations are real/constant currency by default.
"""
from __future__ import annotations

from dataclasses import asdict
from math import ceil
from typing import Iterable

import pandas as pd

from .extensions import capacity_gap, energy_use, service_constraint
from .formulas import (
    capacity_backlog,
    condition_indices,
    current_replacement_value,
    functional_backlog,
    present_value,
    remaining_system_life,
    renewal_cost,
    renewal_time,
    technical_backlog,
)
from .models import ScenarioConfig


REQUIRED_ASSET_COLUMNS = {"caisse_id", "site_id", "gross_floor_area"}


def _number(row: pd.Series, name: str, default: float = 0.0) -> float:
    value = row.get(name, default)
    if pd.isna(value):
        return float(default)
    return float(value)


def validate_assets(assets: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_ASSET_COLUMNS - set(assets.columns))
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing))
    if "site_id" in assets and assets["site_id"].duplicated().any():
        errors.append("site_id must be unique")
    if "gross_floor_area" in assets and (pd.to_numeric(assets["gross_floor_area"], errors="coerce") <= 0).any():
        errors.append("gross_floor_area must be greater than zero")
    return errors


def _crv(row: pd.Series) -> float:
    direct = row.get("crv")
    if direct is not None and not pd.isna(direct) and float(direct) > 0:
        return float(direct)
    return current_replacement_value(
        _number(row, "gross_floor_area"),
        _number(row, "base_construction_cost_per_area", 350.0),
        _number(row, "area_cost_factor", 1.0),
        _number(row, "adjustment_factor", 1.0),
    )


def build_renewal_schedule(
    assets: pd.DataFrame,
    systems: pd.DataFrame | None,
    config: ScenarioConfig,
) -> dict[tuple[str, int], float]:
    """Create site/year sustainment renewal requirements using W-3.1..W-3.3.

    systems columns: site_id, system_life, percent_used,
    percent_original_cost, percent_renewed.
    """
    if systems is None or systems.empty:
        return {}
    required = {
        "site_id", "system_life", "percent_used",
        "percent_original_cost", "percent_renewed",
    }
    missing = required - set(systems.columns)
    if missing:
        raise ValueError("System table missing columns: " + ", ".join(sorted(missing)))

    crv_by_site = {str(r["site_id"]): _crv(r) for _, r in assets.iterrows()}
    schedule: dict[tuple[str, int], float] = {}
    horizon = config.horizon_years
    for _, s in systems.iterrows():
        site_id = str(s["site_id"])
        if site_id not in crv_by_site:
            continue
        life = float(s["system_life"])
        if life <= 0:
            continue
        rem = remaining_system_life(life, float(s["percent_used"]))
        cost = renewal_cost(
            crv_by_site[site_id],
            float(s["percent_original_cost"]),
            float(s["percent_renewed"]),
        )
        cycle = 1
        while True:
            offset = renewal_time(rem, life, cycle)
            if offset > horizon:
                break
            year = config.start_year + max(0, ceil(offset) - 1)
            if year <= config.end_year:
                schedule[(site_id, year)] = schedule.get((site_id, year), 0.0) + cost
            cycle += 1
    return schedule


def _target_ci(opening_ci: float, final_ci: float | None, year_index: int, years: int) -> float:
    if final_ci is None:
        return opening_ci
    fraction = year_index / years
    return opening_ci + (final_ci - opening_ci) * fraction


def _funding(
    mode: str,
    opening_backlog: float,
    requirement: float,
    growth_rate_on_backlog: float,
    crv: float,
    opening_ci_at_horizon: float,
    target_ci: float | None,
    year_index: int,
    years: int,
    fixed_amount: float,
) -> float:
    if mode == "requirement":
        return max(0.0, requirement)
    if mode == "maintain_backlog":
        return max(0.0, opening_backlog * growth_rate_on_backlog + requirement)
    if mode == "target_ci":
        desired_ci = _target_ci(opening_ci_at_horizon, target_ci, year_index, years)
        desired_backlog = max(0.0, desired_ci * crv)
        return max(0.0, opening_backlog * (1.0 + growth_rate_on_backlog) + requirement - desired_backlog)
    if mode == "fixed":
        return max(0.0, fixed_amount)
    raise ValueError(f"Unknown funding mode: {mode}")


def simulate(
    assets: pd.DataFrame,
    config: ScenarioConfig,
    systems: pd.DataFrame | None = None,
) -> dict[str, object]:
    """Run an auditable deterministic annual simulation.

    Returns site-year detail, Caisse-year rollup, portfolio-year rollup,
    summary metrics, scenario configuration and calculation provenance.
    """
    errors = validate_assets(assets)
    if errors:
        raise ValueError("; ".join(errors))

    assets = assets.copy()
    assets["site_id"] = assets["site_id"].astype(str)
    assets["caisse_id"] = assets["caisse_id"].astype(str)
    renewal_schedule = build_renewal_schedule(assets, systems, config)
    records: list[dict[str, object]] = []

    for _, asset in assets.iterrows():
        site_id = str(asset["site_id"])
        caisse_id = str(asset["caisse_id"])
        crv = _crv(asset)
        technical = _number(asset, "technical_backlog")
        functional = _number(asset, "functional_backlog")
        capacity = _number(asset, "capacity_backlog")
        opening_indices = condition_indices(technical, functional, capacity, crv)

        area = _number(asset, "gross_floor_area")
        opex = _number(asset, "annual_opex")
        energy_intensity = _number(asset, "energy_intensity", 0.0)
        emission_factor = _number(asset, "emission_factor_kgco2e_per_energy_unit", 0.0)
        service_demand = _number(asset, "service_demand", 0.0)
        service_capacity = _number(asset, "service_capacity", service_demand)
        active = str(asset.get("asset_status", "active")).lower() not in {"inactive", "disposed", "closed"}
        baseline_carbon = energy_use(area, energy_intensity) * emission_factor if active else 0.0

        for year_index, year in enumerate(config.years, start=1):
            opening_technical = technical
            opening_functional = functional
            opening_capacity = capacity

            renewal_req = renewal_schedule.get((site_id, year), 0.0)
            sustainment_req = crv * config.annual_sustainment_requirement_rate + renewal_req
            improvement_req = crv * config.annual_improvement_requirement_rate
            development_req = crv * config.annual_development_requirement_rate

            sustainment_funding = _funding(
                config.funding.sustainment_mode, opening_technical, sustainment_req,
                config.deterioration_rate + config.inflation_rate, crv,
                opening_indices["technical_ci"], config.funding.target_technical_ci,
                year_index, config.horizon_years,
                _number(asset, "fixed_sustainment_funding"),
            )
            improvement_funding = _funding(
                config.funding.improvement_mode, opening_functional, improvement_req,
                config.inflation_rate, crv,
                opening_indices["functional_ci"], config.funding.target_functional_ci,
                year_index, config.horizon_years,
                _number(asset, "fixed_improvement_funding"),
            )
            development_funding = _funding(
                config.funding.development_mode, opening_capacity, development_req,
                config.inflation_rate, crv,
                opening_indices["capacity_ci"], config.funding.target_capacity_ci,
                year_index, config.horizon_years,
                _number(asset, "fixed_development_funding"),
            )

            technical = technical_backlog(
                opening_technical, config.deterioration_rate, config.inflation_rate,
                sustainment_req, sustainment_funding,
            )
            functional = functional_backlog(
                opening_functional, config.inflation_rate,
                improvement_req, improvement_funding,
            )
            capacity = capacity_backlog(
                opening_capacity, config.inflation_rate,
                development_req, development_funding,
            )
            indices = condition_indices(technical, functional, capacity, crv)

            if year_index > 1:
                opex *= 1.0 + config.annual_opex_growth_rate
                energy_intensity *= max(0.0, 1.0 - config.annual_energy_intensity_reduction_rate)
                service_demand *= 1.0 + config.annual_service_demand_growth_rate

            energy = energy_use(area, energy_intensity) if active else 0.0
            carbon = energy * emission_factor
            target_reduction = config.carbon_target_reduction_fraction_2040 * (year_index / config.horizon_years)
            carbon_target = baseline_carbon * max(0.0, 1.0 - target_reduction)
            service_gap = capacity_gap(service_demand, service_capacity)
            service_ok = service_constraint(service_demand, service_capacity)
            capex = sustainment_funding + improvement_funding + development_funding
            totex = capex + (opex if active else 0.0)

            records.append({
                "year": year,
                "caisse_id": caisse_id,
                "site_id": site_id,
                "site_name": asset.get("site_name", site_id),
                "active": active,
                "area": area,
                "crv": crv,
                "opening_technical_backlog": opening_technical,
                "technical_deterioration_amount": opening_technical * config.deterioration_rate,
                "sustainment_requirements": sustainment_req,
                "system_renewal_requirements": renewal_req,
                "sustainment_funding": sustainment_funding,
                "technical_backlog": technical,
                "opening_functional_backlog": opening_functional,
                "improvement_requirements": improvement_req,
                "improvement_funding": improvement_funding,
                "functional_backlog": functional,
                "opening_capacity_backlog": opening_capacity,
                "development_requirements": development_req,
                "development_funding": development_funding,
                "capacity_backlog": capacity,
                **indices,
                "annual_opex": opex if active else 0.0,
                "capex": capex,
                "totex": totex,
                "energy_intensity": energy_intensity,
                "energy_use": energy,
                "carbon_kgco2e": carbon,
                "carbon_target_kgco2e": carbon_target,
                "carbon_gap_kgco2e": carbon - carbon_target,
                "service_demand": service_demand,
                "service_capacity": service_capacity,
                "service_gap": service_gap,
                "service_constraint_met": service_ok,
            })

    detail = pd.DataFrame.from_records(records)
    additive = [
        "area", "crv", "opening_technical_backlog", "technical_deterioration_amount",
        "sustainment_requirements", "system_renewal_requirements", "sustainment_funding",
        "technical_backlog", "opening_functional_backlog", "improvement_requirements",
        "improvement_funding", "functional_backlog", "opening_capacity_backlog",
        "development_requirements", "development_funding", "capacity_backlog",
        "annual_opex", "capex", "totex", "energy_use", "carbon_kgco2e",
        "carbon_target_kgco2e", "carbon_gap_kgco2e", "service_demand", "service_capacity",
        "service_gap",
    ]

    def rollup(group_cols: list[str]) -> pd.DataFrame:
        grouped = detail.groupby(group_cols, as_index=False)[additive].sum()
        grouped["technical_ci"] = grouped["technical_backlog"] / grouped["crv"]
        grouped["functional_ci"] = grouped["functional_backlog"] / grouped["crv"]
        grouped["capacity_ci"] = grouped["capacity_backlog"] / grouped["crv"]
        grouped["comprehensive_ci"] = (
            grouped["technical_backlog"] + grouped["functional_backlog"] + grouped["capacity_backlog"]
        ) / grouped["crv"]
        return grouped

    caisse_year = rollup(["year", "caisse_id"])
    portfolio_year = rollup(["year"])
    pv_totex = present_value(portfolio_year["totex"].tolist(), config.real_discount_rate)
    end = portfolio_year.iloc[-1]
    start = portfolio_year.iloc[0]
    summary = {
        "scenario": config.name,
        "sites": int(assets["site_id"].nunique()),
        "caisses": int(assets["caisse_id"].nunique()),
        "pv_totex": float(pv_totex),
        "cumulative_capex": float(portfolio_year["capex"].sum()),
        "ending_technical_ci": float(end["technical_ci"]),
        "ending_functional_ci": float(end["functional_ci"]),
        "ending_capacity_ci": float(end["capacity_ci"]),
        "ending_comprehensive_ci": float(end["comprehensive_ci"]),
        "ending_carbon_kgco2e": float(end["carbon_kgco2e"]),
        "carbon_reduction_fraction": 0.0 if float(start["carbon_kgco2e"]) == 0 else 1.0 - float(end["carbon_kgco2e"]) / float(start["carbon_kgco2e"]),
        "ending_service_gap": float(end["service_gap"]),
    }
    return {
        "site_year": detail,
        "caisse_year": caisse_year,
        "portfolio_year": portfolio_year,
        "summary": summary,
        "scenario_config": asdict(config),
        "provenance": {
            "condition_core": "Wooldridge W-3.4 to W-3.8",
            "system_renewal": "Wooldridge W-3.1 to W-3.3",
            "economics": "Wooldridge W-2.2; real/constant currency convention",
            "energy_carbon_service": "Caisse extensions; not thesis formulas",
            "simulation_type": "deterministic",
        },
    }
