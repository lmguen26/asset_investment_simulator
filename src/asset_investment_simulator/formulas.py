"""Auditable quantitative formulas.

W-* identifiers reproduce the Wooldridge-derived deterministic core.
Caisse extensions must be kept outside this module.
"""
from __future__ import annotations


def remaining_system_life(system_life: float, percent_used: float) -> float:
    """W-3.1: RemainingLife = SystemLife * (1 - %Used)."""
    return system_life * (1.0 - percent_used)


def renewal_cost(crv: float, percent_original_cost: float, percent_renewed: float) -> float:
    """W-3.2: RenewalCost = CRV * %OriginalCost * %Renewed."""
    return crv * percent_original_cost * percent_renewed


def renewal_time(remaining_life: float, system_life: float, cycle_number: int) -> float:
    """W-3.3: t_n = RemainingLife + SystemLife(n-1)."""
    return remaining_life + system_life * (cycle_number - 1)


def technical_backlog(opening: float, deterioration_rate: float, inflation_rate: float,
                      sustainment_requirements: float, sustainment_funding: float) -> float:
    """W-3.4 exact additive rate form from the thesis."""
    return max(0.0, opening * (1.0 + deterioration_rate + inflation_rate)
               + sustainment_requirements - sustainment_funding)


def functional_backlog(opening: float, inflation_rate: float,
                       improvement_requirements: float, improvement_funding: float) -> float:
    """W-3.5."""
    return max(0.0, opening * (1.0 + inflation_rate)
               + improvement_requirements - improvement_funding)


def capacity_backlog(opening: float, inflation_rate: float,
                     development_requirements: float, development_funding: float) -> float:
    """W-3.6."""
    return max(0.0, opening * (1.0 + inflation_rate)
               + development_requirements - development_funding)


def condition_indices(technical: float, functional: float, capacity: float, crv: float) -> dict[str, float]:
    """W-3.7: Technical, Functional, Capacity and Comprehensive condition indices."""
    if crv <= 0:
        raise ValueError("CRV must be greater than zero")
    return {
        "technical_ci": technical / crv,
        "functional_ci": functional / crv,
        "capacity_ci": capacity / crv,
        "comprehensive_ci": (technical + functional + capacity) / crv,
    }


def current_replacement_value(area: float, base_construction_cost: float,
                              area_cost_factor: float = 1.0, adjustment_factor: float = 1.0) -> float:
    """W-3.8."""
    return area * base_construction_cost * area_cost_factor * adjustment_factor


def present_value(cashflows: list[float], real_discount_rate: float) -> float:
    """W-2.2. Cashflows are t=1..T."""
    return sum(c / ((1.0 + real_discount_rate) ** t) for t, c in enumerate(cashflows, start=1))


def annual_equivalent(pv: float, real_discount_rate: float, years: int) -> float:
    """W-2.3."""
    if years <= 0:
        raise ValueError("years must be positive")
    if real_discount_rate == 0:
        return pv / years
    return pv * real_discount_rate / (1.0 - (1.0 + real_discount_rate) ** (-years))
