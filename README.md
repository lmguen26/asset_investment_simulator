# Asset Investment Simulator

Python/Streamlit decision-support application for long-range Caisse network portfolio investment planning.

## Current status

The repository now contains a complete **deterministic 2027–2040 baseline engine**. It calculates annual state transitions at the site level, rolls results to each Caisse subportfolio and then to the full network portfolio.

This deterministic baseline is intentionally established before Monte Carlo or optimization. Stochastic sophistication should not be added until the annual mechanics, assumptions and data mappings are trusted.

## Modelling architecture

The simulator separates three complementary paradigms:

1. **Wooldridge deterministic core** — condition, backlog, Sustainment, Improvement, Development, CRV, system renewal and economic formulas.
2. **Caisse portfolio/network model** — 189 Caisse subportfolios containing sites, service relationships, energy/carbon and later explicit portfolio actions.
3. **Uncertainty and decision support** — proxy models, Monte Carlo and later constrained network optimization.

The graph/network model does **not** replace the equations. It describes relationships and constraints in which the quantitative models operate.

## Canonical Wooldridge terminology

| Driver | Condition dimension | Investment class |
|---|---|---|
| Deterioration | Technical Backlog / Technical Condition Index | Sustainment |
| Obsolescence | Functional Backlog / Functional Condition Index | Improvement |
| Capacity | Capacity Backlog / Capacity Condition Index | Development |

Operations is the fourth investment cash-flow class. Comprehensive Condition combines Technical, Functional and Capacity backlog relative to CRV.

## Portfolio hierarchy

`Caisse Network Portfolio -> Caisse (189 subportfolios) -> Site(s)`

A Caisse is an organizational/subportfolio entity. A site is a physical/service location. Closing a site does not necessarily remove a service: services may be redistributed, consolidated or replaced by another service point such as an ATM.

## Deterministic engine

Implemented in `src/asset_investment_simulator/engine.py`.

The engine provides:

- 2027–2040 annual site state transitions;
- exact Wooldridge-derived Technical / Functional / Capacity backlog propagation;
- Comprehensive Condition calculations;
- optional system renewal schedules using remaining life, renewal cost and renewal-cycle timing;
- configurable CRV-based annual requirements;
- requirement, maintain-backlog, target-CI and fixed funding policies;
- OPEX, energy, operational-carbon and service-capacity extensions;
- site -> Caisse -> portfolio aggregation;
- Present Value of TOTEX;
- full calculation-audit fields;
- deterministic scenario library.

See `docs/DETERMINISTIC_ENGINE.md` for mechanics, provenance and limitations.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest -q
```

The application initially loads a small fictitious demonstration portfolio. Import your canonical Asset Register to replace it.

## Asset Register workflow

The supported ingestion pattern is:

`Raw Asset Register -> external field mapping -> canonical OSCRE-aligned import template -> validation -> simulator`

Use `data/templates/asset_register_template.csv` as the target export format. Exact OSCRE IDM entity/attribute identifiers must be validated against the selected licensed OSCRE use-case schema; this repository therefore says **OSCRE-aligned**, not OSCRE-conformant.

Condition, energy, carbon and service data should remain linked data products rather than being fabricated as Asset Register identity attributes. For optional explicit system renewal modelling, use `data/templates/system_renewal_template.csv`.

## Documentation

- `docs/HOW_TO_USE.md` — operating instructions
- `docs/MODEL_GUIDE.md` — principles, formulas, terminology and limitations
- `docs/DETERMINISTIC_ENGINE.md` — deterministic calculation mechanics and provenance
- `docs/ARCHITECTURE.md` — deterministic + graph/network + stochastic architecture
- `docs/ASSET_REGISTER_MAPPING.md` — canonical import profile and mapping workflow
- `docs/AI_FEEDBACK_LOOP.md` — human notes and JSON feedback contract

## Modelling rule

Any code change that alters a 2040 curve must identify the equation, assumption, data mapping, scenario policy or business rule responsible and add/update regression tests.

## Important interpretation

A scenario is not a forecast. A 2040 result is the consequence of initial conditions, assumptions and selected policies. The deterministic engine does not quantify uncertainty; Monte Carlo will be added as a separate layer later.
