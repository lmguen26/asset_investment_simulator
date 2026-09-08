# Model Guide — Principles, Formulas & Terminology

This guide is part of the model and is displayed inside the application. It separates source-derived Wooldridge concepts from Caisse-specific extensions.

## 1. Purpose

The model links facility investment requirements, funding and portfolio condition over time. It is extended for Caisse network planning through 2040 with service, footprint, energy, carbon and network strategy.

> **A scenario is not a forecast.** A 2040 result represents the consequence of supplied initial conditions, assumptions, funding strategy, portfolio rules and uncertainty.

## 2. Wooldridge framework

Three principal drivers/condition dimensions are linked to three investment classes:

| Driver | Backlog / condition | Investment response |
|---|---|---|
| Deterioration | Technical | Sustainment |
| Obsolescence | Functional | Improvement |
| Capacity | Capacity | Development |

Operations is a separate cash-flow class.

### Technical ↔ Sustainment

Sustainment protects and preserves an existing facility and maintains its level of service. Maintenance and repair, system renewal and existing deficiencies are associated with Sustainment. Unfunded Sustainment requirements contribute to Technical Backlog.

**W-3.4**

`TB_t = TB_(t-1) * (1 + RateDet + RateInf) + SustainmentRequirements_t - SustainmentFunding_t`

The rate form is additive, not `(1+d)(1+i)`.

**Technical Condition Index**

`TCI = TechnicalBacklog / CRV`

Lower is better. The ratio is not the percentage of physical life consumed.

### Functional ↔ Improvement

Functional condition represents obsolescence and requirements for modernization, reconfiguration, technology, use, code, function and efficiency. The associated investment class is Improvement.

**W-3.5**

`FB_t = FB_(t-1) * (1 + RateInf) + ImprovementRequirements_t - ImprovementFunding_t`

`FunctionalCI = FunctionalBacklog / CRV`

A facility may have good Technical Condition while being functionally obsolete.

### Capacity ↔ Development

Capacity condition represents outstanding Development requirements associated with capacity. Development includes additions, new facilities and replacement facilities.

**W-3.6**

`CB_t = CB_(t-1) * (1 + RateInf) + DevelopmentRequirements_t - DevelopmentFunding_t`

`CapacityCI = CapacityBacklog / CRV`

For the Caisse extension, raw excess capacity is not automatically converted to Capacity Backlog; it can instead trigger resizing/consolidation strategy.

### Comprehensive Condition

**W-3.7**

`ComprehensiveCI = (TechnicalBacklog + FunctionalBacklog + CapacityBacklog) / CRV`

## 3. Current Replacement Value

**W-3.8**

`CRV = FacilitySize * BaseConstructionCost * AreaCostFactor * AdjustmentFactor`

Adjustment factors may capture owner-specific contingencies, secondary plant, installed equipment, complexity and overhead.

## 4. System renewal

**W-3.1** `RemainingLife = SystemLife * (1 - PercentUsed)`

**W-3.2** `RenewalCost = CRV * PercentOriginalCost * PercentRenewed`

**W-3.3** `t_n = RemainingLife + SystemLife * (n - 1)`

The legacy formulation assumes replacement in kind, repeated cycles based on expected service life and adequate maintenance to preserve expected life. Enhanced causal behavior belongs in a separate extension layer.

## 5. Economics

**W-2.2** `PV = sum(C_t / (1+r)^t)`

**W-2.3** `AE = PV * r / (1 - (1+r)^(-T))`

The MVP should use real/constant currency with a configurable real discount rate. Any default rate is an explicit model assumption, not a thesis constant.

## 6. Caisse extensions — not thesis formulas

### Portfolio hierarchy

`Caisse Network Portfolio → Caisse (189 subportfolios) → Site(s)`

### Service and facility separation

A physical site and a service point are not equivalent. Closing/consolidating a site may redistribute service to another site or alternative service point.

### Capacity gap

**CAISSE-C01**

`CapacityGap = RequiredCapacity - AvailableCapacity`

Positive is shortfall; negative is excess capacity.

### Energy

**CAISSE-E01**

`Energy = Area * EnergyIntensity`

### Operational carbon

**CAISSE-E02**

`Carbon = sum(Energy_by_fuel * EmissionFactor_by_fuel)`

Energy and carbon remain outside Wooldridge condition indices.

## 7. Incomplete energy/carbon data

Measured portfolio observations may be used to calibrate proxy/statistical models for unmeasured sites. Modelled values must retain provenance and uncertainty. Values should be classified as MEASURED, DERIVED, MODELLED, ASSUMED or SCENARIO_OVERRIDE.

Do not extrapolate a simple portfolio average when site characteristics can support a better conditional model.

## 8. Modelling paradigms

- **Equation model:** what happens quantitatively to an asset.
- **Network/graph model:** how Caisses, sites, services, communities, systems and actions relate.
- **Decision model:** what actions satisfy objectives and constraints.
- **Stochastic model:** how uncertainty changes possible outcomes.

The graph does not replace the equations.

## 9. Limitations and provenance

The faithful Wooldridge layer does not automatically model every causal interaction, including all effects of maintenance on future renewal cycles, renewal on existing backlog, or improvement on utilization/utilities/M&R. Such behavior must be implemented and labelled as an extension.

Every formula/rule in code must carry provenance: `W-*` for Wooldridge-derived formulas and `CAISSE-*` for Caisse-specific extensions.
