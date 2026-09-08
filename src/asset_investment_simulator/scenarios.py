"""Named deterministic scenario configurations.

These are Caisse planning policies, not Wooldridge thesis equations.
"""
from __future__ import annotations

from .models import FundingPolicy, ScenarioConfig


def baseline() -> ScenarioConfig:
    return ScenarioConfig(
        name="Baseline",
        funding=FundingPolicy(
            sustainment_mode="requirement",
            improvement_mode="requirement",
            development_mode="requirement",
        ),
    )


def maintain_condition() -> ScenarioConfig:
    return ScenarioConfig(
        name="Maintain Condition",
        funding=FundingPolicy(
            sustainment_mode="maintain_backlog",
            improvement_mode="maintain_backlog",
            development_mode="maintain_backlog",
        ),
    )


def target_condition(
    technical_ci: float = 0.10,
    functional_ci: float = 0.08,
    capacity_ci: float = 0.05,
) -> ScenarioConfig:
    return ScenarioConfig(
        name="Target Condition",
        funding=FundingPolicy(
            sustainment_mode="target_ci",
            improvement_mode="target_ci",
            development_mode="target_ci",
            target_technical_ci=technical_ci,
            target_functional_ci=functional_ci,
            target_capacity_ci=capacity_ci,
        ),
    )


def integrated_2040() -> ScenarioConfig:
    return ScenarioConfig(
        name="Integrated 2040",
        annual_energy_intensity_reduction_rate=0.025,
        annual_service_demand_growth_rate=-0.005,
        carbon_target_reduction_fraction_2040=1.0,
        funding=FundingPolicy(
            sustainment_mode="target_ci",
            improvement_mode="target_ci",
            development_mode="target_ci",
            target_technical_ci=0.08,
            target_functional_ci=0.06,
            target_capacity_ci=0.04,
        ),
    )


SCENARIOS = {
    "Baseline": baseline,
    "Maintain Condition": maintain_condition,
    "Target Condition": target_condition,
    "Integrated 2040": integrated_2040,
}
