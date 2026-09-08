"""Caisse-specific extensions.

These are NOT Wooldridge thesis formulas. Keep provenance explicit.
"""
from __future__ import annotations


def energy_use(area: float, energy_intensity: float) -> float:
    """CAISSE-E01: Energy = Area * EnergyIntensity."""
    return area * energy_intensity


def operational_carbon(energy_by_fuel: dict[str, float], emission_factors: dict[str, float]) -> float:
    """CAISSE-E02: sum(Energy_f * EmissionFactor_f)."""
    return sum(value * emission_factors.get(fuel, 0.0) for fuel, value in energy_by_fuel.items())


def capacity_gap(required_capacity: float, available_capacity: float) -> float:
    """CAISSE-C01. Positive = shortfall; negative = excess capacity."""
    return required_capacity - available_capacity


def service_constraint(required_service: float, available_service: float) -> bool:
    """CAISSE-S01: available service must meet/exceed required service."""
    return available_service >= required_service
