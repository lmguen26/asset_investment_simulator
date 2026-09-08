# Architecture

## Principle

Use complementary modelling paradigms rather than forcing the entire problem into one representation.

```text
Asset Register + linked data products
              |
              v
      Canonical data model
          /          \
         v            v
 Portfolio graph   State tables
 relationships    quantitative state
         \            /
          v          v
       Deterministic engine
       Wooldridge formulas
              |
              v
       Stochastic engine
       proxy + Monte Carlo
              |
              v
        Strategy engine
  constraints + network actions
              |
              v
         2027–2040 results
```

## Deterministic equation model

Purpose: calculate auditable annual asset/portfolio state. Wooldridge-derived formulas live in `formulas.py`. Caisse extensions live separately in `extensions.py`.

## Graph/network model

Purpose: represent relationships such as portfolio HAS_CAISSE Caisse, Caisse HAS_SITE Site, Site PROVIDES Service, Site HAS_SYSTEM System, Site SERVES Community and Site CAN_ABSORB_SERVICE_FROM Site.

The initial implementation uses NetworkX and tabular relationship data. A graph database is not required for the MVP. Neo4j or another graph store should be considered only if relationship volume/querying/lineage justifies it.

## Stochastic model

Purpose: represent uncertain deterioration, construction cost, demand, delivery, energy intensity, retrofit performance and other calibrated variables. Preserve deterministic mechanics underneath Monte Carlo.

## Decision/optimization model

Purpose: select feasible strategies under multiple objectives and constraints. Candidate methods include facility-location, set-covering, p-median/network optimization and multi-objective mathematical programming. This is a later stage after deterministic mechanics and service constraints are validated.

## AI boundary

Natural-language intent → LLM-generated validated scenario configuration → Python calculation/simulation → structured results → LLM explanation.

The LLM should not directly calculate portfolio forecasts.
