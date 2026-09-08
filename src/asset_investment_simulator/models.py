"""Configuration models for deterministic portfolio simulation.

Wooldridge-derived equations live in formulas.py. This module only defines
simulation configuration and Caisse portfolio policy inputs.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FundingPolicy:
    """Annual funding policy by investment class.

    mode values:
    - requirement: fund current requirement only
    - maintain_backlog: fund enough to hold opening backlog constant
    - target_ci: fund toward a target condition-index trajectory
    - fixed: use fixed annual amount per site when supplied in the asset data
    """

    sustainment_mode: str = "requirement"
    improvement_mode: str = "requirement"
    development_mode: str = "requirement"
    target_technical_ci: float | None = None
    target_functional_ci: float | None = None
    target_capacity_ci: float | None = None


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    start_year: int = 2027
    end_year: int = 2040
    real_discount_rate: float = 0.03
    deterioration_rate: float = 0.02
    inflation_rate: float = 0.0
    annual_sustainment_requirement_rate: float = 0.02
    annual_improvement_requirement_rate: float = 0.005
    annual_development_requirement_rate: float = 0.0
    annual_opex_growth_rate: float = 0.0
    annual_energy_intensity_reduction_rate: float = 0.0
    annual_service_demand_growth_rate: float = 0.0
    carbon_target_reduction_fraction_2040: float = 0.0
    funding: FundingPolicy = field(default_factory=FundingPolicy)

    @property
    def years(self) -> list[int]:
        return list(range(self.start_year, self.end_year + 1))

    @property
    def horizon_years(self) -> int:
        return self.end_year - self.start_year + 1
