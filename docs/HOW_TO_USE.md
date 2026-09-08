# How to Use

## 1. Prepare the Asset Register

Export your authoritative source list. Map it outside the application to `data/templates/asset_register_template.csv`. Keep `source_system` and `source_record_id` so every canonical record can be traced back.

## 2. Validate identity and hierarchy

Import the canonical file. Resolve missing required fields, duplicate `site_id` values and sites without a `caisse_id`. The expected hierarchy is portfolio → 189 Caisse subportfolios → sites.

## 3. Link analytical data products

Join condition/FCA, systems, energy/carbon, service/capacity, lease and other analytical datasets by stable identifiers. Do not invent missing values in the Asset Register merely to satisfy the simulator.

## 4. Establish provenance

For important analytical values, record whether they are MEASURED, DERIVED, MODELLED, ASSUMED or SCENARIO_OVERRIDE, together with source date/model version where possible.

## 5. Review the Model Guide

Before interpreting results, use the in-app **Model guide**. Technical/Sustainment, Functional/Improvement and Capacity/Development have specific meanings inherited from the Wooldridge framework.

## 6. Configure scenarios

Initial strategy families are Baseline, Condition First, Network Optimization, Carbon First and Integrated 2040. Scenario assumptions should be explicit and versioned.

## 7. Run deterministic calculations first

Validate opening balances, requirements, funding, ending balances and condition indices before introducing Monte Carlo. Every annual calculation should be auditable.

## 8. Add uncertainty only after calibration

Use measured portfolio observations to calibrate distributions/proxy models. Report P10/P50/P90 and probabilities rather than false precision.

## 9. Preserve service constraints

Cost/carbon minimization must not be allowed to solve the problem by simply closing sites. Required service, strategic presence, capacity and later geographic access/travel-time constraints must be explicit.

## 10. Record review feedback

Use **Review notes** to capture observations and questions. Export JSON for AI-assisted model evolution. Notes are review input, not automatically approved business rules.

## 11. Development workflow with GitHub Copilot

Create a feature branch per change, e.g. `feature/energy-proxy`, `feature/monte-carlo`, `feature/network-optimization`.

Suggested Copilot instruction:

> Review `docs/MODEL_GUIDE.md`, the relevant source module and tests before changing the model. State whether the change is Wooldridge-derived or a Caisse extension. Identify the equation, assumption, data mapping or business rule affected. Keep constants configurable. Add regression tests for any change that alters scenario results. Do not present Caisse extensions as thesis formulas.

Recommended sequence: canonical import/data quality → deterministic engine → energy proxy/provenance → service/network graph → Monte Carlo → constrained optimization.
