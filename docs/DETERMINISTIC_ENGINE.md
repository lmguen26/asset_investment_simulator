# Deterministic Engine — 2027–2040

## Purpose

This engine is the auditable baseline for all later stochastic and optimization work. It computes annual site states, rolls them up to each Caisse subportfolio, and then to the full network portfolio.

A scenario is **not a forecast**. It is the deterministic consequence of the loaded state, assumptions and funding policy.

## Model separation

### Wooldridge-derived core

Implemented in `src/asset_investment_simulator/formulas.py` and used without mixing Caisse-specific business rules:

- W-3.1 Remaining system life
- W-3.2 System renewal cost
- W-3.3 Renewal time profile
- W-3.4 Technical backlog propagation
- W-3.5 Functional backlog propagation
- W-3.6 Capacity backlog propagation
- W-3.7 Technical, Functional, Capacity and Comprehensive condition indices
- W-3.8 Current Replacement Value
- W-2.2 Present Value
- W-2.3 Annual Equivalent (available in the formula module)

Canonical relationships:

- Deterioration -> Technical Backlog -> Sustainment
- Obsolescence -> Functional Backlog -> Improvement
- Capacity -> Capacity Backlog -> Development

### Caisse extensions

Kept outside the Wooldridge formula module:

- energy intensity and annual energy use;
- operational carbon;
- service demand and service capacity;
- Caisse/site hierarchy;
- scenario funding policies;
- future network actions, carbon transition, stochastic modelling and optimization.

## Annual state transition

For every site and year the engine records opening balances, requirements, funding and ending balances.

Technical:

`TB_t = TB_(t-1) * (1 + deterioration + inflation) + sustainment requirements - sustainment funding`

Functional:

`FB_t = FB_(t-1) * (1 + inflation) + improvement requirements - improvement funding`

Capacity:

`CB_t = CB_(t-1) * (1 + inflation) + development requirements - development funding`

Condition indices are then calculated from ending backlog and CRV.

## Requirements

Base annual requirements are currently configurable rates of CRV. Optional system records add explicit renewal events using W-3.1 through W-3.3.

This is deliberate: CRV-rate requirements are a planning assumption, while system renewal timing is a thesis-derived algorithm. They are kept identifiable in the calculation audit.

## Funding policies

The engine supports four deterministic funding modes by investment class:

- `requirement` — fund the current annual requirement;
- `maintain_backlog` — fund enough to hold the opening backlog constant;
- `target_ci` — fund enough to follow a linear path from opening CI to a specified final CI;
- `fixed` — read a fixed annual funding amount from the site data.

The funding policy is a scenario rule, **not** a Wooldridge equation.

## Economics

The default model operates in real/constant currency. Inflation therefore defaults to zero and Present Value uses a configurable real discount rate. Annual site TOTEX is modelled as funded Sustainment + Improvement + Development + OPEX.

## Energy and carbon

When energy information is available:

`Energy = Area * EnergyIntensity`

`OperationalCarbon = Energy * EmissionFactor`

These are Caisse extensions and are intentionally excluded from the Wooldridge condition indices.

The current deterministic engine reports both actual modelled carbon and a linear carbon target trajectory. It does **not** automatically force the portfolio to meet that target. The gap is visible and must later be addressed through explicit portfolio actions and/or optimization.

## Service constraint

`service_gap = required service demand - available service capacity`

A positive value is a shortfall. A negative value is excess capacity. Excess capacity is not automatically converted into Capacity Backlog.

## Outputs

`site_year` — full annual calculation audit by site.

`caisse_year` — additive measures rolled up to each Caisse; condition indices are recalculated from aggregate backlog / aggregate CRV, not averaged across sites.

`portfolio_year` — same logic across the entire loaded network.

`summary` — decision-level metrics including PV TOTEX, cumulative CAPEX, ending condition indices, carbon change and service gap.

## Limitations intentionally preserved

The deterministic engine does not yet claim that:

- renewal automatically removes an independently supplied Technical Backlog;
- maintenance changes future system service lives;
- Improvement automatically changes OPEX, energy or service utilization;
- Development automatically opens/closes/merges sites;
- carbon targets are achieved without explicit actions;
- deterministic outputs quantify uncertainty.

Those interactions belong in separately identified Caisse extensions. They should not be silently inserted into the Wooldridge core.

## Change-control rule

Any change that alters a 2040 result must identify whether the cause is:

1. a Wooldridge equation;
2. an explicit model assumption;
3. a Caisse business rule;
4. a data mapping or source change; or
5. a scenario policy.

Regression tests must accompany the change.
